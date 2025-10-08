# auth.py
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import bcrypt
from datetime import datetime, timedelta
import os
from pydantic import BaseModel
from typing import Optional
import uuid


# Router for auth endpoints
router = APIRouter(prefix="/auth", tags=["authentication"])

# Security
security = HTTPBearer()
JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"

# Pydantic models
class UserSignup(BaseModel):
    name: str
    email: str
    password: str
    newsletter: bool = False

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    plan: str
    joined_date: str
    datasets_processed: int
    total_storage_used: int
    newsletter_subscribed: bool

# Mock user database (replace with real database in production)
users_db = {}
user_stats = {}

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_token(user_id: str, email: str) -> str:
    payload = {
        "user_id": user_id,
        "email": email,
        "exp": datetime.utcnow() + timedelta(days=7)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_token(token)
    
    user_id = payload.get("user_id")
    if user_id not in users_db:
        raise HTTPException(status_code=401, detail="User not found")
    
    return users_db[user_id]

@router.post("/signup")
async def signup(user_data: UserSignup):
    # Check if user already exists
    for user_id, user in users_db.items():
        if user["email"] == user_data.email:
            raise HTTPException(status_code=400, detail="User already exists")
    
    # Create new user
    user_id = str(uuid.uuid4())
    hashed_password = hash_password(user_data.password)
    
    users_db[user_id] = {
        "id": user_id,
        "name": user_data.name,
        "email": user_data.email,
        "password": hashed_password,
        "plan": "free",
        "joined_date": datetime.utcnow().isoformat(),
        "newsletter_subscribed": user_data.newsletter
    }
    
    user_stats[user_id] = {
        "datasets_processed": 0,
        "total_storage_used": 0
    }
    
    # Create token
    token = create_token(user_id, user_data.email)
    
    return {
        "success": True,
        "token": token,
        "user": {
            "id": user_id,
            "name": user_data.name,
            "email": user_data.email,
            "plan": "free",
            "joined_date": users_db[user_id]["joined_date"],
            "datasets_processed": 0,
            "total_storage_used": 0,
            "newsletter_subscribed": user_data.newsletter
        }
    }

@router.post("/login")
async def login(user_data: UserLogin):
    # Find user by email
    user = None
    for user_id, u in users_db.items():
        if u["email"] == user_data.email:
            user = u
            break
    
    if not user or not verify_password(user_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create token
    token = create_token(user["id"], user["email"])
    
    stats = user_stats.get(user["id"], {"datasets_processed": 0, "total_storage_used": 0})
    
    return {
        "success": True,
        "token": token,
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "plan": user["plan"],
            "joined_date": user["joined_date"],
            "datasets_processed": stats["datasets_processed"],
            "total_storage_used": stats["total_storage_used"],
            "newsletter_subscribed": user["newsletter_subscribed"]
        }
    }

@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    stats = user_stats.get(current_user["id"], {"datasets_processed": 0, "total_storage_used": 0})
    
    return {
        "success": True,
        "user": {
            "id": current_user["id"],
            "name": current_user["name"],
            "email": current_user["email"],
            "plan": current_user["plan"],
            "joined_date": current_user["joined_date"],
            "datasets_processed": stats["datasets_processed"],
            "total_storage_used": stats["total_storage_used"],
            "newsletter_subscribed": current_user["newsletter_subscribed"]
        }
    }

@router.get("/google")
async def google_auth():
    # This would redirect to Google OAuth
    # For now, return a mock response
    return {"message": "Google OAuth would redirect here"}

# Helper function to update user stats (to be called from main.py)
def update_user_stats(user_id: str, dataset_size: int):
    if user_id in user_stats:
        user_stats[user_id]["datasets_processed"] += 1
        user_stats[user_id]["total_storage_used"] += dataset_size
    else:
        user_stats[user_id] = {
            "datasets_processed": 1,
            "total_storage_used": dataset_size
        }