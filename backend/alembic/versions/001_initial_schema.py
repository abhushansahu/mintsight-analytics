"""Initial schema: transactions, entities, entity_labels, enriched_transactions

Revision ID: 001
Revises: None
Create Date: 2026-04-06
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;")

    op.create_table(
        "transactions",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("signature", sa.Text, nullable=False),
        sa.Column("block_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("slot", sa.BigInteger, nullable=False),
        sa.Column("source_wallet", sa.Text, nullable=False),
        sa.Column("destination_wallet", sa.Text, nullable=False),
        sa.Column("mint", sa.Text, nullable=False),
        sa.Column("amount", sa.Numeric, nullable=False),
        sa.Column("decimals", sa.Integer, nullable=False, server_default="0"),
        sa.Column("program_id", sa.Text, nullable=True),
        sa.Column("instruction_type", sa.Text, nullable=True),
        sa.Column("raw_data", JSONB, nullable=True),
    )
    op.create_index("ix_transactions_signature", "transactions", ["signature"])
    op.create_index("ix_transactions_block_time", "transactions", ["block_time"])
    op.create_index("ix_transactions_source_wallet", "transactions", ["source_wallet"])
    op.create_index("ix_transactions_destination_wallet", "transactions", ["destination_wallet"])
    op.create_index("ix_transactions_mint", "transactions", ["mint"])

    # TimescaleDB hypertable for time-series queries
    op.execute(
        "SELECT create_hypertable('transactions', 'block_time', "
        "migrate_data => true, if_not_exists => true);"
    )

    op.create_table(
        "entities",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.Text, nullable=False),
        sa.Column("slug", sa.Text, nullable=False),
        sa.Column("category", sa.Text, nullable=False),
        sa.Column("subcategory", sa.Text, nullable=True),
        sa.Column("website", sa.Text, nullable=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("metadata", JSONB, nullable=True),
    )
    op.create_index("ix_entities_slug", "entities", ["slug"], unique=True)

    op.create_table(
        "entity_labels",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("wallet_address", sa.Text, nullable=False),
        sa.Column("entity_id", sa.Integer, sa.ForeignKey("entities.id"), nullable=False),
        sa.Column("label_type", sa.Text, nullable=False, server_default="manual"),
        sa.Column("confidence", sa.Float, nullable=False, server_default="1.0"),
        sa.Column("source", sa.Text, nullable=True),
        sa.UniqueConstraint("wallet_address", "entity_id", name="uq_label_wallet_entity"),
    )
    op.create_index("ix_entity_labels_wallet_address", "entity_labels", ["wallet_address"])
    op.create_index("ix_entity_labels_entity_id", "entity_labels", ["entity_id"])

    op.create_table(
        "enriched_transactions",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column(
            "transaction_id",
            sa.BigInteger,
            sa.ForeignKey("transactions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("source_entity_id", sa.Integer, sa.ForeignKey("entities.id"), nullable=True),
        sa.Column("dest_entity_id", sa.Integer, sa.ForeignKey("entities.id"), nullable=True),
        sa.Column("source_category", sa.Text, nullable=True),
        sa.Column("dest_category", sa.Text, nullable=True),
        sa.Column("token_symbol", sa.Text, nullable=True),
        sa.Column("usd_amount", sa.Numeric, nullable=True),
        sa.Column("commerce_type", sa.Text, nullable=False, server_default="unknown"),
    )
    op.create_index("ix_enriched_transaction_id", "enriched_transactions", ["transaction_id"], unique=True)


def downgrade() -> None:
    op.drop_table("enriched_transactions")
    op.drop_table("entity_labels")
    op.drop_table("entities")
    op.drop_table("transactions")
