from typing import Any, Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient

from app.app import create_app
from app.constants import DB_BASE_URL, DB_NAME, DB_POSTGRES, ECHO_OPTIONS
from app.db.init_engine import create_database, drop_database
from app.db.load_data import (
    load_drivers_teams,
    load_race,
    load_results,
    load_stage
    )
from app.db.session import close_dbs, pop_session, set_session
from app.utils.tables import create_tables


@pytest.fixture(scope='session')
def app() -> Generator[Flask, Any, None]:
    app = create_app()
    yield app


@pytest.fixture(scope='session')
def client(app) -> FlaskClient:
    return app.test_client()


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    create_database(
        db_url=f'{DB_BASE_URL}/{DB_POSTGRES}',
        db_name=DB_NAME,
    )
    print('CREATE DB')
    set_session()
    create_tables()
    load_drivers_teams('tests/data/abbreviations.txt')
    load_results(
        start='tests/data/start.txt',
        end='tests/data/end.txt',
        stage=load_stage('tests/data/stages.txt'),
        race=load_race(),
        driver=load_drivers_teams('tests/data/abbreviations.txt')
    )
    pop_session()


@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    try:
        close_dbs()
    finally:
        print('\nCLOSE DB')
    try:
        drop_database(db_url=f'{DB_BASE_URL}/{DB_POSTGRES}', db_name=DB_NAME)
    finally:
        print('DROP DB')
