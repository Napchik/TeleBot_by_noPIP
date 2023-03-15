"""
    Description: Download the schedule from the DB.

    Author: Ivan Maruzhenko

    version 0.4
"""

from DataBase.db_function import schedule_day_by_group, link_by_subject, professor_by_subject
from dataclasses import dataclass


@dataclass
class Lesson:
    """Represents a lesson with name, number, professor, and link"""
    number: int
    name: str = None
    professor: str = None
    url: list[str] = None

    def _split_links(self):
        """Checks if there are more links than one and separates them"""
        links = ""
        if len(self.url) > 1:
            for link in self.url:
                if link != "":
                    links += f"{link}\n"
        else:
            if self.url[0] != "None":
                links = f"{self.url[0]}"
            else:
                links = "Невідомо..."

        return links

    def __repr__(self):
        """Function to output an instance of a class"""
        return f"<b>Пара №{self.number})</b>\n<b><i>{self.name}</i></b>\n<b>Викладач: </b><i>{self.professor}" \
               f"</i>\n\n<b>Посилання на пару:</b>\n{self._split_links()}\n"


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

    def _load_lessons(self) -> list[Lesson] | None:
        """Converting Input Data to Lesson Class Instances"""
        if self.data is None:
            return None

        data = self._split_input()

        list_of_items = []

        for i, c in zip(data, range(6)):

            if i == "":
                list_of_items.append(Lesson(c + 1))
            else:
                list_of_items.append(
                    Lesson(c + 1, i, professor_by_subject(self.group, i),
                           link_by_subject(self.group, i).split(", ")))
        return list_of_items

    def get_lessons(self) -> list[Lesson]:
        """Returns all lessons for the day"""
        return self.lessons
