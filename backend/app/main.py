# from dotenv import load_dotenv
# import os
# load_dotenv()

# from fastapi import FastAPI, File, UploadFile, HTTPException, Query, Depends
# from fastapi.responses import FileResponse, JSONResponse
# from fastapi.middleware.cors import CORSMiddleware
# from starlette.middleware.sessions import SessionMiddleware
# import pandas as pd
# import hashlib
# import uuid
# from datetime import datetime
# from typing import Optional
# import io
# from pathlib import Path
# import json

# from .cleaning import DataCleaner
# from .blockchain import SolanaClient
# from .database import Database
# from .models import DatasetMetadata, VerifyResponse, HistoryResponse
# from .auth import router as auth_router, get_current_user, update_user_stats

# app = FastAPI(title="Keginator API", version="1.0.0")

# # Add SessionMiddleware
# app.add_middleware(
#     SessionMiddleware,
#     secret_key="142af9a5f574a2c6eb19e218711370f6538c5611184aec51b70cabe4ac00218d"
# )

# # Include auth router (only once)
# app.include_router(auth_router)

# # CORS for React frontend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "https://keginator.vercel.app",
#         "http://localhost:3000",
#         "*"  # Remove in production
#     ],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Initialize components
# db = Database()
# cleaner = DataCleaner()
# solana_client = SolanaClient()

# # Storage directories
# UPLOAD_DIR = Path("uploads")
# CLEANED_DIR = Path("cleaned")
# UPLOAD_DIR.mkdir(exist_ok=True)
# CLEANED_DIR.mkdir(exist_ok=True)

# @app.on_event("startup")
# async def startup():
#     """Initialize database and connections"""
#     await db.connect()
#     print("✅ Keginator API Ready")

# @app.on_event("shutdown")
# async def shutdown():
#     """Cleanup connections"""
#     await db.disconnect()

# @app.get("/")
# async def root():
#     return {
#         "message": "Keginator API - Data Cleaning + Solana Blockchain",
#         "version": "1.0.0",
#         "endpoints": ["/upload", "/history/{user_id}", "/commit", "/verify/{hash}"]
#     }

# @app.post("/upload")
# async def upload_dataset(
#     file: UploadFile = File(...),
#     user_id: str = Query(..., description="User identifier"),
#     auto_commit: bool = Query(True, description="Auto-commit to Solana")  # Changed default to True
# ):
#     try:
#         # Validate file type
#         if not file.filename.endswith(('.csv', '.json', '.xlsx', '.xls')):
#             raise HTTPException(400, "Unsupported file format. Use CSV, JSON, or XLSX")
        
#         # Read file content
#         content = await file.read()
#         file_size = len(content)
        
#         # Load dataset
#         if file.filename.endswith('.csv'):
#             df = pd.read_csv(io.BytesIO(content))
#         elif file.filename.endswith('.json'):
#             df = pd.read_json(io.BytesIO(content))
#         elif file.filename.endswith(('.xlsx', '.xls')):
#             df = pd.read_excel(io.BytesIO(content))
        
#         # Clean dataset
#         cleaned_df, cleaning_report = cleaner.clean(df)
        
#         # Generate hash FIRST
#         cleaned_csv = cleaned_df.to_csv(index=False)
#         cleaned_size = len(cleaned_csv.encode())
#         dataset_hash = hashlib.sha256(cleaned_csv.encode()).hexdigest()
        
#         # CHECK IF HASH ALREADY EXISTS
#         existing_metadata = None
#         if db.use_sqlite:
#             cursor = db.sqlite_conn.cursor()
#             cursor.execute('SELECT * FROM datasets WHERE dataset_hash = ?', (dataset_hash,))
#             existing_row = cursor.fetchone()
#             if existing_row:
#                 existing_metadata = {
#                     "id": existing_row['id'],
#                     "dataset_hash": existing_row['dataset_hash'],
#                     "original_rows": existing_row['rows_original'],
#                     "cleaned_rows": existing_row['rows_cleaned'],
#                     "columns": existing_row['columns'],
#                     "cleaning_report": json.loads(existing_row['cleaning_report']),
#                     "download_url": f"/download/{existing_row['id']}",
#                     "solana_signature": existing_row['solana_signature'],
#                     "committed_to_solana": bool(existing_row['committed_to_solana'])
#                 }
#         else:
#             if db.pool:
#                 async with db.pool.acquire() as conn:
#                     existing_row = await conn.fetchrow(
#                         'SELECT * FROM datasets WHERE dataset_hash = $1', dataset_hash
#                     )
#                     if existing_row:
#                         existing_metadata = {
#                             "id": existing_row['id'],
#                             "dataset_hash": existing_row['dataset_hash'],
#                             "original_rows": existing_row['rows_original'],
#                             "cleaned_rows": existing_row['rows_cleaned'],
#                             "columns": existing_row['columns'],
#                             "cleaning_report": json.loads(existing_row['cleaning_report']),
#                             "download_url": f"/download/{existing_row['id']}",
#                             "solana_signature": existing_row['solana_signature'],
#                             "committed_to_solana": existing_row['committed_to_solana']
#                         }
        
#         if existing_metadata:
#             def format_bytes(bytes_val):
#                 if bytes_val < 1024:
#                     return f"{bytes_val} B"
#                 elif bytes_val < 1024 * 1024:
#                     return f"{bytes_val / 1024:.2f} KB"
#                 else:
#                     return f"{bytes_val / (1024 * 1024):.2f} MB"
            
#             return JSONResponse({
#                 "success": True,
#                 "message": "Dataset already exists (duplicate)",
#                 "dataset_id": existing_metadata['id'],
#                 "dataset_hash": existing_metadata['dataset_hash'],
#                 "original_rows": existing_metadata['original_rows'],
#                 "cleaned_rows": existing_metadata['cleaned_rows'],
#                 "columns": existing_metadata['columns'],
#                 "file_size": format_bytes(file_size),
#                 "cleaned_size": format_bytes(cleaned_size),
#                 "file_size_bytes": file_size,
#                 "cleaned_size_bytes": cleaned_size,
#                 "cleaning_report": existing_metadata['cleaning_report'],
#                 "download_url": existing_metadata['download_url'],
#                 "solana_signature": existing_metadata['solana_signature'],
#                 "committed_to_solana": existing_metadata['committed_to_solana']
#             })
        
#         # Generate unique ID
#         dataset_id = str(uuid.uuid4())
        
#         # FIXED: Save with original name + hash
#         original_name = file.filename.rsplit('.', 1)[0]  # Remove extension
#         hash_short = dataset_hash[:8]
#         cleaned_filename = f"{original_name}_{hash_short}_cleaned.csv"
#         cleaned_path = CLEANED_DIR / cleaned_filename
#         cleaned_df.to_csv(cleaned_path, index=False)
        
#         # Store metadata
#         metadata = DatasetMetadata(
#             id=dataset_id,
#             user_id=user_id,
#             original_filename=file.filename,
#             cleaned_filename=cleaned_filename,
#             dataset_hash=dataset_hash,
#             rows_original=len(df),
#             rows_cleaned=len(cleaned_df),
#             columns=len(cleaned_df.columns),
#             cleaning_report=cleaning_report,
#             created_at=datetime.utcnow(),
#             committed_to_solana=False
#         )
        
#         await db.insert_metadata(metadata)
#         print(f"✅ Saved metadata to database: {dataset_id}")
        
#         # Update user stats
#         update_user_stats(user_id, file_size)
        
#         # Auto-commit to Solana
#         solana_signature = None
#         if auto_commit:
#             try:
#                 solana_signature = await solana_client.commit_hash(
#                     dataset_hash, user_id, int(datetime.utcnow().timestamp())
#                 )
#                 await db.update_solana_status(dataset_id, True, solana_signature)
#                 print(f"✅ Committed to Solana: {solana_signature}")
#             except Exception as e:
#                 print(f"⚠️ Solana commit failed: {e}")
        
#         def format_bytes(bytes_val):
#             if bytes_val < 1024:
#                 return f"{bytes_val} B"
#             elif bytes_val < 1024 * 1024:
#                 return f"{bytes_val / 1024:.2f} KB"
#             else:
#                 return f"{bytes_val / (1024 * 1024):.2f} MB"
        
#         return JSONResponse({
#             "success": True,
#             "dataset_id": dataset_id,
#             "dataset_hash": dataset_hash,
#             "original_rows": len(df),
#             "cleaned_rows": len(cleaned_df),
#             "columns": list(cleaned_df.columns),
#             "file_size": format_bytes(file_size),
#             "cleaned_size": format_bytes(cleaned_size),
#             "file_size_bytes": file_size,
#             "cleaned_size_bytes": cleaned_size,
#             "cleaning_report": cleaning_report,
#             "download_url": f"/download/{dataset_id}",
#             "solana_signature": solana_signature,
#             "committed_to_solana": auto_commit and solana_signature is not None
#         })
        
#     except pd.errors.EmptyDataError:
#         raise HTTPException(400, "Empty dataset")
#     except Exception as e:
#         print(f"Upload error: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         raise HTTPException(500, f"Processing error: {str(e)}")
        
# @app.get("/download/{dataset_id}")
# async def download_cleaned(dataset_id: str):
#     """Download cleaned dataset"""
#     metadata = await db.get_metadata(dataset_id)
#     if not metadata:
#         raise HTTPException(404, "Dataset not found")
    
#     file_path = CLEANED_DIR / metadata.cleaned_filename
#     if not file_path.exists():
#         raise HTTPException(404, "Cleaned file not found")
    
#     return FileResponse(
#         file_path,
#         media_type="text/csv",
#         filename=metadata.cleaned_filename
#     )

# # @app.get("/history/{user_id}")
# # async def get_history(user_id: str, limit: int = Query(50, le=100)):
# #     """Get user's dataset history"""
# #     history = await db.get_user_history(user_id, limit)
    
# #     return HistoryResponse(
# #         user_id=user_id,
# #         total_datasets=len(history),
# #         datasets=history
# #     )

# @app.get("/history/{user_id}")
# async def get_history(user_id: str, limit: int = Query(50, le=100)):
#     """Get user's dataset history from DATABASE"""
#     try:
#         history = await db.get_user_history(user_id, limit)
        
#         # Transform to match frontend format
#         datasets_transformed = []
#         for dataset in history:
#             datasets_transformed.append({
#                 "id": dataset.id,
#                 "filename": dataset.original_filename,
#                 "originalSize": dataset.rows_original * 1000,  # Estimate from rows
#                 "cleanedSize": dataset.rows_cleaned * 1000,
#                 "hash": dataset.dataset_hash,
#                 "timestamp": dataset.created_at.isoformat(),
#                 "solanaTx": dataset.solana_signature,
#                 "status": "completed" if dataset.committed_to_solana else "processing"
#             })
        
#         return {
#             "user_id": user_id,
#             "total_datasets": len(datasets_transformed),
#             "datasets": datasets_transformed
#         }
#     except Exception as e:
#         print(f"History fetch error: {e}")
#         return {
#             "user_id": user_id,
#             "total_datasets": 0,
#             "datasets": []
#         }

# @app.post("/commit")
# async def commit_to_solana(
#     dataset_id: str = Query(...),
#     user_id: str = Query(...)
# ):
#     """Commit dataset hash to Solana blockchain"""
#     metadata = await db.get_metadata(dataset_id)
#     if not metadata:
#         raise HTTPException(404, "Dataset not found")
    
#     if metadata.user_id != user_id:
#         raise HTTPException(403, "Unauthorized")
    
#     if metadata.committed_to_solana:
#         return {
#             "success": True,
#             "message": "Already committed",
#             "solana_signature": metadata.solana_signature
#         }
    
#     try:
#         signature = await solana_client.commit_hash(
#             metadata.dataset_hash,
#             user_id,
#             int(metadata.created_at.timestamp())
#         )
        
#         await db.update_solana_status(dataset_id, True, signature)
        
#         return {
#             "success": True,
#             "dataset_hash": metadata.dataset_hash,
#             "solana_signature": signature,
#             "explorer_url": f"https://explorer.solana.com/tx/{signature}?cluster=devnet"
#         }
#     except Exception as e:
#         raise HTTPException(500, f"Solana commit failed: {str(e)}")

# @app.get("/verify/{dataset_hash}")
# async def verify_hash(dataset_hash: str):
#     """Verify if dataset hash exists on Solana"""
#     try:
#         exists, timestamp = await solana_client.verify_hash(dataset_hash)
        
#         return VerifyResponse(
#             dataset_hash=dataset_hash,
#             exists_on_chain=exists,
#             timestamp=timestamp,
#             verified_at=datetime.utcnow()
#         )
#     except Exception as e:
#         raise HTTPException(500, f"Verification failed: {str(e)}")

# @app.get("/health")
# async def health_check():
#     """Health check endpoint"""
#     return {
#         "status": "healthy",
#         "timestamp": datetime.utcnow().isoformat(),
#         "solana_connected": solana_client.is_connected()
#     }

# # Add payment endpoints (for Pricing page)
# @app.post("/payment/upgrade")
# async def upgrade_plan(
#     plan: str,
#     user_id: str,
#     current_user: dict = Depends(get_current_user)
# ):
#     """Upgrade user plan"""
#     # In a real implementation, this would handle payment processing
#     # For now, just update the user's plan
#     from .auth import users_db
    
#     if user_id not in users_db:
#         raise HTTPException(404, "User not found")
    
#     users_db[user_id]["plan"] = plan
    
#     return {
#         "success": True,
#         "message": f"Plan upgraded to {plan}",
#         "user": users_db[user_id]
#     }

# @app.post("/payment/verify")
# async def verify_payment(
#     reference: str,
#     plan: str,
#     current_user: dict = Depends(get_current_user)
# ):
#     """Verify payment (mock implementation)"""
#     # In a real implementation, this would verify with Paystack/Stripe
#     return {
#         "success": True,
#         "message": "Payment verified successfully",
#         "plan": plan,
#         "reference": reference
#     }



# main.py

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
from typing import Optional, Dict, Any, Union
import io
from pathlib import Path
import json
import logging
import httpx # NEW IMPORT for async HTTP requests (Paystack API)

from .cleaning import DataCleaner
from .audio_processor import AudioProcessor
from .blockchain import SolanaClient
from .database import Database
from .models import DatasetMetadata, VerifyResponse, HistoryResponse
from .auth import router as auth_router, get_current_user, update_user_stats

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Paystack Configuration ---
PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY")
PAYSTACK_API_BASE = "https://api.paystack.co"

if not PAYSTACK_SECRET_KEY:
    logger.warning("⚠️ PAYSTACK_SECRET_KEY not set. Payment endpoints will fail.")
# -----------------------------

app = FastAPI(title="Keginator API", version="1.0.0")

# Add SessionMiddleware
app.add_middleware(
    SessionMiddleware,
    secret_key="142af9a5f574a2c6eb19e218711370f6538c5611184aec51b70cabe4ac00218d"
)

# Include auth router
app.include_router(auth_router)

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://keginator.vercel.app",
        "http://localhost:3000",
        "*" 
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
db = Database()
cleaner = DataCleaner()
audio_processor = AudioProcessor() 
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
    logger.info("✅ Keginator API Ready")

@app.on_event("shutdown")
async def shutdown():
    """Cleanup connections"""
    await db.disconnect()

@app.get("/")
async def root():
    return {
        "message": "Keginator API - Data Cleaning + Solana Blockchain",
        "version": "1.0.0",
        "endpoints": ["/upload", "/history/{user_id}", "/commit", "/verify/{hash}", "/payment/initialize", "/payment/verify"]
    }

def get_file_type(filename: str) -> str:
    """Helper to determine file type based on extension."""
    ext = filename.split('.')[-1].lower()
    if ext in ('csv', 'json', 'xlsx', 'xls'):
        return "tabular"
    elif ext in ('mp3', 'wav'):
        return "audio"
    return "unsupported"

@app.post("/upload")
async def upload_dataset(
    file: UploadFile = File(...),
    user_id: str = Query(..., description="User identifier"),
    auto_commit: bool = Query(True, description="Auto-commit to Solana")
):
    """
    Handles file upload and dynamic routing for cleaning/processing.
    Supports CSV, JSON, XLSX (Tabular) and MP3, WAV (Audio).
    """
    try:
        file_type = get_file_type(file.filename)
        content = await file.read()
        file_size = len(content)

        if file_type == "tabular":
            # --- Tabular Data Processing ---
            
            # 1. Load dataset
            if file.filename.endswith('.csv'):
                df = pd.read_csv(io.BytesIO(content))
            elif file.filename.endswith('.json'):
                df = pd.read_json(io.BytesIO(content))
            elif file.filename.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(io.BytesIO(content))
            
            # 2. Clean, scale, encode, and embed dataset
            cleaned_df, cleaning_report = cleaner.clean(df)
            
            # 3. Generate hash and check for duplicates
            cleaned_csv = cleaned_df.to_csv(index=False)
            cleaned_size = len(cleaned_csv.encode())
            dataset_hash = hashlib.sha256(cleaned_csv.encode()).hexdigest()
            
            existing_metadata: Optional[Dict[str, Any]] = None
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
                    "type": "tabular_duplicate",
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
                    "download_url": f"/download/{existing_metadata['id']}",
                    "solana_signature": existing_metadata['solana_signature'],
                    "committed_to_solana": existing_metadata['committed_to_solana']
                })
            
            # 4. Save file and metadata
            dataset_id = str(uuid.uuid4())
            original_name = file.filename.rsplit('.', 1)[0]
            hash_short = dataset_hash[:8]
            cleaned_filename = f"{original_name}_{hash_short}_cleaned.csv"
            cleaned_path = CLEANED_DIR / cleaned_filename
            cleaned_df.to_csv(cleaned_path, index=False)
            
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
            logger.info(f"✅ Saved metadata to database: {dataset_id}")
            
            # 5. Update user stats
            update_user_stats(user_id, file_size)
            
            # 6. Auto-commit to Solana
            solana_signature = None
            if auto_commit:
                try:
                    solana_signature = await solana_client.commit_hash(
                        dataset_hash, user_id, int(datetime.utcnow().timestamp())
                    )
                    await db.update_solana_status(dataset_id, True, solana_signature)
                    logger.info(f"✅ Committed hash to Solana: {solana_signature}")
                except Exception as e:
                    logger.warning(f"⚠️ Solana commit failed for tabular data: {e}")
            
            def format_bytes(bytes_val):
                if bytes_val < 1024:
                    return f"{bytes_val} B"
                elif bytes_val < 1024 * 1024:
                    return f"{bytes_val / 1024:.2f} KB"
                else:
                    return f"{bytes_val / (1024 * 1024):.2f} MB"
            
            return JSONResponse({
                "success": True,
                "type": "tabular",
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

        elif file_type == "audio":
            # --- Audio Data Processing ---
            if not audio_processor.model:
                 raise HTTPException(503, "Audio transcription service is unavailable (Model failed to load).")

            audio_report = audio_processor.process_audio(content, file.filename)
            
            # Log successful transcription (hash of transcript) to Solana
            transcription_hash = hashlib.sha256(audio_report['transcript_text'].encode('utf-8')).hexdigest()
            solana_signature = None
            
            if auto_commit:
                try:
                    solana_signature = await solana_client.commit_hash(
                        transcription_hash, user_id, int(datetime.utcnow().timestamp())
                    )
                    logger.info(f"✅ Committed transcript hash to Solana: {solana_signature}")
                except Exception as e:
                    logger.warning(f"⚠️ Solana commit failed for audio data: {e}")

            # Return a specialized response for audio
            return JSONResponse({
                "success": True,
                "type": "audio",
                "user_id": user_id,
                "original_filename": file.filename,
                "file_size_bytes": file_size,
                "audio_report": audio_report,
                "transcript_hash": transcription_hash,
                "solana_signature": solana_signature,
                "committed_to_solana": auto_commit and solana_signature is not None
            })

        else:
            raise HTTPException(400, f"Unsupported file format: {file.filename.split('.')[-1]}. Use CSV, JSON, XLSX, MP3, or WAV.")
        
    except pd.errors.EmptyDataError:
        raise HTTPException(400, "Empty dataset")
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
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
                "originalSize": dataset.rows_original * 1000, 
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
        logger.error(f"History fetch error: {e}")
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

# ====================================================================
# 💰 PAYSTACK PAYMENT ENDPOINTS (REPLACED MOCK IMPLEMENTATION)
# ====================================================================

@app.post("/payment/initialize")
async def initialize_payment(
    email: str = Query(..., description="User email for payment"),
    amount_kobo: int = Query(..., description="Amount in kobo (e.g., 50000 for N500)"),
    plan: str = Query(..., description="The plan being purchased (e.g., 'pro', 'enterprise')"),
    user_id: str = Query(..., description="User ID for metadata")
):
    """
    Initiates a payment transaction via Paystack.
    Returns: authorization URL.
    """
    if not PAYSTACK_SECRET_KEY:
        raise HTTPException(500, "Paystack is not configured. Missing PAYSTACK_SECRET_KEY.")
        
    url = f"{PAYSTACK_API_BASE}/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    
    # Paystack requires amount in kobo (or cents)
    payload = {
        "email": email,
        "amount": amount_kobo, 
        "metadata": {
            "custom_fields": [
                {"display_name": "User ID", "variable_name": "user_id", "value": user_id},
                {"display_name": "Plan", "variable_name": "plan", "value": plan},
            ]
        },
        # You can add a callback_url here to redirect the user after payment
        # "callback_url": f"https://keginator.vercel.app/payment/callback?user_id={user_id}" 
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()

            if data['status'] and data['data']['authorization_url']:
                return {
                    "success": True,
                    "message": "Payment initialization successful",
                    "authorization_url": data['data']['authorization_url'],
                    "reference": data['data']['reference']
                }
            
            logger.error(f"Paystack initialization failed: {data}")
            raise HTTPException(500, f"Payment initialization failed: {data.get('message', 'API error')}")

    except httpx.HTTPStatusError as e:
        logger.error(f"Paystack HTTP error: {e.response.text}")
        raise HTTPException(e.response.status_code, "Paystack API failed to initialize transaction.")
    except Exception as e:
        logger.error(f"Payment initialization error: {e}")
        raise HTTPException(500, f"An unexpected error occurred: {str(e)}")

@app.get("/payment/verify/{reference}")
async def verify_payment(
    reference: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Verifies a payment transaction using the Paystack reference.
    If successful, the user's plan is updated.
    """
    if not PAYSTACK_SECRET_KEY:
        raise HTTPException(500, "Paystack is not configured. Missing PAYSTACK_SECRET_KEY.")
        
    url = f"{PAYSTACK_API_BASE}/transaction/verify/{reference}"
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

            if data['status'] and data['data']['status'] == 'success':
                transaction_data = data['data']
                user_id = transaction_data['metadata']['custom_fields'][0]['value']
                plan = transaction_data['metadata']['custom_fields'][1]['value']
                
                # Update user plan in the mock database
                from .auth import users_db
                if user_id in users_db:
                    users_db[user_id]["plan"] = plan
                    logger.info(f"User {user_id} plan successfully upgraded to {plan} via Paystack.")
                
                return {
                    "success": True,
                    "message": "Payment verified and plan upgraded successfully",
                    "plan": plan,
                    "reference": reference,
                    "user_id": user_id,
                    "amount_paid_kobo": transaction_data['amount']
                }
            
            # Payment failed or not yet successful
            status = data['data'].get('status', 'N/A')
            logger.warning(f"Paystack verification failed/pending for ref {reference}. Status: {status}")
            return {
                "success": False,
                "message": f"Payment status is not successful: {status}",
                "reference": reference,
                "status": status
            }

    except httpx.HTTPStatusError as e:
        logger.error(f"Paystack HTTP error during verification: {e.response.text}")
        raise HTTPException(e.response.status_code, "Paystack API failed to verify transaction.")
    except Exception as e:
        logger.error(f"Payment verification error: {e}")
        raise HTTPException(500, f"An unexpected error occurred during verification: {str(e)}")