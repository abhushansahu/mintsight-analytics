# MintSight Analytics — Solana Payment Intent Analytics

Transaction data enrichment and commerce intelligence for the Solana payment economy. MintSight maps wallet addresses to entities, classifies flows as B2B/B2C/protocol/exchange, and surfaces spending patterns through an API and dashboard.

## Quick Start

```bash
# 1. Copy env file
cp .env.example .env
# Edit .env with your Helius API key

# 2. Start services
docker compose up -d

# 3. Run database migrations
cd backend
pip install -e .
alembic upgrade head

# 4. Seed entity labels
python -m app.seed_loader

# 5. Access
# API:       http://localhost:8000/docs
# Dashboard: http://localhost:3000
```

## Architecture

```
Helius Webhooks → Ingestion (FastAPI) → PostgreSQL/TimescaleDB
                                              ↓
                                     Enrichment Engine
                                              ↓
                                       REST API (FastAPI)
                                              ↓
                                    Dashboard (Next.js)
```

## Tech Stack

- **Backend:** Python 3.12, FastAPI, SQLAlchemy (async), Alembic
- **Database:** PostgreSQL 16 + TimescaleDB
- **Frontend:** Next.js 15, TypeScript, Tailwind CSS, Recharts
- **Data Source:** Helius Enhanced Transactions API (webhooks)
- **Infra:** Docker Compose

## Colosseum-friendly checklist

- **English-first repo**: Docs and code are in English (required in official rules).
- **Open-source**: Includes a permissive `LICENSE` (judging criteria includes open-source and composability).

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/webhooks/helius` | Ingest Helius webhook payloads |
| GET | `/api/transactions` | Query enriched transactions |
| GET | `/api/entities` | List/search entities |
| GET | `/api/entities/{slug}` | Entity profile with stats |
| GET | `/api/analytics/overview` | Dashboard summary stats |
| GET | `/api/analytics/volume` | Volume over time |
| GET | `/api/analytics/top-merchants` | Top merchants by volume |
| GET | `/api/analytics/commerce-flow` | B2B/B2C/protocol breakdown |
| GET | `/api/analytics/category-breakdown` | Spending by category |

## Project Structure

```
backend/           Python/FastAPI backend
  app/
    api/           Route handlers
    ingestion/     Helius webhook parser
    enrichment/    Entity labeling + categorization
    models/        SQLAlchemy models
    schemas/       Pydantic schemas
    services/      Business logic
  seed/            Entity seed data
  alembic/         DB migrations
frontend/          Next.js dashboard
  src/
    components/    Dashboard widgets
    lib/           API client
```
