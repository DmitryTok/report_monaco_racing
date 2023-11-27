import logging
from typing import Any

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.exc import OperationalError

logger = logging.getLogger(__name__)


def _engine_connection(db_url: str, options: dict[str, Any]) -> Engine:
    run_engine = create_engine(db_url, **options)
    connect = run_engine.connect()
    connect.close()
    return run_engine


def create_database(db_url: str, db_name: str) -> None:
    with create_engine(db_url, isolation_level='AUTOCOMMIT').begin() as conn:
        conn.execute(text(f'CREATE DATABASE {db_name};'))
        logger.info(f'Create Database {db_name}')


def drop_database(db_url: str, db_name: str) -> None:
    with create_engine(db_url, isolation_level='AUTOCOMMIT').begin() as conn:
        conn.execute(text(f'DROP DATABASE {db_name} WITH (FORCE);'))
        logger.info(f'Drop Database {db_name}')


def create_database_or_engine(
    db_base_url: str, db_name: str, postgres_db: str, options: dict[str, Any]
) -> Engine:
    working_db = f'{db_base_url}/{db_name}'
    try:
        return _engine_connection(db_url=working_db, options=options)
    except OperationalError as exc:
        if not str(exc).__contains__(f'database "{db_name}" does not exist'):
            raise exc
        psql = f'{db_base_url}/{postgres_db}'
        create_database(db_url=psql, db_name=db_name)
        return _engine_connection(db_url=working_db, options=options)
