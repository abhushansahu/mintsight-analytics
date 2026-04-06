from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models.enrichment import EnrichedTransaction
from app.models.entity import Entity
from app.models.transaction import Transaction
from app.schemas.analytics import (
    CategoryBreakdownItem,
    CommerceFlowItem,
    TopMerchant,
    VolumePoint,
    VolumeResponse,
)
from app.services.analytics import get_overview_stats

router = APIRouter()


@router.get("/overview")
async def overview(db: AsyncSession = Depends(get_db)):
    return await get_overview_stats(db)


TRUNC_MAP = {"1h": "hour", "1d": "day", "1w": "week"}
PERIOD_MAP = {"7d": "7 days", "30d": "30 days", "90d": "90 days", "1y": "365 days"}


def _period_filter(period: str):
    pg = PERIOD_MAP.get(period, "30 days")
    return Transaction.block_time >= text(f"now() - interval '{pg}'")


@router.get("/volume", response_model=VolumeResponse)
async def volume(
    group_by: str = Query("total", enum=["total", "entity", "category", "token"]),
    interval: str = Query("1d", enum=["1h", "1d", "1w"]),
    period: str = Query("30d"),
    db: AsyncSession = Depends(get_db),
):
    trunc = TRUNC_MAP[interval]
    bucket = func.date_trunc(trunc, Transaction.block_time).label("timestamp")

    stmt = (
        select(
            bucket,
            func.coalesce(func.sum(EnrichedTransaction.usd_amount), 0).label("volume_usd"),
            func.count(Transaction.id).label("transaction_count"),
        )
        .join(EnrichedTransaction, EnrichedTransaction.transaction_id == Transaction.id)
        .where(_period_filter(period))
        .group_by(bucket)
        .order_by(bucket)
    )

    result = await db.execute(stmt)
    data = [VolumePoint(**dict(r._mapping)) for r in result.all()]
    return VolumeResponse(group=group_by, interval=interval, data=data)


@router.get("/top-merchants", response_model=list[TopMerchant])
async def top_merchants(
    period: str = Query("30d"),
    limit: int = Query(20, le=100),
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(
            Entity.slug.label("entity_slug"),
            Entity.name.label("entity_name"),
            Entity.category,
            func.coalesce(func.sum(EnrichedTransaction.usd_amount), 0).label("volume_usd"),
            func.count(EnrichedTransaction.id).label("transaction_count"),
        )
        .join(Entity, Entity.id == EnrichedTransaction.dest_entity_id)
        .join(Transaction, Transaction.id == EnrichedTransaction.transaction_id)
        .where(_period_filter(period))
        .group_by(Entity.slug, Entity.name, Entity.category)
        .order_by(func.sum(EnrichedTransaction.usd_amount).desc())
        .limit(limit)
    )
    result = await db.execute(stmt)
    return [TopMerchant(**dict(r._mapping)) for r in result.all()]


@router.get("/commerce-flow", response_model=list[CommerceFlowItem])
async def commerce_flow(
    period: str = Query("30d"),
    db: AsyncSession = Depends(get_db),
):
    total_sub = (
        select(func.coalesce(func.sum(EnrichedTransaction.usd_amount), 1))
        .join(Transaction, Transaction.id == EnrichedTransaction.transaction_id)
        .where(_period_filter(period))
        .scalar_subquery()
    )

    stmt = (
        select(
            EnrichedTransaction.commerce_type,
            func.coalesce(func.sum(EnrichedTransaction.usd_amount), 0).label("volume_usd"),
            func.count(EnrichedTransaction.id).label("transaction_count"),
            (func.coalesce(func.sum(EnrichedTransaction.usd_amount), 0) / total_sub * 100).label(
                "percentage"
            ),
        )
        .join(Transaction, Transaction.id == EnrichedTransaction.transaction_id)
        .where(_period_filter(period))
        .group_by(EnrichedTransaction.commerce_type)
        .order_by(func.sum(EnrichedTransaction.usd_amount).desc())
    )
    result = await db.execute(stmt)
    return [CommerceFlowItem(**dict(r._mapping)) for r in result.all()]


@router.get("/category-breakdown", response_model=list[CategoryBreakdownItem])
async def category_breakdown(
    period: str = Query("30d"),
    db: AsyncSession = Depends(get_db),
):
    total_sub = (
        select(func.coalesce(func.sum(EnrichedTransaction.usd_amount), 1))
        .join(Transaction, Transaction.id == EnrichedTransaction.transaction_id)
        .where(_period_filter(period))
        .scalar_subquery()
    )

    stmt = (
        select(
            EnrichedTransaction.dest_category.label("category"),
            func.coalesce(func.sum(EnrichedTransaction.usd_amount), 0).label("volume_usd"),
            func.count(EnrichedTransaction.id).label("transaction_count"),
            (func.coalesce(func.sum(EnrichedTransaction.usd_amount), 0) / total_sub * 100).label(
                "percentage"
            ),
        )
        .join(Transaction, Transaction.id == EnrichedTransaction.transaction_id)
        .where(_period_filter(period))
        .where(EnrichedTransaction.dest_category.isnot(None))
        .group_by(EnrichedTransaction.dest_category)
        .order_by(func.sum(EnrichedTransaction.usd_amount).desc())
    )
    result = await db.execute(stmt)
    return [CategoryBreakdownItem(**dict(r._mapping)) for r in result.all()]
