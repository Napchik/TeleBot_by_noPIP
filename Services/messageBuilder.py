from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from Services.schedulebuilder import ScheduleBuilder


def build_text(day: ScheduleBuilder, title: str = "") -> str:
    if title != "":
        text: str = f"{title}\n"
    else:
        text: str = ""

    for lesson in day.build_text():
        text += f"{lesson.number}) {lesson.name}\n{lesson.professor}\n\n"

    return text


def build_markup(day: ScheduleBuilder) -> InlineKeyboardMarkup:
    keyboard: list[InlineKeyboardButton] = []

    for lesson in day.build_text():
        if lesson.url is not None:
            for url in lesson.url:
                keyboard.append(InlineKeyboardButton(f"{lesson.number}) {lesson.name}", url=url))

    return InlineKeyboardMarkup([[button] for button in keyboard])


