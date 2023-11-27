from datetime import datetime

from app.constants import PATTERN, TIME_FORMAT


def read_data_from_file(path: str) -> list[str]:
    """ Read input text file with data """
    with open(path) as file_parce:
        return [data for data in file_parce.read().splitlines() if data]


def parce_abbr_driver(path: str) -> dict[str, dict[str, str | int]]:
    """ Parce data from abbreviations file """
    parce_abbr = read_data_from_file(path)
    result = {}
    for line in parce_abbr:
        abbr, driver, team = line.split('_')
        result[abbr] = {'driver': driver, 'team': team}
    return result


def parce_abbr_time(path: str) -> dict[str, datetime]:
    """ Parce time and abbr data """
    abbr_time = read_data_from_file(path)
    result = {}
    for item in abbr_time:
        matches = PATTERN.match(item)
        if matches:
            abbr, time_str = matches.groups()
            result[abbr] = datetime.strptime(time_str, TIME_FORMAT)
    return result


def parce_start(path: str) -> dict[str, datetime]:
    """ Parce start time """
    return parce_abbr_time(path)


def parce_end(path: str) -> dict[str, datetime]:
    """ Parce end time """
    return parce_abbr_time(path)


def calculate_time_lap(start_path: str, end_path: str) -> dict[str, int]:
    """ Build a dict with driver abbr and converted time lap """
    result = {}
    start_time = parce_start(start_path)
    end_time = parce_end(end_path)
    for abbr, time in start_time.items():
        total_time = end_time[abbr] - time
        result[abbr] = int(total_time.total_seconds())
    return result


def build_report(
        abbr_path: str,
        start_path: str,
        end_path: str) -> dict[str, dict[str, str | int]]:
    """ Build report with driver name and total time """
    drivers = parce_abbr_driver(abbr_path)
    time_lap = calculate_time_lap(start_path, end_path)
    for abbr, abbr_time in drivers.items():
        abbr_time['time'] = time_lap[abbr]
    return drivers
