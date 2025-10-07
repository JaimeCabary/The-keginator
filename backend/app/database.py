# database.py
import asyncpg
import os
from typing import Optional, List
import json

from .models import DatasetMetadata  # UNCOMMENTED - this is the fix!


class Database:
    """
    PostgreSQL database for storing dataset metadata
    """
    
    def __init__(self):
        self.pool = None
        self.db_url = os.getenv(
            "DATABASE_URL",
            "postgresql://keginator:password@localhost:5432/keginator"
        )
    
    async def connect(self):
        """Initialize database connection pool"""
        try:
            self.pool = await asyncpg.create_pool(self.db_url, min_size=1, max_size=10)
            await self._create_tables()
            print("✅ Database connected")
        except Exception as e:
            print(f"⚠️ Database connection failed: {e}")
            print("Using in-memory fallback")
            self.pool = None
    
    async def disconnect(self):
        """Close database connections"""
        if self.pool:
            await self.pool.close()
    
    async def _create_tables(self):
        """Create database tables if they don't exist"""
        if not self.pool:
            return
        
        async with self.pool.acquire() as conn:
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS datasets (
                    id VARCHAR(64) PRIMARY KEY,
                    user_id VARCHAR(128) NOT NULL,
                    original_filename VARCHAR(512),
                    cleaned_filename VARCHAR(512),
                    dataset_hash VARCHAR(64) UNIQUE NOT NULL,
                    rows_original INTEGER,
                    rows_cleaned INTEGER,
                    columns INTEGER,
                    cleaning_report JSONB,
                    created_at TIMESTAMP DEFAULT NOW(),
                    committed_to_solana BOOLEAN DEFAULT FALSE,
                    solana_signature VARCHAR(128)
                );
                
                CREATE INDEX IF NOT EXISTS idx_user_id ON datasets(user_id);
                CREATE INDEX IF NOT EXISTS idx_dataset_hash ON datasets(dataset_hash);
                CREATE INDEX IF NOT EXISTS idx_created_at ON datasets(created_at DESC);
            ''')
    
    async def insert_metadata(self, metadata: DatasetMetadata):
        """Insert dataset metadata"""
        if not self.pool:
            return
        
        async with self.pool.acquire() as conn:
            await conn.execute('''
                INSERT INTO datasets (
                    id, user_id, original_filename, cleaned_filename,
                    dataset_hash, rows_original, rows_cleaned, columns,
                    cleaning_report, created_at, committed_to_solana, solana_signature
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
            ''',
                metadata.id,
                metadata.user_id,
                metadata.original_filename,
                metadata.cleaned_filename,
                metadata.dataset_hash,
                metadata.rows_original,
                metadata.rows_cleaned,
                metadata.columns,
                json.dumps(metadata.cleaning_report),
                metadata.created_at,
                metadata.committed_to_solana,
                metadata.solana_signature
            )
    
    async def get_metadata(self, dataset_id: str) -> Optional[DatasetMetadata]:
        """Get dataset metadata by ID"""
        if not self.pool:
            return None
        
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                'SELECT * FROM datasets WHERE id = $1', dataset_id
            )
            
            if not row:
                return None
            
            return DatasetMetadata(
                id=row['id'],
                user_id=row['user_id'],
                original_filename=row['original_filename'],
                cleaned_filename=row['cleaned_filename'],
                dataset_hash=row['dataset_hash'],
                rows_original=row['rows_original'],
                rows_cleaned=row['rows_cleaned'],
                columns=row['columns'],
                cleaning_report=json.loads(row['cleaning_report']),
                created_at=row['created_at'],
                committed_to_solana=row['committed_to_solana'],
                solana_signature=row['solana_signature']
            )
    
    async def get_user_history(self, user_id: str, limit: int = 50) -> List[DatasetMetadata]:
        """Get user's dataset history"""
        if not self.pool:
            return []
        
        async with self.pool.acquire() as conn:
            rows = await conn.fetch('''
                SELECT * FROM datasets 
                WHERE user_id = $1 
                ORDER BY created_at DESC 
                LIMIT $2
            ''', user_id, limit)
            
            return [
                DatasetMetadata(
                    id=row['id'],
                    user_id=row['user_id'],
                    original_filename=row['original_filename'],
                    cleaned_filename=row['cleaned_filename'],
                    dataset_hash=row['dataset_hash'],
                    rows_original=row['rows_original'],
                    rows_cleaned=row['rows_cleaned'],
                    columns=row['columns'],
                    cleaning_report=json.loads(row['cleaning_report']),
                    created_at=row['created_at'],
                    committed_to_solana=row['committed_to_solana'],
                    solana_signature=row['solana_signature']
                )
                for row in rows
            ]
    
    async def update_solana_status(
        self, 
        dataset_id: str, 
        committed: bool, 
        signature: str
    ):
        """Update Solana commitment status"""
        if not self.pool:
            return
        
        async with self.pool.acquire() as conn:
            await conn.execute('''
                UPDATE datasets 
                SET committed_to_solana = $1, solana_signature = $2
                WHERE id = $3
            ''', committed, signature, dataset_id)