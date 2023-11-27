
from app.utils.report.main import build_report


def show_report(
        abbr_path: str,
        start_path: str,
        end_path: str,
        is_sorted: bool = True) -> None:
    """ Print report with driver data and places """
    report = sorted(
        build_report(abbr_path, start_path, end_path).items(),
        key=lambda item: (
            item[1]['time'] >= 0, abs(item[1]['time'])
        )
    )
    if not is_sorted:
        report.reverse()
    place = 0
    for elem in report:
        place += 1
        print(f'{place}. {elem[0]} | {elem[1]["driver"]} | {elem[1]["time"]}')
        if place == 15:
            print('-' * 50)


def racer_info(
        abbr_path: str,
        start_path: str,
        end_path: str,
        driver_name: str
) -> None:
    """ Print info about racer by abbr """
    for item, elem in build_report(abbr_path, start_path, end_path).items():
        if driver_name == elem["driver"]:
            print(
                f'{item} | {elem["driver"]} | {elem["team"]} | {elem["time"]}'
            )
