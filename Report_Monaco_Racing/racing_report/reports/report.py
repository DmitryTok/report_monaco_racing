import datetime
import argparse
import operator
from collections import OrderedDict

 
def read_file(path: str) -> list:
    with open(path) as file:
        parsed_list = []
        for line in file:
            if line != '\n':
                line = line.replace('_', ' ').rstrip('\n')
                parsed_list.append((line[:3], line[3:]))
    return parsed_list


def parse_racer_team(path: str) -> list:
    racer = {}
    with open(path + 'abbreviations.txt') as file:
        for text in file:
            driver = text[4:].rstrip('\n').split('_')
            racer[text[:3]] = '{} | {}'.format(driver[0], driver[1])
    return racer


def parse_racer_html(path: str, revers_racers=True) -> list:
    racer = []
    with open(path + 'abbreviations.txt') as file:
        for text in file:
            racer.append(text.rstrip('\n').replace('_', ' '))
    if revers_racers:
        return sorted(racer, reverse=False)
    else:
        return sorted(racer, reverse=True)


def parse_time_lap(path: str) -> list:
    start = read_file(path + 'start.log')
    end = read_file(path + 'end.log')
    time_dict = {}
    result_list = []
    for key, value in start:
        time_dict[key] = [value]
    for key, value in end:
        time_dict[key].append(value)
    for time in time_dict.values():
        lap_time = datetime.datetime.strptime(time[1], "%Y-%m-%d %H:%M:%S.%f") - datetime.datetime.strptime(time[0], "%Y-%m-%d %H:%M:%S.%f")
        result_list.append(str(lap_time))
    return result_list


def build_report(path: str, sort_list: bool=True) -> dict:
    racer = parse_racer_team(path)
    time_lap = parse_time_lap(path)
    dict_racer_time = dict(zip(racer.values(), time_lap))
    if sort_list:
        return dict(sorted(dict_racer_time.items(),
                                key=lambda x: str(x[1])))
    else:
        return dict(sorted(dict_racer_time.items(),
                            key=lambda x: str(x[1]),
                            reverse=True))


def racer_info(path: str, racer: str) -> str:
    driver = parse_racer_html(path)
    time_lap = parse_time_lap(path)
    driver_time_dict = dict(zip(driver, time_lap))
    sorted_tuples = sorted(driver_time_dict.items(), key=operator.itemgetter(1))
    result_dict = OrderedDict()
    for item, elem in sorted_tuples:
        result_dict[item] = elem
    for name, time in result_dict.items():
        if racer in name[:3]:
            return f'{name} | {time}'


def print_report(path: str, sort_list: bool = True) -> list:
    report = build_report(path, sort_list)
    report_list = []
    for i in report.items():
        report_list.append('{} | {}'.format(i[0], i[1]))
    return report_list


def command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', help='Directory path to file')
    parser.add_argument('--driver', help='Name of driver')
    parser.add_argument('--asc', action='store_const', const=True, help='Sort by Ascending')
    parser.add_argument('--desc', action='store_const', const=True, help='Sort by Descending')
    args = parser.parse_args()
    if args.file:
        if args.driver:
            racer_info(args.file, args.driver)
        if args.asc:
            print_report(args.file, True)
        else:
            print_report(args.file, False)
