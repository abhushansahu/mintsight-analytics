"""Entity label matching — looks up wallet addresses against the entity_labels table."""

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.entity import Entity, EntityLabel


@dataclass
class LabelMatch:
    entity_id: int
    entity_name: str
    category: str
    confidence: float


async def lookup_wallet(wallet: str, db: AsyncSession) -> LabelMatch | None:
    """Find the best entity match for a wallet address."""
    stmt = (
        select(EntityLabel, Entity)
        .join(Entity, Entity.id == EntityLabel.entity_id)
        .where(EntityLabel.wallet_address == wallet)
        .order_by(EntityLabel.confidence.desc())
        .limit(1)
    )
    result = await db.execute(stmt)
    row = result.first()
    if not row:
        return None

    label, entity = row
    return LabelMatch(
        entity_id=entity.id,
        entity_name=entity.name,
        category=entity.category,
        confidence=label.confidence,
    )


async def build_wallet_cache(db: AsyncSession) -> dict[str, LabelMatch]:
    """Pre-load all wallet→entity mappings into memory for batch enrichment."""
    stmt = (
        select(EntityLabel, Entity)
        .join(Entity, Entity.id == EntityLabel.entity_id)
        .order_by(EntityLabel.confidence.desc())
    )
    result = await db.execute(stmt)
    cache: dict[str, LabelMatch] = {}
    for label, entity in result.all():
        if label.wallet_address not in cache:
            cache[label.wallet_address] = LabelMatch(
                entity_id=entity.id,
                entity_name=entity.name,
                category=entity.category,
                confidence=label.confidence,
            )
    return cache
