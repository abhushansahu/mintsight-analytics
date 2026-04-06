"""Process Helius webhook payloads and persist parsed transfers."""

from __future__ import annotations

from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.ingestion.parser import ParsedTransfer, parse_enhanced_transaction
from app.models.transaction import Transaction


async def process_helius_webhook(payload: Any, db: AsyncSession) -> int:
    """Ingest a Helius webhook payload (list of enhanced transactions).

    Returns the number of transfers persisted.
    """
    if isinstance(payload, dict):
        txs = payload.get("data", payload.get("transactions", [payload]))
        if not isinstance(txs, list):
            txs = [payload]
    elif isinstance(payload, list):
        txs = payload
    else:
        return 0

    all_transfers: list[ParsedTransfer] = []
    for tx in txs:
        all_transfers.extend(parse_enhanced_transaction(tx))

    if not all_transfers:
        return 0

    persisted = 0
    for t in all_transfers:
        exists = await db.execute(
            text("SELECT 1 FROM transactions WHERE signature = :sig AND source_wallet = :src AND destination_wallet = :dst LIMIT 1"),
            {"sig": t.signature, "src": t.source_wallet, "dst": t.destination_wallet},
        )
        if exists.scalar_one_or_none():
            continue

        row = Transaction(
            signature=t.signature,
            block_time=t.block_time,
            slot=t.slot,
            source_wallet=t.source_wallet,
            destination_wallet=t.destination_wallet,
            mint=t.mint,
            amount=t.amount,
            decimals=t.decimals,
            program_id=t.program_id,
            instruction_type=t.instruction_type,
            raw_data=t.raw_data,
        )
        db.add(row)
        persisted += 1

    await db.commit()
    return persisted
