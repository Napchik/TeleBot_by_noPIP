"""
    Description: Download the schedule from the DB.

    Author: Ivan Maruzhenko
    Version: 1.0
"""

from Database.db_function import schedule_day_by_group, link_by_subject, professor_by_subject, time_by_number
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Lesson:
    """
        DataClass Lesson.

        Represents a lesson with name, number, professor, and link
    """

    number: int
    time: str = None
    name: str = None
    professor: str = None
    url: list[str] = None


class Lessons:
    """ The class for loading lessons from the database and converting them into instances of the Lesson class. """

    def __init__(self, group: str, day: int):
        self.group = group
        self.day = day
        self.data: str = schedule_day_by_group(self.group, self.day)
        self.lessons: list[Lesson] = self._load_lessons()

    def _split_input(self) -> list[str]:
        """ Split input string into lessons. """
        self.data = self.data.split("; ")
        return self.data

    def _load_lessons(self) -> list[Lesson]:
        """ Converting Input Data to Lesson Class Instances. """

        data = self._split_input()

        list_of_items = []

        for i, c in zip(data, range(6)):

            if i == "":
                list_of_items.append(Lesson(c + 1))
            else:
                time = time_by_number(c + 1)

                list_of_items.append(
                    Lesson(number=c + 1, time=time, name=i, professor=professor_by_subject(self.group, i),
                           url=link_by_subject(self.group, i).split(",")))
        return list_of_items

    def get_lesson(self, number: int) -> Lesson:
        """ Returns a specific lesson by number. """
        return self.lessons[number - 1]

    def get_all_lessons(self) -> list[Lesson]:
        """ Returns all lessons for the day. """
        return self.lessons
