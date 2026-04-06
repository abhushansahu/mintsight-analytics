from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class VolumePoint(BaseModel):
    timestamp: datetime
    volume_usd: Decimal
    transaction_count: int


class VolumeResponse(BaseModel):
    group: str
    interval: str
    data: list[VolumePoint]


class TopMerchant(BaseModel):
    entity_slug: str
    entity_name: str
    category: str
    volume_usd: Decimal
    transaction_count: int


class CommerceFlowItem(BaseModel):
    commerce_type: str
    volume_usd: Decimal
    transaction_count: int
    percentage: float


class CategoryBreakdownItem(BaseModel):
    category: str
    volume_usd: Decimal
    transaction_count: int
    percentage: float
