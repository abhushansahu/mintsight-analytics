"""Analytics service — high-level query helpers."""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enrichment import EnrichedTransaction
from app.models.entity import Entity
from app.models.transaction import Transaction


async def get_overview_stats(db: AsyncSession) -> dict:
    tx_count = (await db.execute(select(func.count(Transaction.id)))).scalar_one()
    enriched_count = (await db.execute(select(func.count(EnrichedTransaction.id)))).scalar_one()
    entity_count = (await db.execute(select(func.count(Entity.id)))).scalar_one()
    total_volume = (
        await db.execute(select(func.coalesce(func.sum(EnrichedTransaction.usd_amount), 0)))
    ).scalar_one()

    return {
        "total_transactions": tx_count,
        "enriched_transactions": enriched_count,
        "total_entities": entity_count,
        "total_volume_usd": float(total_volume),
    }
