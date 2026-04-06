# MintSight Analytics — board narrative pack

Board-facing copy for **Solana Payment Intent Analytics**. Keep this file in sync with engineering release notes when the CTO publishes README/CHANGELOG updates for the same ship window.

## Target audiences

1. **Product and infra builders** — teams shipping payments, wallets, or merchant tooling on Solana who need more than raw transaction lists: labeled entities, flow types, and category signals.
2. **Research and ops** — analysts tracing **where volume concentrates**, which merchants and categories matter, and how activity breaks across commerce patterns.
3. **Partners and capital** — stakeholders who want a crisp, defensible story: enrichment pipeline (Helius → Postgres/Timescale → API) plus a dashboard that makes patterns legible without standing up their own warehouse.

## One-line story

**MintSight turns Solana payment activity into entity-level commerce intelligence** — mapped counterparties, B2B/B2C/protocol/exchange-style flows, and spend patterns you can explore in the API and dashboard.

## Positioning blurb (board-ready)

MintSight Analytics is commerce intelligence for the Solana payment economy. Instead of stopping at “transactions,” it **maps addresses to entities**, classifies **how value moves** (B2B, B2C, protocol, exchange), and surfaces **volume, merchants, and categories** through a FastAPI backend and a Next.js dashboard. It is built for teams that want **repeatable enrichment** (webhook ingestion, structured storage, documented REST endpoints) and **human-readable exploration** of what the chain is actually doing in payment terms — not just DEX terms.

## Release notes — dashboard exploration (this window)

Use externally after engineering confirms the branch is merged and deployed.

- **Navigation:** Overview plus dedicated **Entities**, **Categories**, and **Flows** sections in the dashboard shell.
- **Deeper drill-down:** Entity and category pages support focused analysis without losing the main overview (stats, volume chart, merchants, category split, transaction feed, entity explorer).
- **Shareable context:** URL-driven selection where applicable so bookmarks and handoffs preserve the view.
- **Unchanged core value:** Enriched transaction API, overview analytics, and the enrichment story described in the repository README.

## Channel-ready copy

**LinkedIn (short)**  
We are tightening the loop between **Solana payment data** and **decisions**: MintSight enriches flows into entities and commerce patterns — volume, merchants, categories — with an API and dashboard built for operators, not only indexers.

**X / short social**  
MintSight: Solana payments → **entity + flow intelligence**. Dashboard + API for volume, merchants, categories — beyond raw txs.

## Handoff to engineering narrative

Engineering source of truth for the same ship window: [CHANGELOG.md](../CHANGELOG.md) and [README — Engineering visibility](../README.md#engineering-visibility). When you extend **Release notes** here, keep wording consistent with those files.
