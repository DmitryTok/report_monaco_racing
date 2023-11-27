from sqlalchemy import select

from app.db.models import Driver
from app.db.session import pop_session, s, set_session


def test_client_creation(client):
    assert client


def test_db():
    set_session()
    assert len(s.pg_db.scalars(select(Driver)).all()) == 5
    pop_session()
