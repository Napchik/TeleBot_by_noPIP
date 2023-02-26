#
# Description: Download the schedule from the DB.
#
# Author: Ivan Maruzhenko
#
# version 0.1
import dataclasses
from typing import List

from db_function import schedule_day_by_group, professor_by_subject, link_by_subject
from dataclasses import dataclass

current_day = 3
current_group = "ІО-13"
db_input = schedule_day_by_group(current_group, current_day)
# db_input = "Основи підприємницької діяльності, Стилі в образотворчому мистецтві Лек on-line; " \
#            "Основи академічної доброчесності, Корпоративна культура та діловий етикет, " \
#            "Основи підприємницької діяльності, Естетика промислового дизайну Прак on-line; ; " \
#            "Естетика промислового дизайну Прак on-line; ; ; "


@dataclass
class Lesson:
    """Daily schedule."""
    number: int
    name: str = None
    # type: #str = None
    professor: str = None
    url: str = None


def _split_input(data: str) -> list[list[str]]:
    data = data.split("; ")
    data = [item.split(", ") for item in data]
    return data


def _load_lessons(data: list[list[str]]) -> [list[Lesson]]:
    """Convert the schedule of the day from the string to the type 'Day'."""
    if data is None:
        return None

    list_of_items = [list[Lesson]]

    for i, c in zip(data, range(6)):

        if i == "":
            list_of_items.append(Lesson(c + 1))
        else:
            for j in i:
                list_of_items.append(
                    Lesson(c, j, professor_by_subject(current_group, j), link_by_subject(current_group, j)))
    return list_of_items

    # def __init__(self, data: str):
    #     lessons = _cast_to_day_schedule(data)
    #     self.lesson1 = lessons[0]
    #     self.lesson2 = lessons[1]
    #     self.lesson3 = lessons[2]
    #     self.lesson4 = lessons[3]
    #     self.lesson5 = lessons[4]
    #     self.lesson6 = lessons[5]


# class Lessons:
#     def __init__(self):
#         self.lessons = _cast_to_day_schedule(db_input)

# def load_lessons(self):

# print(db_input)
for k in _load_lessons(_split_input(db_input)):
    print(k)
