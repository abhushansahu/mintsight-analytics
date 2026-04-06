"""Batch enrichment service — enriches unenriched transactions."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.enrichment.categorizer import classify_commerce_type, resolve_token_symbol
from app.enrichment.labeler import LabelMatch, build_wallet_cache
from app.models.enrichment import EnrichedTransaction
from app.models.transaction import Transaction


async def enrich_pending(db: AsyncSession, batch_size: int = 500) -> int:
    """Enrich transactions that don't yet have an enriched_transactions row."""
    cache = await build_wallet_cache(db)

    stmt = (
        select(Transaction)
        .outerjoin(EnrichedTransaction, EnrichedTransaction.transaction_id == Transaction.id)
        .where(EnrichedTransaction.id.is_(None))
        .order_by(Transaction.block_time.desc())
        .limit(batch_size)
    )
    result = await db.execute(stmt)
    transactions = result.scalars().all()

    if not transactions:
        return 0

    count = 0
    for tx in transactions:
        src_label: LabelMatch | None = cache.get(tx.source_wallet)
        dst_label: LabelMatch | None = cache.get(tx.destination_wallet)

        commerce_type = classify_commerce_type(src_label, dst_label)
        token_symbol = resolve_token_symbol(tx.mint)

        enriched = EnrichedTransaction(
            transaction_id=tx.id,
            source_entity_id=src_label.entity_id if src_label else None,
            dest_entity_id=dst_label.entity_id if dst_label else None,
            source_category=src_label.category if src_label else None,
            dest_category=dst_label.category if dst_label else None,
            token_symbol=token_symbol,
            usd_amount=tx.amount if token_symbol in ("USDC", "USDT", "USDS", "PYUSD") else None,
            commerce_type=commerce_type,
        )
        db.add(enriched)
        count += 1

    await db.commit()
    return count
