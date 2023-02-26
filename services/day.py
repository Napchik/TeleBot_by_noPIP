#
# Description: Represents day timetable
#
# Author: Ivan Maruzhenko
#
# version 0.1

from lessons import Lessons, Lesson

current_day = 1
current_group = "ІО-11"


class Day:
    def __init__(self, group: str, day: int):
        self.lessons = Lessons(group, day)

    def get_lesson(self, number: int) -> Lesson:
        return self.lessons.get_lessons()[number - 1]

    def get_all_lessons(self) -> str:
        result = ""

        for lesson in self.lessons.get_lessons():
            if lesson.name is not None:
                result += f"{lesson}\n"

        return result


print(Day(current_group, current_day).get_all_lessons())
