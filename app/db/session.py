import dataclasses
import typing
from contextvars import ContextVar

from sqlalchemy import Engine, create_engine, select
from sqlalchemy.orm import Session, SessionTransaction, sessionmaker

from app.constants import DB_BASE_URL, DB_NAME, ECHO_OPTIONS


@dataclasses.dataclass
class SessionPool:
    engine: Engine
    maker: sessionmaker


ses_pools: dict[str, SessionPool] = {}


pg_db = ContextVar[Session]('pg_db')
pg_db_transaction = ContextVar[SessionTransaction | None](
    'pg_db_transaction', default=None
)


class SessionException(Exception):
    pass


def get_pool_sync(db_url: str, options: dict[str, typing.Any]) -> SessionPool:
    db_statement = ses_pools.get(db_url)
    if not db_statement:
        auto_engine = create_engine(db_url, **options)
        check_connection(auto_engine)
        auto_maker = _create_sessionmaker(auto_engine)

        db_statement = SessionPool(
            engine=auto_engine,
            maker=auto_maker,
        )
        ses_pools[db_url] = db_statement

    return db_statement


def _create_sessionmaker(engine: Engine) -> sessionmaker:
    return sessionmaker(
        bind=engine,
        expire_on_commit=False,
        future=True,
    )


def check_connection(engine: Engine) -> None:
    try:
        with engine.connect() as conn:
            conn.execute(select(1))
    except Exception as ex:
        raise SessionException(ex)


def close_dbs() -> None:
    for ses_pool in ses_pools.values():
        ses_pool.engine.dispose()


def set_session() -> None:
    current_pool = get_pool_sync(f'{DB_BASE_URL}/{DB_NAME}', ECHO_OPTIONS)
    s.pg_db = current_pool.maker()
    s.pg_db.connection(execution_options={'isolation_level': 'AUTOCOMMIT'})


def pop_session() -> None:
    try:
        s.pg_db.commit()
    except Exception:
        s.pg_db.rollback()
    finally:
        s.pg_db.close()


class Sessions:
    @property
    def pg_db(self) -> Session:
        return pg_db.get()

    @pg_db.setter
    def pg_db(self, value: Session) -> None:
        pg_db.set(value)

    @property
    def pg_db_transaction(self) -> SessionTransaction | None:
        return pg_db_transaction.get()

    @pg_db_transaction.setter
    def pg_db_transaction(self, value: SessionTransaction) -> None:
        pg_db_transaction.set(value)


s = Sessions()
