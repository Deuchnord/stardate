#!/usr/bin/env python3

from math import fabs
from datetime import datetime
import argparse

DATETIME_STANDARD_1 = datetime(2162, 1, 4)
DATETIME_STANDARD_2 = datetime(2270, 1, 26)
DATETIME_STANDARD_3 = datetime(2283, 10, 5)
DATETIME_STANDARD_4 = datetime(2323, 1, 1)


def main():
    args = get_args()
    date = datetime.fromisoformat(args.date) if args.date is not None else datetime.now()

    coeff, stardate, display_float = convert_to_stardate(date)
    print('Stardate: %s%s' % (('[%d] ' % coeff) if coeff is not None else '',
                              ('%.1f' if display_float else '%d') % stardate))


def convert_to_stardate(date: datetime) -> (int, float, bool):
    if date < DATETIME_STANDARD_2:
        diff = date - DATETIME_STANDARD_1
        units = diff.days * 5
        coeff = int(units / 10000)
        time = fabs(int(diff.seconds / 3600 / 5)) * (-1 if coeff < 0 else 1)
        units = fabs(units) - (fabs(coeff) * 10000) + time
        return coeff, units, False

    if date < DATETIME_STANDARD_3:
        diff = DATETIME_STANDARD_2 - date
        units = 197340 + 0.1 * diff.days
        coeff = int(units / 10000)
        units = fabs(units) - (fabs(coeff) * 10000)
        return coeff, units, False

    if date < DATETIME_STANDARD_4:
        diff = date - DATETIME_STANDARD_3
        units = 197840 + 0.5 * diff.days
        coeff = int(units / 10000)
        time = diff.seconds / 3600 / 48
        units = fabs(units) - (fabs(coeff) * 10000) + floor(time, 1)
        return coeff, units, True

    diff = date - DATETIME_STANDARD_4
    coeff = 1000 / (365 if not is_leap_year(date) else 366)
    time = diff.seconds / 3600 / 24
    units = (date.year - DATETIME_STANDARD_4.year) * 1000 + diff.days * coeff + time

    return None, floor(units, 1), True


def is_leap_year(date: datetime) -> bool:
    return date.year % 4 == 0 and date.year % 100 != 0 or date.year % 400 == 0


def floor(x: float, n: int = 0) -> float:
    return int(x * (10 ** n)) / (10 ** n)


def get_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--date', '-d', type=str)
    return argparser.parse_args()


if __name__ == '__main__':
    exit(main())
