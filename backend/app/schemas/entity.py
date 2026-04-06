from decimal import Decimal

from pydantic import BaseModel


class EntityOut(BaseModel):
    id: int
    name: str
    slug: str
    category: str
    subcategory: str | None = None
    website: str | None = None
    description: str | None = None

    model_config = {"from_attributes": True}


class EntityWithStats(EntityOut):
    total_volume_usd: Decimal | None = None
    transaction_count: int = 0
    label_count: int = 0
