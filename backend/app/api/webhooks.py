from fastapi import APIRouter, Depends, Request, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
import hmac
import hashlib

from app.db import get_db
from app.ingestion.helius import process_helius_webhook
from app.services.enrichment import enrich_pending
from app.config import settings
from app.schemas.webhook import HeliusWebhookPayload

router = APIRouter()


async def verify_helius_signature(request: Request):
    if not settings.helius_webhook_secret:
        raise HTTPException(status_code=500, detail="Webhook secret not configured")
    
    body = await request.body()
    signature = request.headers.get("x-helius-signature")
    if not signature:
        raise HTTPException(status_code=401, detail="Missing signature")
    
    expected_signature = hmac.new(
        settings.helius_webhook_secret.encode(),
        body,
        hashlib.sha256
    ).hexdigest()
    
    if not hmac.compare_digest(signature, expected_signature):
        raise HTTPException(status_code=401, detail="Invalid signature")


async def verify_api_key(x_api_key: str = Header(None)):
    if not x_api_key or x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")


@router.post("/helius")
async def helius_webhook(
    payload: HeliusWebhookPayload,
    request: Request,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_helius_signature)
):
    # Payload is validated by Pydantic
    payload_dict = payload.model_dump()
    ingested = await process_helius_webhook(payload_dict, db)
    enriched = await enrich_pending(db, batch_size=ingested or 100)
    return {"ingested": ingested, "enriched": enriched}


@router.post("/enrich")
async def trigger_enrichment(
    batch_size: int = 500,
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_api_key),
):
    """Manually trigger enrichment of unenriched transactions."""
    count = await enrich_pending(db, batch_size=batch_size)
    return {"enriched": count}


@router.post("/seed")
async def seed_entities(
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_api_key),
):
    """Load seed entity data into the database."""
    from app.seed_loader import load_seed_entities
    entities, labels = await load_seed_entities(db)
    return {"entities_created": entities, "labels_created": labels}


@router.post("/backfill")
async def trigger_backfill(
    _: None = Depends(verify_api_key),
):
    """Trigger historical backfill from Helius (runs in background)."""
    import asyncio
    from app.backfill import run_backfill
    asyncio.create_task(run_backfill(max_pages=5))
    return {"status": "backfill started in background"}
    _: None = Depends(verify_api_key),
):
    """Manually trigger enrichment of unenriched transactions."""
    count = await enrich_pending(db, batch_size=batch_size)
    return {"enriched": count}


@router.post("/seed")
async def seed_entities(
    db: AsyncSession = Depends(get_db),
    _: None = Depends(verify_api_key),
):
    """Load seed entity data into the database."""
    from app.seed_loader import load_seed_entities
    entities, labels = await load_seed_entities(db)
    return {"entities_created": entities, "labels_created": labels}


@router.post("/backfill")
async def trigger_backfill(
    _: None = Depends(verify_api_key),
):
    """Trigger historical backfill from Helius (runs in background)."""
    import asyncio
    from app.backfill import run_backfill
    asyncio.create_task(run_backfill(max_pages=5))
    return {"status": "backfill started in background"}
