from typing import Any, Sequence

from sqlalchemy import Select, select
from sqlalchemy.orm import joinedload

from app.db.models import Driver, Result
from app.db.session import s


def _stmt_results() -> Select:
    query = select(Result).options(
        joinedload(Result.driver).joinedload(Driver.team),
        joinedload(Result.stage),
        joinedload(Result.race),
    )
    return query


def get_result() -> Sequence[Result]:
    results = (
        select(Result).options(
            joinedload(Result.driver).joinedload(Driver.team),
            joinedload(Result.stage),
            joinedload(Result.race)
        )
    ).order_by(Result.position)

    return s.pg_db.scalars(results).all()


def get_drivers() -> Sequence[Driver]:
    drivers = select(Driver).options(joinedload(Driver.team))
    return s.pg_db.scalars(drivers).all()


def get_driver(abbr: str) -> Any | None:
    driver = _stmt_results().where(Result.driver.and_(Driver.abbr == abbr))
    return s.pg_db.scalar(driver)


def result_as_dict(result: Result) -> dict[str, Any]:
    return {
        'place': result.position,
        'abbr': result.driver.abbr,
        'name': result.driver.name,
        'team': result.driver.team.name,
        'start_time': str(result.start_time),
        'end_time': str(result.end_time),
        'result': result.result,
        'stage': result.stage.name,
        'race': result.race.name,
        'year': result.race.year,
    }
