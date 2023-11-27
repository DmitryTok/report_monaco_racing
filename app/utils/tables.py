from app.db.models.base import Base
from app.db.session import s


def create_tables() -> None:
    assert s.pg_db.bind
    Base.metadata.create_all(s.pg_db.bind)
