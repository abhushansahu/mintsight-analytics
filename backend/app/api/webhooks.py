from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.ingestion.helius import process_helius_webhook
from app.services.enrichment import enrich_pending

router = APIRouter()


@router.post("/helius")
async def helius_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    payload = await request.json()
    ingested = await process_helius_webhook(payload, db)
    enriched = await enrich_pending(db, batch_size=ingested or 100)
    return {"ingested": ingested, "enriched": enriched}


@router.post("/enrich")
async def trigger_enrichment(
    batch_size: int = 500,
    db: AsyncSession = Depends(get_db),
):
    """Manually trigger enrichment of unenriched transactions."""
    count = await enrich_pending(db, batch_size=batch_size)
    return {"enriched": count}


@router.post("/seed")
async def seed_entities(db: AsyncSession = Depends(get_db)):
    """Load seed entity data into the database."""
    from app.seed_loader import load_seed_entities
    entities, labels = await load_seed_entities(db)
    return {"entities_created": entities, "labels_created": labels}


@router.post("/backfill")
async def trigger_backfill():
    """Trigger historical backfill from Helius (runs in background)."""
    import asyncio
    from app.backfill import run_backfill
    asyncio.create_task(run_backfill(max_pages=5))
    return {"status": "backfill started in background"}
