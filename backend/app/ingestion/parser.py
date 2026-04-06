"""Parse Helius enhanced transaction payloads into normalized SPL transfer records."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any


@dataclass
class ParsedTransfer:
    signature: str
    block_time: datetime
    slot: int
    source_wallet: str
    destination_wallet: str
    mint: str
    amount: Decimal
    decimals: int
    program_id: str | None
    instruction_type: str | None
    raw_data: dict[str, Any] | None


def parse_enhanced_transaction(tx: dict[str, Any]) -> list[ParsedTransfer]:
    """Extract SPL token transfers from a Helius enhanced transaction payload."""
    transfers: list[ParsedTransfer] = []
    signature = tx.get("signature", "")
    timestamp = tx.get("timestamp")
    slot = tx.get("slot", 0)

    if timestamp:
        block_time = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    else:
        block_time = datetime.now(tz=timezone.utc)

    for transfer in tx.get("tokenTransfers", []):
        source = transfer.get("fromUserAccount") or transfer.get("fromTokenAccount", "")
        dest = transfer.get("toUserAccount") or transfer.get("toTokenAccount", "")
        mint = transfer.get("mint", "")
        raw_amount = transfer.get("tokenAmount", 0)

        if not source or not dest or not mint:
            continue

        transfers.append(
            ParsedTransfer(
                signature=signature,
                block_time=block_time,
                slot=slot,
                source_wallet=source,
                destination_wallet=dest,
                mint=mint,
                amount=Decimal(str(raw_amount)),
                decimals=transfer.get("decimals", 0) if "decimals" in transfer else 0,
                program_id=transfer.get("programId"),
                instruction_type=tx.get("type"),
                raw_data=None,
            )
        )

    for transfer in tx.get("nativeTransfers", []):
        source = transfer.get("fromUserAccount", "")
        dest = transfer.get("toUserAccount", "")
        lamports = transfer.get("amount", 0)
        if not source or not dest or lamports == 0:
            continue

        transfers.append(
            ParsedTransfer(
                signature=signature,
                block_time=block_time,
                slot=slot,
                source_wallet=source,
                destination_wallet=dest,
                mint="So11111111111111111111111111111111",
                amount=Decimal(str(lamports)) / Decimal("1000000000"),
                decimals=9,
                program_id="11111111111111111111111111111111",
                instruction_type=tx.get("type"),
                raw_data=None,
            )
        )

    return transfers
