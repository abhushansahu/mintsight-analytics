from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models.enrichment import EnrichedTransaction
from app.models.entity import Entity
from app.models.transaction import Transaction
from app.schemas.transaction import EnrichedTransactionOut

router = APIRouter()


@router.get("", response_model=list[EnrichedTransactionOut])
async def list_transactions(
    wallet: str | None = None,
    mint: str | None = None,
    from_date: datetime | None = Query(None, alias="from"),
    to_date: datetime | None = Query(None, alias="to"),
    commerce_type: str | None = None,
    limit: int = Query(50, le=500),
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    src_entity = Entity.__table__.alias("src_entity")
    dst_entity = Entity.__table__.alias("dst_entity")

    stmt = (
        select(
            Transaction.id,
            Transaction.signature,
            Transaction.block_time,
            Transaction.source_wallet,
            Transaction.destination_wallet,
            Transaction.mint,
            Transaction.amount,
            EnrichedTransaction.token_symbol,
            EnrichedTransaction.usd_amount,
            src_entity.c.name.label("source_entity"),
            dst_entity.c.name.label("dest_entity"),
            EnrichedTransaction.source_category,
            EnrichedTransaction.dest_category,
            EnrichedTransaction.commerce_type,
        )
        .outerjoin(EnrichedTransaction, EnrichedTransaction.transaction_id == Transaction.id)
        .outerjoin(src_entity, src_entity.c.id == EnrichedTransaction.source_entity_id)
        .outerjoin(dst_entity, dst_entity.c.id == EnrichedTransaction.dest_entity_id)
        .order_by(Transaction.block_time.desc())
        .limit(limit)
        .offset(offset)
    )

    if wallet:
        stmt = stmt.where(
            (Transaction.source_wallet == wallet) | (Transaction.destination_wallet == wallet)
        )
    if mint:
        stmt = stmt.where(Transaction.mint == mint)
    if from_date:
        stmt = stmt.where(Transaction.block_time >= from_date)
    if to_date:
        stmt = stmt.where(Transaction.block_time <= to_date)
    if commerce_type:
        stmt = stmt.where(EnrichedTransaction.commerce_type == commerce_type)

    result = await db.execute(stmt)
    rows = result.all()
    return [EnrichedTransactionOut.model_validate(dict(row._mapping)) for row in rows]


@router.get("/count")
async def transaction_count(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(func.count(Transaction.id)))
    return {"count": result.scalar_one()}
