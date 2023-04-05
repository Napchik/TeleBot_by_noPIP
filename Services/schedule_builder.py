"""
    Description: Represents day timetable.

    Author: Ivan Maruzhenko
    Version: 0.6
"""

from Services.lessons import Lessons
from Database.db_function import group_by_user
from telegram import InlineKeyboardMarkup, InlineKeyboardButton


class ScheduleBuilder:
    """Class day represents the daily schedule"""

    def __init__(self, user_id, day: int):
        self.__group = group_by_user(user_id)
        self.__lessons = Lessons(self.__group, day)

    def build_text(self, title: str = "") -> str:
        """Builds the message with daily schedule"""

        if title != "":
            title = title + "\n\n"

        text: str = ""

        for lesson in self.__lessons.get_all_lessons():
            if lesson.name is not None:
                text += f"{lesson.number}) <I>{lesson.time}</I>" \
                        f"\n\n<B><I>{lesson.name}</I></B>" \
                        f"\n<I>{lesson.professor}</I>\n\n"

        if text != "":
            return title + text
        else:
            return title + "В цей день пар немає! Можна відпчивати! ;)"

    def build_markup(self) -> InlineKeyboardMarkup:
        """Builds the keyboard with links to lessons"""
        keyboard: list[InlineKeyboardButton] = []

        for lesson in self.__lessons.get_all_lessons():
            if lesson.name is not None:
                for url in lesson.url:
                    if url != "None":
                        keyboard.append(InlineKeyboardButton(f"{lesson.number}) {lesson.name}", url=url))

        return InlineKeyboardMarkup([[button] for button in keyboard])
