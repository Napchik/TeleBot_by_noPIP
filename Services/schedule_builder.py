"""
    Description: Represents day timetable.

    Author: Ivan Maruzhenko
    Version: 0.8
"""

from Services.lessons import Lessons
from Database.db_function import group_by_user
from telegram import InlineKeyboardMarkup, InlineKeyboardButton


def build_extended_markup(step_back: str, step_forward: str):
    markup: list[InlineKeyboardButton] = [InlineKeyboardButton(text="<", callback_data=step_back),
                                          InlineKeyboardButton(text=">", callback_data=step_forward)]

    return markup


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
                text += f"{lesson.number}) <i>{lesson.time}</i>"

                if len(lesson.url) <= 1:
                    text += f"\n<b><i><a href='{lesson.url[0]}'>{lesson.name}</a></i></b>"
                else:
                    text += f"<b><i>\n{lesson.name}</i></b>\n\n❗<i>Пара має декілька посилань.\n" \
                            f"Натисніть кнопку знизу для виводу всіх посилань.</i>\n"

                text += f"\n<I>{lesson.professor}</I>\n\n"

        if text != "":
            return title + text
        else:
            return title + "В цей день пар немає! Можна відпочивати! ;)"

    def build_keyboard(self, callback: str) -> InlineKeyboardMarkup:
        """
        Builds the keyboard with links to lessons.

        Arguments:
            callback - Callback data for get links button.

        """

        keyboard = self._build_special_markup(callback)

        return InlineKeyboardMarkup(keyboard)

    def build_extended_keyboard(self, step_back: str, step_forward: str, callback: str) -> InlineKeyboardMarkup:
        """
        Builds the extended keyboard with links to lessons and navigation buttons.

        Arguments:
            step_back - Callback data for back button ;
            step_forward - Callback data for forward button ;
            callback - Callback data for get links button.

        """

        extended_keyboard = self._build_special_markup(callback)

        extended_keyboard.append(build_extended_markup(step_back, step_forward))

        return InlineKeyboardMarkup(extended_keyboard)

    def _build_markup(self):
        """Builds the array with links to lessons"""

        markup: list[[InlineKeyboardButton]] = []

        for lesson in self.__lessons.get_all_lessons():
            if lesson.name is not None:
                for url in lesson.url:
                    if url != "None":
                        markup.append([InlineKeyboardButton(f"{lesson.number}) {lesson.name}", url=url)])

        return markup

    def _build_special_markup(self, callback: str):
        """
        Builds buttons for lessons with more than one link.

        Arguments:
            callback - Callback data for get links button.

        """

        markup: list[[InlineKeyboardButton]] = []

        for lesson in self.__lessons.get_all_lessons():
            if lesson.name is not None and len(lesson.url) > 1:
                markup.append(
                    [InlineKeyboardButton(f"Посилання на пару № {lesson.number}", callback_data=callback)])

        return markup

    def build_link_list(self):
        """Builds message with links for lessons with more than one link"""

        text: str = "<b>Всі посилання на пару:\n\n</b>"
        for lesson in self.__lessons.get_all_lessons():
            if lesson.name is not None and len(lesson.url) > 1:
                for count, link in enumerate(lesson.url):
                    if count != len(lesson.url):
                        text += f"<b>{count + 1}.</b> {link}\n\n"
                    else:
                        text += f"<b>{count + 1}.</b> {link}"

        return text
