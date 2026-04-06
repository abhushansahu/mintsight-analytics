from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


from app.models.entity import Entity, EntityLabel  # noqa: E402, F401
from app.models.transaction import Transaction  # noqa: E402, F401
from app.models.enrichment import EnrichedTransaction  # noqa: E402, F401
