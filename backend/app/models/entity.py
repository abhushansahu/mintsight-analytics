import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

from app.models import Base


class Entity(Base):
    __tablename__ = "entities"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.Text, nullable=False)
    slug = sa.Column(sa.Text, unique=True, nullable=False, index=True)
    category = sa.Column(sa.Text, nullable=False)
    subcategory = sa.Column(sa.Text, nullable=True)
    website = sa.Column(sa.Text, nullable=True)
    description = sa.Column(sa.Text, nullable=True)
    metadata_ = sa.Column("metadata", JSONB, nullable=True)


class EntityLabel(Base):
    __tablename__ = "entity_labels"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    wallet_address = sa.Column(sa.Text, nullable=False, index=True)
    entity_id = sa.Column(sa.Integer, sa.ForeignKey("entities.id"), nullable=False, index=True)
    label_type = sa.Column(sa.Text, nullable=False, default="manual")
    confidence = sa.Column(sa.Float, nullable=False, default=1.0)
    source = sa.Column(sa.Text, nullable=True)

    __table_args__ = (
        sa.UniqueConstraint("wallet_address", "entity_id", name="uq_label_wallet_entity"),
    )
