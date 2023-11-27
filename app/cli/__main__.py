import argparse

from app.constants import (
    ABBREVIATIONS,
    DB_BASE_URL,
    DB_NAME,
    DB_POSTGRES,
    ECHO_OPTIONS,
    END,
    STAGES,
    START
    )
from app.db.init_engine import create_database_or_engine, drop_database
from app.db.load_data import (
    load_drivers_teams,
    load_race,
    load_results,
    load_stage
    )
from app.db.session import pop_session, set_session
from app.utils.tables import create_tables


def command_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser('APIReport of Monaco 2018 Racing')
    parser.add_argument('--db_name', help='Database name', default=DB_NAME)
    parser.add_argument(
        '--create',
        help='Create Database',
        action='store_const',
        const=True
    )
    parser.add_argument(
        '--drop',
        help='Delete Database',
        action='store_const',
        const=True
    )
    parser.add_argument(
        '--recreate',
        help='Recreate Database',
        action='store_const',
        const=True
    )
    parser.add_argument(
        '--load_data',
        help='Load data to Database',
        action='store_const',
        const=True
    )
    return parser


def command_line() -> None:
    args = command_parser().parse_args()
    db_url = f'{DB_BASE_URL}/{DB_POSTGRES}'

    if args.drop:
        drop_database(db_url=db_url, db_name=args.db_name)
        return

    if args.create:
        create_database_or_engine(
            db_base_url=DB_BASE_URL,
            db_name=args.db_name,
            postgres_db=str(DB_POSTGRES),
            options=ECHO_OPTIONS
        )

    if args.recreate:
        drop_database(db_url=db_url, db_name=args.db_name)
        create_database_or_engine(
            db_base_url=DB_BASE_URL,
            db_name=args.db_name,
            postgres_db=str(DB_POSTGRES),
            options=ECHO_OPTIONS
        )

    if args.load_data:
        set_session()
        create_tables()
        print(load_results(
            START,
            END,
            stage=load_stage(STAGES),
            race=load_race(),
            driver=load_drivers_teams(ABBREVIATIONS)
        ))
        pop_session()


if __name__ == '__main__':
    command_line()
