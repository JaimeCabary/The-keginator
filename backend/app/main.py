# from fastapi import FastAPI, File, UploadFile, HTTPException, Query
# from fastapi.responses import FileResponse, JSONResponse
# from fastapi.middleware.cors import CORSMiddleware
# import pandas as pd
# import hashlib
# import os
# import uuid
# from datetime import datetime
# from typing import Optional
# import io
# from pathlib import Path

# from .cleaning import DataCleaner
# from .blockchain import SolanaClient
# from .database import Database
# from .models import DatasetMetadata, VerifyResponse, HistoryResponse

# app = FastAPI(title="Keginator API", version="1.0.0")

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
#     auto_commit: bool = Query(False, description="Auto-commit to Solana")
# ):
#     """
#     Upload and clean dataset
#     Returns: cleaned file + dataset hash
#     """
#     try:
#         # Validate file type
#         if not file.filename.endswith(('.csv', '.json', '.xlsx', '.xls')):
#             raise HTTPException(400, "Unsupported file format. Use CSV, JSON, or XLSX")
        
#         # Read file content
#         content = await file.read()
        
#         # Load dataset
#         if file.filename.endswith('.csv'):
#             df = pd.read_csv(io.BytesIO(content))
#         elif file.filename.endswith('.json'):
#             df = pd.read_json(io.BytesIO(content))
#         elif file.filename.endswith(('.xlsx', '.xls')):
#             df = pd.read_excel(io.BytesIO(content))
        
#         # Clean dataset
#         cleaned_df, cleaning_report = cleaner.clean(df)
        
#         # Generate unique ID and hash
#         dataset_id = str(uuid.uuid4())
#         cleaned_csv = cleaned_df.to_csv(index=False)
#         dataset_hash = hashlib.sha256(cleaned_csv.encode()).hexdigest()
        
#         # Save cleaned file
#         cleaned_filename = f"{dataset_id}_cleaned.csv"
#         cleaned_path = CLEANED_DIR / cleaned_filename
#         cleaned_df.to_csv(cleaned_path, index=False)
        
#         # Store metadata in database
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
        
#         # Auto-commit to Solana if requested
#         solana_signature = None
#         if auto_commit:
#             try:
#                 solana_signature = await solana_client.commit_hash(
#                     dataset_hash, user_id, int(datetime.utcnow().timestamp())
#                 )
#                 await db.update_solana_status(dataset_id, True, solana_signature)
#             except Exception as e:
#                 print(f"⚠️ Solana commit failed: {e}")
        
#         return JSONResponse({
#             "success": True,
#             "dataset_id": dataset_id,
#             "dataset_hash": dataset_hash,
#             "original_rows": len(df),
#             "cleaned_rows": len(cleaned_df),
#             "columns": list(cleaned_df.columns),
#             "cleaning_report": cleaning_report,
#             "download_url": f"/download/{dataset_id}",
#             "solana_signature": solana_signature,
#             "committed_to_solana": auto_commit and solana_signature is not None
#         })
        
#     except pd.errors.EmptyDataError:
#         raise HTTPException(400, "Empty dataset")
#     except Exception as e:
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


# @app.get("/history/{user_id}")
# async def get_history(user_id: str, limit: int = Query(50, le=100)):
#     """Get user's dataset history"""
#     history = await db.get_user_history(user_id, limit)
    
#     return HistoryResponse(
#         user_id=user_id,
#         total_datasets=len(history),
#         datasets=history
#     )


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


# # from fastapi import FastAPI, File, UploadFile, HTTPException, Query
# # from fastapi.responses import JSONResponse, FileResponse
# # from fastapi.middleware.cors import CORSMiddleware
# # import pandas as pd
# # import hashlib
# # import uuid
# # from datetime import datetime
# # from pathlib import Path
# # import io

# # app = FastAPI(title="Keginator API", version="1.0.0")

# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # UPLOAD_DIR = Path("uploads")
# # CLEANED_DIR = Path("cleaned")
# # UPLOAD_DIR.mkdir(exist_ok=True)
# # CLEANED_DIR.mkdir(exist_ok=True)

# # @app.get("/")
# # async def root():
# #     return {
# #         "message": "Keginator API - Data Cleaning Engine",
# #         "version": "1.0.0",
# #         "status": "running"
# #     }

# # @app.get("/health")
# # async def health():
# #     return {
# #         "status": "healthy",
# #         "timestamp": datetime.utcnow().isoformat()
# #     }

# # @app.post("/upload")
# # async def upload_dataset(
# #     file: UploadFile = File(...),
# #     user_id: str = Query(..., description="User identifier")
# # ):
# #     try:
# #         if not file.filename.endswith(('.csv', '.json', '.xlsx')):
# #             raise HTTPException(400, "Unsupported file format")
        
# #         content = await file.read()
        
# #         if file.filename.endswith('.csv'):
# #             df = pd.read_csv(io.BytesIO(content))
# #         else:
# #             raise HTTPException(400, "Only CSV supported in demo")
        
# #         # Basic cleaning
# #         original_rows = len(df)
# #         df = df.drop_duplicates()
# #         df = df.dropna(how='all')
# #         cleaned_rows = len(df)
        
# #         # Generate hash
# #         dataset_id = str(uuid.uuid4())
# #         cleaned_csv = df.to_csv(index=False)
# #         dataset_hash = hashlib.sha256(cleaned_csv.encode()).hexdigest()
        
# #         # Save cleaned file
# #         cleaned_filename = f"{dataset_id}_cleaned.csv"
# #         cleaned_path = CLEANED_DIR / cleaned_filename
# #         df.to_csv(cleaned_path, index=False)
        
# #         return JSONResponse({
# #             "success": True,
# #             "dataset_id": dataset_id,
# #             "dataset_hash": dataset_hash,
# #             "original_rows": original_rows,
# #             "cleaned_rows": cleaned_rows,
# #             "columns": list(df.columns),
# #             "download_url": f"/download/{dataset_id}"
# #         })
        
# #     except Exception as e:
# #         raise HTTPException(500, f"Error: {str(e)}")

# # @app.get("/download/{dataset_id}")
# # async def download_cleaned(dataset_id: str):
# #     file_path = CLEANED_DIR / f"{dataset_id}_cleaned.csv"
# #     if not file_path.exists():
# #         raise HTTPException(404, "Dataset not found")
# #     return FileResponse(file_path, media_type="text/csv", filename=f"{dataset_id}_cleaned.csv")


from fastapi import FastAPI, File, UploadFile, HTTPException, Query, Depends
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import hashlib
import os
import uuid
from datetime import datetime
from typing import Optional
import io
from pathlib import Path

from .cleaning import DataCleaner
from .blockchain import SolanaClient
from .database import Database
from .models import DatasetMetadata, VerifyResponse, HistoryResponse
from .auth import router as auth_router, get_current_user, update_user_stats

app = FastAPI(title="Keginator API", version="1.0.0")

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

# Include auth router
app.include_router(auth_router)

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

# @app.post("/upload")
# async def upload_dataset(
#     file: UploadFile = File(...),
#     user_id: str = Query(..., description="User identifier"),
#     auto_commit: bool = Query(False, description="Auto-commit to Solana")
# ):
#     """
#     Upload and clean dataset
#     Returns: cleaned file + dataset hash
#     """
#     try:
#         # Validate file type
#         if not file.filename.endswith(('.csv', '.json', '.xlsx', '.xls')):
#             raise HTTPException(400, "Unsupported file format. Use CSV, JSON, or XLSX")
        
#         # Read file content
#         content = await file.read()
        
#         # Load dataset
#         if file.filename.endswith('.csv'):
#             df = pd.read_csv(io.BytesIO(content))
#         elif file.filename.endswith('.json'):
#             df = pd.read_json(io.BytesIO(content))
#         elif file.filename.endswith(('.xlsx', '.xls')):
#             df = pd.read_excel(io.BytesIO(content))
        
#         # Clean dataset
#         cleaned_df, cleaning_report = cleaner.clean(df)
        
#         # Generate unique ID and hash
#         dataset_id = str(uuid.uuid4())
#         cleaned_csv = cleaned_df.to_csv(index=False)
#         dataset_hash = hashlib.sha256(cleaned_csv.encode()).hexdigest()
        
#         # Save cleaned file
#         cleaned_filename = f"{dataset_id}_cleaned.csv"
#         cleaned_path = CLEANED_DIR / cleaned_filename
#         cleaned_df.to_csv(cleaned_path, index=False)
        
#         # Store metadata in database
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
        
#         # Update user stats
#         dataset_size = len(content)
#         update_user_stats(user_id, dataset_size)
        
#         # Auto-commit to Solana if requested
#         solana_signature = None
#         if auto_commit:
#             try:
#                 solana_signature = await solana_client.commit_hash(
#                     dataset_hash, user_id, int(datetime.utcnow().timestamp())
#                 )
#                 await db.update_solana_status(dataset_id, True, solana_signature)
#             except Exception as e:
#                 print(f"⚠️ Solana commit failed: {e}")
        
#         return JSONResponse({
#             "success": True,
#             "dataset_id": dataset_id,
#             "dataset_hash": dataset_hash,
#             "original_rows": len(df),
#             "cleaned_rows": len(cleaned_df),
#             "columns": list(cleaned_df.columns),
#             "cleaning_report": cleaning_report,
#             "download_url": f"/download/{dataset_id}",
#             "solana_signature": solana_signature,
#             "committed_to_solana": auto_commit and solana_signature is not None
#         })
        
#     except pd.errors.EmptyDataError:
#         raise HTTPException(400, "Empty dataset")
#     except Exception as e:
#         raise HTTPException(500, f"Processing error: {str(e)}")

@app.post("/upload")
async def upload_dataset(
    file: UploadFile = File(...),
    user_id: str = Query(..., description="User identifier"),
    auto_commit: bool = Query(False, description="Auto-commit to Solana")
):
    try:
        # Validate file type
        if not file.filename.endswith(('.csv', '.json', '.xlsx', '.xls')):
            raise HTTPException(400, "Unsupported file format. Use CSV, JSON, or XLSX")
        
        # Read file content
        content = await file.read()
        file_size = len(content)  # ACTUAL FILE SIZE IN BYTES
        
        # Load dataset
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(content))
        elif file.filename.endswith('.json'):
            df = pd.read_json(io.BytesIO(content))
        elif file.filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(io.BytesIO(content))
        
        # Clean dataset
        cleaned_df, cleaning_report = cleaner.clean(df)
        
        # Generate unique ID and hash
        dataset_id = str(uuid.uuid4())
        cleaned_csv = cleaned_df.to_csv(index=False)
        cleaned_size = len(cleaned_csv.encode())  # CLEANED SIZE IN BYTES
        dataset_hash = hashlib.sha256(cleaned_csv.encode()).hexdigest()
        
        # Save cleaned file
        cleaned_filename = f"{dataset_id}_cleaned.csv"
        cleaned_path = CLEANED_DIR / cleaned_filename
        cleaned_df.to_csv(cleaned_path, index=False)
        
        # Store metadata in database
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
        
        # Update user stats with ACTUAL file size
        update_user_stats(user_id, file_size)
        
        # Auto-commit to Solana if requested
        solana_signature = None
        if auto_commit:
            try:
                solana_signature = await solana_client.commit_hash(
                    dataset_hash, user_id, int(datetime.utcnow().timestamp())
                )
                await db.update_solana_status(dataset_id, True, solana_signature)
            except Exception as e:
                print(f"⚠️ Solana commit failed: {e}")
        
        # Format file sizes properly
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
            "file_size": format_bytes(file_size),  # NEW: Formatted size
            "cleaned_size": format_bytes(cleaned_size),  # NEW: Cleaned size
            "file_size_bytes": file_size,  # NEW: Raw bytes for frontend
            "cleaned_size_bytes": cleaned_size,  # NEW: Raw bytes for frontend
            "cleaning_report": cleaning_report,
            "download_url": f"/download/{dataset_id}",
            "solana_signature": solana_signature,
            "committed_to_solana": auto_commit and solana_signature is not None
        })
        
    except pd.errors.EmptyDataError:
        raise HTTPException(400, "Empty dataset")
    except Exception as e:
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