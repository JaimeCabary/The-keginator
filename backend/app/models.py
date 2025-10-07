# models.py
from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Any, Optional


class DatasetMetadata(BaseModel):
    id: str
    user_id: str
    original_filename: str
    cleaned_filename: str
    dataset_hash: str
    rows_original: int
    rows_cleaned: int
    columns: int
    cleaning_report: Dict[str, Any]
    created_at: datetime
    committed_to_solana: bool = False
    solana_signature: Optional[str] = None


class HistoryResponse(BaseModel):
    user_id: str
    total_datasets: int
    datasets: List[DatasetMetadata]


class VerifyResponse(BaseModel):
    dataset_hash: str
    exists_on_chain: bool
    timestamp: Optional[int]
    verified_at: datetime

