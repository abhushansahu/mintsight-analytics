import sqlalchemy as sa

from app.models import Base


class EnrichedTransaction(Base):
    __tablename__ = "enriched_transactions"

    id = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True)
    transaction_id = sa.Column(
        sa.BigInteger, sa.ForeignKey("transactions.id", ondelete="CASCADE"),
        nullable=False, unique=True, index=True,
    )
    source_entity_id = sa.Column(sa.Integer, sa.ForeignKey("entities.id"), nullable=True)
    dest_entity_id = sa.Column(sa.Integer, sa.ForeignKey("entities.id"), nullable=True)
    source_category = sa.Column(sa.Text, nullable=True)
    dest_category = sa.Column(sa.Text, nullable=True)
    token_symbol = sa.Column(sa.Text, nullable=True)
    usd_amount = sa.Column(sa.Numeric, nullable=True)
    commerce_type = sa.Column(sa.Text, nullable=False, default="unknown")
