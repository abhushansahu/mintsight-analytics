"""Load seed entity data from seed/entities.json into the database."""

from __future__ import annotations

import asyncio
import json
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import async_session
from app.models.entity import Entity, EntityLabel

SEED_FILE = Path(__file__).parent.parent / "seed" / "entities.json"


async def load_seed_entities(db: AsyncSession) -> tuple[int, int]:
    """Load seed entities and their wallet labels. Returns (entities_created, labels_created)."""
    with open(SEED_FILE) as f:
        seed_data = json.load(f)

    entities_created = 0
    labels_created = 0

    for item in seed_data:
        existing = await db.execute(select(Entity).where(Entity.slug == item["slug"]))
        entity = existing.scalar_one_or_none()

        if not entity:
            entity = Entity(
                name=item["name"],
                slug=item["slug"],
                category=item["category"],
                subcategory=item.get("subcategory"),
                website=item.get("website"),
                description=item.get("description"),
            )
            db.add(entity)
            await db.flush()
            entities_created += 1

        for wallet in item.get("wallets", []):
            existing_label = await db.execute(
                select(EntityLabel).where(
                    EntityLabel.wallet_address == wallet,
                    EntityLabel.entity_id == entity.id,
                )
            )
            if not existing_label.scalar_one_or_none():
                label = EntityLabel(
                    wallet_address=wallet,
                    entity_id=entity.id,
                    label_type="manual",
                    confidence=1.0,
                    source="seed",
                )
                db.add(label)
                labels_created += 1

    await db.commit()
    return entities_created, labels_created


async def main():
    async with async_session() as db:
        entities, labels = await load_seed_entities(db)
        print(f"Seeded {entities} entities and {labels} wallet labels.")


if __name__ == "__main__":
    asyncio.run(main())
