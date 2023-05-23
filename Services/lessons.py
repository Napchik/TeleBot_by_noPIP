"""
    Description: Download the schedule from the DB.

    Author: Ivan Maruzhenko
    Version: 0.7
"""

from Database.db_function import schedule_day_by_group, link_by_subject, professor_by_subject
from dataclasses import dataclass

timetable = ("08:30 - 10:05", "10:25 - 12:00", "12:20 - 13:55", "14:15 - 15:50", "16:10 - 17:45", "18:30 - 20:05")


@dataclass(frozen=True, slots=True)
class Lesson:
    """Represents a lesson with name, number, professor, and link"""
    number: int
    time: str = None
    name: str = None
    professor: str = None
    url: list[str] = None


class Lessons:
    """The class for loading lessons from the database and converting them into instances of the Lesson class."""

    def __init__(self, group: str, day: int):
        self.group = group
        self.day = day
        self.data: str = schedule_day_by_group(self.group, self.day)
        self.lessons: list[Lesson] = self._load_lessons()

    def _split_input(self) -> list[str]:
        """Split input string into lessons"""
        self.data = self.data.split("; ")
        return self.data

    def _load_lessons(self) -> list[Lesson]:
        """Converting Input Data to Lesson Class Instances"""

        data = self._split_input()

        list_of_items = []

        for i, c in zip(data, range(6)):

            if i == "":
                list_of_items.append(Lesson(c + 1))
            else:
                list_of_items.append(
                    Lesson(number=c + 1, time=timetable[c], name=i, professor=professor_by_subject(self.group, i),
                           url=link_by_subject(self.group, i).split(",")))
        return list_of_items

    def get_lesson(self, number: int) -> Lesson:
        """Returns a specific lesson by number"""
        return self.lessons[number - 1]

    def get_all_lessons(self) -> list[Lesson]:
        """Returns all lessons for the day"""
        return self.lessons
