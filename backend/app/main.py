from dotenv import load_dotenv
import os
load_dotenv()

from fastapi import FastAPI, File, UploadFile, HTTPException, Query, Depends
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import pandas as pd
import hashlib
import uuid
from datetime import datetime
from typing import Optional
import io
from pathlib import Path
import json

from .cleaning import DataCleaner
from .blockchain import SolanaClient
from .database import Database
from .models import DatasetMetadata, VerifyResponse, HistoryResponse
from .auth import router as auth_router, get_current_user, update_user_stats

app = FastAPI(title="Keginator API", version="1.0.0")

# Add SessionMiddleware
app.add_middleware(
    SessionMiddleware,
    secret_key="142af9a5f574a2c6eb19e218711370f6538c5611184aec51b70cabe4ac00218d"
)

# Include auth router (only once)
app.include_router(auth_router)

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://keginator.vercel.app",
        "http://localhost:3000",
        "*"  # Remove in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
db = Database()
cleaner = DataCleaner()
solana_client = SolanaClient()

# Storage directories
UPLOAD_DIR = Path("uploads")
CLEANED_DIR = Path("cleaned")
UPLOAD_DIR.mkdir(exist_ok=True)
CLEANED_DIR.mkdir(exist_ok=True)

@app.on_event("startup")
async def startup():
    """Initialize database and connections"""
    await db.connect()
    print("✅ Keginator API Ready")

@app.on_event("shutdown")
async def shutdown():
    """Cleanup connections"""
    await db.disconnect()

@app.get("/")
async def root():
    return {
        "message": "Keginator API - Data Cleaning + Solana Blockchain",
        "version": "1.0.0",
        "endpoints": ["/upload", "/history/{user_id}", "/commit", "/verify/{hash}"]
    }

@app.post("/upload")
async def upload_dataset(
    file: UploadFile = File(...),
    user_id: str = Query(..., description="User identifier"),
    auto_commit: bool = Query(True, description="Auto-commit to Solana")  # Changed default to True
):
    try:
        # Validate file type
        if not file.filename.endswith(('.csv', '.json', '.xlsx', '.xls')):
            raise HTTPException(400, "Unsupported file format. Use CSV, JSON, or XLSX")
        
        # Read file content
        content = await file.read()
        file_size = len(content)
        
        # Load dataset
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(content))
        elif file.filename.endswith('.json'):
            df = pd.read_json(io.BytesIO(content))
        elif file.filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(io.BytesIO(content))
        
        # Clean dataset
        cleaned_df, cleaning_report = cleaner.clean(df)
        
        # Generate hash FIRST
        cleaned_csv = cleaned_df.to_csv(index=False)
        cleaned_size = len(cleaned_csv.encode())
        dataset_hash = hashlib.sha256(cleaned_csv.encode()).hexdigest()
        
        # CHECK IF HASH ALREADY EXISTS
        existing_metadata = None
        if db.use_sqlite:
            cursor = db.sqlite_conn.cursor()
            cursor.execute('SELECT * FROM datasets WHERE dataset_hash = ?', (dataset_hash,))
            existing_row = cursor.fetchone()
            if existing_row:
                existing_metadata = {
                    "id": existing_row['id'],
                    "dataset_hash": existing_row['dataset_hash'],
                    "original_rows": existing_row['rows_original'],
                    "cleaned_rows": existing_row['rows_cleaned'],
                    "columns": existing_row['columns'],
                    "cleaning_report": json.loads(existing_row['cleaning_report']),
                    "download_url": f"/download/{existing_row['id']}",
                    "solana_signature": existing_row['solana_signature'],
                    "committed_to_solana": bool(existing_row['committed_to_solana'])
                }
        else:
            if db.pool:
                async with db.pool.acquire() as conn:
                    existing_row = await conn.fetchrow(
                        'SELECT * FROM datasets WHERE dataset_hash = $1', dataset_hash
                    )
                    if existing_row:
                        existing_metadata = {
                            "id": existing_row['id'],
                            "dataset_hash": existing_row['dataset_hash'],
                            "original_rows": existing_row['rows_original'],
                            "cleaned_rows": existing_row['rows_cleaned'],
                            "columns": existing_row['columns'],
                            "cleaning_report": json.loads(existing_row['cleaning_report']),
                            "download_url": f"/download/{existing_row['id']}",
                            "solana_signature": existing_row['solana_signature'],
                            "committed_to_solana": existing_row['committed_to_solana']
                        }
        
        if existing_metadata:
            def format_bytes(bytes_val):
                if bytes_val < 1024:
                    return f"{bytes_val} B"
                elif bytes_val < 1024 * 1024:
                    return f"{bytes_val / 1024:.2f} KB"
                else:
                    return f"{bytes_val / (1024 * 1024):.2f} MB"
            
            return JSONResponse({
                "success": True,
                "message": "Dataset already exists (duplicate)",
                "dataset_id": existing_metadata['id'],
                "dataset_hash": existing_metadata['dataset_hash'],
                "original_rows": existing_metadata['original_rows'],
                "cleaned_rows": existing_metadata['cleaned_rows'],
                "columns": existing_metadata['columns'],
                "file_size": format_bytes(file_size),
                "cleaned_size": format_bytes(cleaned_size),
                "file_size_bytes": file_size,
                "cleaned_size_bytes": cleaned_size,
                "cleaning_report": existing_metadata['cleaning_report'],
                "download_url": existing_metadata['download_url'],
                "solana_signature": existing_metadata['solana_signature'],
                "committed_to_solana": existing_metadata['committed_to_solana']
            })
        
        # Generate unique ID
        dataset_id = str(uuid.uuid4())
        
        # FIXED: Save with original name + hash
        original_name = file.filename.rsplit('.', 1)[0]  # Remove extension
        hash_short = dataset_hash[:8]
        cleaned_filename = f"{original_name}_{hash_short}_cleaned.csv"
        cleaned_path = CLEANED_DIR / cleaned_filename
        cleaned_df.to_csv(cleaned_path, index=False)
        
        # Store metadata
        metadata = DatasetMetadata(
            id=dataset_id,
            user_id=user_id,
            original_filename=file.filename,
            cleaned_filename=cleaned_filename,
            dataset_hash=dataset_hash,
            rows_original=len(df),
            rows_cleaned=len(cleaned_df),
            columns=len(cleaned_df.columns),
            cleaning_report=cleaning_report,
            created_at=datetime.utcnow(),
            committed_to_solana=False
        )
        
        await db.insert_metadata(metadata)
        print(f"✅ Saved metadata to database: {dataset_id}")
        
        # Update user stats
        update_user_stats(user_id, file_size)
        
        # Auto-commit to Solana
        solana_signature = None
        if auto_commit:
            try:
                solana_signature = await solana_client.commit_hash(
                    dataset_hash, user_id, int(datetime.utcnow().timestamp())
                )
                await db.update_solana_status(dataset_id, True, solana_signature)
                print(f"✅ Committed to Solana: {solana_signature}")
            except Exception as e:
                print(f"⚠️ Solana commit failed: {e}")
        
        def format_bytes(bytes_val):
            if bytes_val < 1024:
                return f"{bytes_val} B"
            elif bytes_val < 1024 * 1024:
                return f"{bytes_val / 1024:.2f} KB"
            else:
                return f"{bytes_val / (1024 * 1024):.2f} MB"
        
        return JSONResponse({
            "success": True,
            "dataset_id": dataset_id,
            "dataset_hash": dataset_hash,
            "original_rows": len(df),
            "cleaned_rows": len(cleaned_df),
            "columns": list(cleaned_df.columns),
            "file_size": format_bytes(file_size),
            "cleaned_size": format_bytes(cleaned_size),
            "file_size_bytes": file_size,
            "cleaned_size_bytes": cleaned_size,
            "cleaning_report": cleaning_report,
            "download_url": f"/download/{dataset_id}",
            "solana_signature": solana_signature,
            "committed_to_solana": auto_commit and solana_signature is not None
        })
        
    except pd.errors.EmptyDataError:
        raise HTTPException(400, "Empty dataset")
    except Exception as e:
        print(f"Upload error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(500, f"Processing error: {str(e)}")
        
@app.get("/download/{dataset_id}")
async def download_cleaned(dataset_id: str):
    """Download cleaned dataset"""
    metadata = await db.get_metadata(dataset_id)
    if not metadata:
        raise HTTPException(404, "Dataset not found")
    
    file_path = CLEANED_DIR / metadata.cleaned_filename
    if not file_path.exists():
        raise HTTPException(404, "Cleaned file not found")
    
    return FileResponse(
        file_path,
        media_type="text/csv",
        filename=metadata.cleaned_filename
    )

# @app.get("/history/{user_id}")
# async def get_history(user_id: str, limit: int = Query(50, le=100)):
#     """Get user's dataset history"""
#     history = await db.get_user_history(user_id, limit)
    
#     return HistoryResponse(
#         user_id=user_id,
#         total_datasets=len(history),
#         datasets=history
#     )

@app.get("/history/{user_id}")
async def get_history(user_id: str, limit: int = Query(50, le=100)):
    """Get user's dataset history from DATABASE"""
    try:
        history = await db.get_user_history(user_id, limit)
        
        # Transform to match frontend format
        datasets_transformed = []
        for dataset in history:
            datasets_transformed.append({
                "id": dataset.id,
                "filename": dataset.original_filename,
                "originalSize": dataset.rows_original * 1000,  # Estimate from rows
                "cleanedSize": dataset.rows_cleaned * 1000,
                "hash": dataset.dataset_hash,
                "timestamp": dataset.created_at.isoformat(),
                "solanaTx": dataset.solana_signature,
                "status": "completed" if dataset.committed_to_solana else "processing"
            })
        
        return {
            "user_id": user_id,
            "total_datasets": len(datasets_transformed),
            "datasets": datasets_transformed
        }
    except Exception as e:
        print(f"History fetch error: {e}")
        return {
            "user_id": user_id,
            "total_datasets": 0,
            "datasets": []
        }

@app.post("/commit")
async def commit_to_solana(
    dataset_id: str = Query(...),
    user_id: str = Query(...)
):
    """Commit dataset hash to Solana blockchain"""
    metadata = await db.get_metadata(dataset_id)
    if not metadata:
        raise HTTPException(404, "Dataset not found")
    
    if metadata.user_id != user_id:
        raise HTTPException(403, "Unauthorized")
    
    if metadata.committed_to_solana:
        return {
            "success": True,
            "message": "Already committed",
            "solana_signature": metadata.solana_signature
        }
    
    try:
        signature = await solana_client.commit_hash(
            metadata.dataset_hash,
            user_id,
            int(metadata.created_at.timestamp())
        )
        
        await db.update_solana_status(dataset_id, True, signature)
        
        return {
            "success": True,
            "dataset_hash": metadata.dataset_hash,
            "solana_signature": signature,
            "explorer_url": f"https://explorer.solana.com/tx/{signature}?cluster=devnet"
        }
    except Exception as e:
        raise HTTPException(500, f"Solana commit failed: {str(e)}")

@app.get("/verify/{dataset_hash}")
async def verify_hash(dataset_hash: str):
    """Verify if dataset hash exists on Solana"""
    try:
        exists, timestamp = await solana_client.verify_hash(dataset_hash)
        
        return VerifyResponse(
            dataset_hash=dataset_hash,
            exists_on_chain=exists,
            timestamp=timestamp,
            verified_at=datetime.utcnow()
        )
    except Exception as e:
        raise HTTPException(500, f"Verification failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "solana_connected": solana_client.is_connected()
    }

# Add payment endpoints (for Pricing page)
@app.post("/payment/upgrade")
async def upgrade_plan(
    plan: str,
    user_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Upgrade user plan"""
    # In a real implementation, this would handle payment processing
    # For now, just update the user's plan
    from .auth import users_db
    
    if user_id not in users_db:
        raise HTTPException(404, "User not found")
    
    users_db[user_id]["plan"] = plan
    
    return {
        "success": True,
        "message": f"Plan upgraded to {plan}",
        "user": users_db[user_id]
    }

@app.post("/payment/verify")
async def verify_payment(
    reference: str,
    plan: str,
    current_user: dict = Depends(get_current_user)
):
    """Verify payment (mock implementation)"""
    # In a real implementation, this would verify with Paystack/Stripe
    return {
        "success": True,
        "message": "Payment verified successfully",
        "plan": plan,
        "reference": reference
    }