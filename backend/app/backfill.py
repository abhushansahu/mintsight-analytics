"""Historical backfill — fetch recent transactions from Helius and ingest them."""

from __future__ import annotations

import asyncio
import logging

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db import async_session
from app.ingestion.helius import process_helius_webhook
from app.services.enrichment import enrich_pending

logger = logging.getLogger(__name__)

HELIUS_BASE = "https://api.helius.xyz/v0"

USDC_MINT = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
USDT_MINT = "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB"

TRACKED_ACCOUNTS = [
    USDC_MINT,
    USDT_MINT,
]


async def fetch_address_transactions(
    client: httpx.AsyncClient,
    address: str,
    limit: int = 100,
    before: str | None = None,
) -> list[dict]:
    """Fetch enhanced transactions for an address from Helius."""
    params: dict = {"api-key": settings.helius_api_key}
    if before:
        params["before"] = before

    url = f"{HELIUS_BASE}/addresses/{address}/transactions"
    resp = await client.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


async def backfill_address(
    address: str,
    max_pages: int = 5,
    page_size: int = 100,
) -> int:
    """Backfill transactions for a single address."""
    total_ingested = 0
    before = None

    async with httpx.AsyncClient() as client:
        for page in range(max_pages):
            logger.info(f"Backfill page {page + 1} for {address[:8]}...")
            try:
                txs = await fetch_address_transactions(client, address, page_size, before)
            except httpx.HTTPStatusError as e:
                logger.error(f"Helius API error: {e}")
                break

            if not txs:
                break

            async with async_session() as db:
                ingested = await process_helius_webhook(txs, db)
                total_ingested += ingested
                logger.info(f"  Ingested {ingested} transfers from {len(txs)} transactions")

            before = txs[-1].get("signature")
            if len(txs) < page_size:
                break

            await asyncio.sleep(0.5)

    return total_ingested


async def run_backfill(max_pages: int = 5):
    """Run backfill for all tracked accounts, then enrich."""
    if not settings.helius_api_key:
        logger.error("HELIUS_API_KEY not set. Cannot backfill.")
        return

    total = 0
    for address in TRACKED_ACCOUNTS:
        logger.info(f"Backfilling {address[:8]}...")
        count = await backfill_address(address, max_pages=max_pages)
        total += count
        logger.info(f"  Total from {address[:8]}: {count}")

    logger.info(f"Backfill complete. {total} transfers ingested.")

    async with async_session() as db:
        enriched = await enrich_pending(db, batch_size=2000)
        logger.info(f"Enriched {enriched} transactions.")


async def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    await run_backfill(max_pages=10)


if __name__ == "__main__":
    asyncio.run(main())
