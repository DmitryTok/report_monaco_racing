from reports.report import parse_racer_team, build_report, read_file, parse_time_lap
from models import Drivers, Time , db


DATA = 'data/'

def incert_data(path):
    start = read_file(path + 'start.log')
    end = read_file(path + 'end.log')
    racers = parse_racer_team(path)
    all_data = {}
    for key, value in start:
        all_data[key] = [value]
    for key, value in end:
        all_data[key].append(value)
    for key, value in racers.items():
        all_data[key].append(value)
    for key, value in all_data.items():
        code_id = Drivers.create(code=key, name=value[2])
        Time.create(
            code=code_id,
            start=value[0],
            end=value[1]
        )

if __name__ == '__main__':
    db.create_tables([Drivers, Time])
    incert_data(DATA)
