#
# Description: Download the schedule from the DB.
#
# Author: Ivan Maruzhenko
#
# version 0.1

from typing import NamedTuple

db_input = ('IO-13', 'Алгебра,,,Геометри,ТЕКС', None, None, None, None, None, None, None, None, None, None, None)


class Day(NamedTuple):
    """Daily schedule."""
    lesson1: str = None
    lesson2: str = None
    lesson3: str = None
    lesson4: str = None
    lesson5: str = None
    lesson6: str = None


class Schedule(NamedTuple):
    """Schedule for each day for the selected group."""
    group: str
    day1: Day
    day2: Day
    day3: Day
    day4: Day
    day5: Day
    day6: Day
    day8: Day
    day9: Day
    day10: Day
    day11: Day
    day12: Day
    day13: Day


def download_schedule_from_db(data: tuple) -> Schedule:
    """Download schedule from DB and put it into named tuple."""
    return Schedule(data[0], *[cast_to_day_schedule(data[index]) for index in range(1, len(data))])


def cast_to_day_schedule(item: str) -> Day | None:
    """Convert the schedule of the day from the string to the type 'Day'."""
    if item is None:
        return None

    list_of_items = []

    for i in item.split(","):
        if i == "":
            list_of_items.append(None)
        else:
            list_of_items.append(i)

    return Day(*list_of_items)
