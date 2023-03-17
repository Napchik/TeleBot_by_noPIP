"""
    Description: Represents day timetable.

    Author: Ivan Maruzhenko
    Version: 0.4
"""

from Services.lessons import Lesson, Lessons


class Day:
    """Class day represents the daily schedule"""
    def __init__(self, group: str, day: int):
        self.lessons = Lessons(group, day)

    def get_lesson(self, number: int) -> Lesson:
        """Returns a specific lesson by number"""
        return self.lessons.get_lessons()[number - 1]

    def get_all_lessons(self) -> str:
        """Returns all lessons for the day"""
        result = ""

        for lesson in self.lessons.get_lessons():
            if lesson.name is not None:
                result += f"{lesson}\n"
        if result != "":
            return result
        else:
            return "В цей день пар немає! Можна відпчивати! ;)"
