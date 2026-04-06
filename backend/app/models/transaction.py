import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

from app.models import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True)
    signature = sa.Column(sa.Text, nullable=False, index=True)
    block_time = sa.Column(sa.DateTime(timezone=True), nullable=False, index=True)
    slot = sa.Column(sa.BigInteger, nullable=False)

    source_wallet = sa.Column(sa.Text, nullable=False, index=True)
    destination_wallet = sa.Column(sa.Text, nullable=False, index=True)

    mint = sa.Column(sa.Text, nullable=False, index=True)
    amount = sa.Column(sa.Numeric, nullable=False)
    decimals = sa.Column(sa.Integer, nullable=False, default=0)

    program_id = sa.Column(sa.Text, nullable=True)
    instruction_type = sa.Column(sa.Text, nullable=True)

    raw_data = sa.Column(JSONB, nullable=True)
