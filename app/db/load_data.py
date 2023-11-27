from itertools import chain

from app.db.models import Driver, Race, Result, Stage, Team
from app.db.session import s
from app.utils.report.main import (
    parce_abbr_driver,
    parce_end,
    parce_start,
    read_data_from_file
    )


def load_drivers_teams(path: str) -> dict[str, Driver]:
    driver_data = parce_abbr_driver(path)

    teams = {
        item['team']: Team(name=item['team'])
        for item in driver_data.values()
    }

    drivers = {
        abbr: Driver(
            abbr=abbr,
            name=elem.get('driver'),
            team=teams.get(elem['team'])
        )
        for abbr, elem in driver_data.items()
    }

    return drivers


def load_stage(path: str) -> list[Stage]:
    return [Stage(name=item) for item in read_data_from_file(path)]


def load_race() -> Race:
    return Race(name='Formula 1 - Monaco Racing', year=2018)


def load_results(
        start: str,
        end: str,
        stage: list[Stage],
        race: Race,
        driver: dict[str, Driver]
) -> None:
    start_time = parce_start(start)
    end_time = parce_end(end)
    results = []
    stages = stage
    race = race
    drivers = driver
    for abbr, lap_time in start_time.items():
        if driver := drivers.get(abbr):
            result = Result(
                    start_time=start_time[abbr],
                    end_time=end_time[abbr],
                    result=int((end_time[abbr] - start_time[abbr]).total_seconds()),
                    driver=driver,
                    stage=stages[-1],
                    race=race
                )
            results.append(result)

    sorted_results = sorted(
        results,
        key=lambda item: item.result
    )
    
    for index, elem in enumerate(sorted_results, start=1):
        elem.position = index

    s.pg_db.add_all(chain(stages, results))
    s.pg_db.commit()
