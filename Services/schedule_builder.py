"""
    Description: Builds messages using pattern builder.

    Author: Ivan Maruzhenko
    Version: 1.0
"""

from Services.lessons import Lessons
from Database.db_function_user import check_user_group
from telegram import InlineKeyboardMarkup, InlineKeyboardButton


class ScheduleBuilder:
    """
        Class ScheduleBuilder

        Takes instance of lesson class and using it`s parameters to build messages.
    """

    def __init__(self, user_id, day: int):
        """
            Contains starting and processed values

            :param user_id: user id, used to define the user group;
            :param day: day, for which the schedule is displayed.
        """
        self.__group = check_user_group(user_id)
        self.__lessons = Lessons(self.__group, day)

    def build_text(self, title: str = "") -> str:
        """
            Builds the message with daily schedule

            :param title: title of the message (usually name of week day). Default value - "".
        """

        if title != "":
            title = title + "\n\n"

        text: str = ""

        for lesson in self.__lessons.get_all_lessons():

            if lesson.name is not None:
                text += f"{lesson.number}) ⏰ <i>{lesson.time}</i>"

                if len(lesson.url) <= 1:
                    text += f"\n<b><i><a href='{lesson.url[0]}'>{lesson.name}</a></i></b>"
                else:
                    text += f"<b><i>\n{lesson.name}</i></b>\n\n❗<i>Пара має декілька посилань.\n" \
                            f"Натисніть кнопку знизу для виводу всіх посилань.</i>\n"

                text += f"\n<I>{lesson.professor}</I>\n\n"

        if text != "":
            return title + text
        else:
            return title + "В цей день пар немає! Можна відпочивати! 😴"

    def build_keyboard(self, callback: str) -> InlineKeyboardMarkup:
        """
            Builds the keyboard with links to lessons.

            :param callback: - Callback data for get links button.
        """

        keyboard = self._build_special_markup(callback)

        return InlineKeyboardMarkup(keyboard)

    def build_extended_keyboard(self, step_back: str, step_forward: str, callback: str) -> InlineKeyboardMarkup:
        """
            Builds the extended keyboard with links to lessons and navigation buttons.

            :param step_back: Callback data for back button;
            :param step_forward: Callback data for forward button;
            :param callback: Callback data for get links button.
        """

        extended_keyboard = self._build_special_markup(callback)

        extended_keyboard.append([InlineKeyboardButton(text="⬅️", callback_data=step_back),
                                  InlineKeyboardButton(text="➡️", callback_data=step_forward)])

        return InlineKeyboardMarkup(extended_keyboard)

    def _build_markup(self):
        """ Builds the array with links to lessons """

        markup: list[[InlineKeyboardButton]] = []

        for lesson in self.__lessons.get_all_lessons():
            if lesson.name is not None:
                for url in lesson.url:
                    if url != "None":
                        markup.append([InlineKeyboardButton(f"{lesson.number}) {lesson.name}", url=url)])

        return markup

    def _build_special_markup(self, callback: str):
        """
            Builds buttons for lessons with more than one link

            :param callback: Callback data for get links button.

        """

        markup: list[[InlineKeyboardButton]] = []

        for lesson in self.__lessons.get_all_lessons():
            if lesson.name is not None and len(lesson.url) > 1:
                markup.append(
                    [InlineKeyboardButton(f"Посилання на пару № {lesson.number}",
                                          callback_data=callback + f"{lesson.number}")])

        return markup

    def build_link_list(self, lesson_number: int):
        """
            Builds message with links for lessons with more than one link

            :param lesson_number: lesson number in day timetable.
        """

        text: str = ""
        lesson = self.__lessons.get_lesson(lesson_number)
        if lesson.name is not None and len(lesson.url) > 1:
            text += f"<b>{lesson.name}</b>\n\n"
            text += "<b>Всі посилання на пару:\n\n</b>"
            for count, link in enumerate(lesson.url):
                if count + 1 != len(lesson.url):
                    text += f"<b>{count + 1}.</b> {link}\n\n"
                else:
                    text += f"<b>{count + 1}.</b> {link}"

        return text
