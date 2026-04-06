from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models.enrichment import EnrichedTransaction
from app.models.entity import Entity, EntityLabel
from app.schemas.entity import EntityOut, EntityWithStats

router = APIRouter()


@router.get("", response_model=list[EntityOut])
async def list_entities(
    category: str | None = None,
    search: str | None = None,
    limit: int = Query(50, le=200),
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Entity).order_by(Entity.name).limit(limit).offset(offset)
    if category:
        stmt = stmt.where(Entity.category == category)
    if search:
        stmt = stmt.where(Entity.name.ilike(f"%{search}%"))
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/{slug}", response_model=EntityWithStats)
async def get_entity(slug: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Entity).where(Entity.slug == slug))
    entity = result.scalar_one_or_none()
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")

    vol_stmt = select(
        func.coalesce(func.sum(EnrichedTransaction.usd_amount), 0).label("total_volume_usd"),
        func.count(EnrichedTransaction.id).label("transaction_count"),
    ).where(
        (EnrichedTransaction.source_entity_id == entity.id)
        | (EnrichedTransaction.dest_entity_id == entity.id)
    )
    vol_row = (await db.execute(vol_stmt)).one()

    label_count_stmt = select(func.count(EntityLabel.id)).where(EntityLabel.entity_id == entity.id)
    label_count = (await db.execute(label_count_stmt)).scalar_one()

    return EntityWithStats(
        **EntityOut.model_validate(entity).model_dump(),
        total_volume_usd=vol_row.total_volume_usd,
        transaction_count=vol_row.transaction_count,
        label_count=label_count,
    )
