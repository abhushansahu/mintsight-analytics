from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class TransactionOut(BaseModel):
    id: int
    signature: str
    block_time: datetime
    slot: int
    source_wallet: str
    destination_wallet: str
    mint: str
    amount: Decimal
    decimals: int
    program_id: str | None = None
    instruction_type: str | None = None

    model_config = {"from_attributes": True}


class EnrichedTransactionOut(BaseModel):
    id: int
    signature: str
    block_time: datetime
    source_wallet: str
    destination_wallet: str
    mint: str
    amount: Decimal
    token_symbol: str | None = None
    usd_amount: Decimal | None = None
    source_entity: str | None = None
    dest_entity: str | None = None
    source_category: str | None = None
    dest_category: str | None = None
    commerce_type: str = "unknown"

    model_config = {"from_attributes": True}
