from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import analytics, entities, transactions, webhooks
from app.config import settings

app = FastAPI(
    title="MintSight Analytics",
    description="MintSight Analytics — Solana payment intent analytics and transaction enrichment API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(webhooks.router, prefix="/api/webhooks", tags=["webhooks"])
app.include_router(transactions.router, prefix="/api/transactions", tags=["transactions"])
app.include_router(entities.router, prefix="/api/entities", tags=["entities"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])


@app.get("/health")
async def health():
    return {"status": "ok"}
