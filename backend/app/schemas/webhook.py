from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class HeliusTransaction(BaseModel):
    signature: str
    blockTime: Optional[int]
    slot: int
    # Add other fields as needed, but keep flexible
    tokenTransfers: Optional[List[Dict[str, Any]]] = []
    nativeTransfers: Optional[List[Dict[str, Any]]] = []


class HeliusWebhookPayload(BaseModel):
    data: Optional[List[HeliusTransaction]] = []
    transactions: Optional[List[HeliusTransaction]] = []