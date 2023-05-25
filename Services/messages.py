"""
    Description: Contains static phrases.

    Author: Ivan Maruzhenko
    Version: 0.4
"""

from dataclasses import dataclass
from typing import NamedTuple

START: str = "Привіт, я Ваш бот-помічник. Давайте знайомитися!" \
             "\nВведіть, будь ласка, Вашу групу." \
             "\n(ХХ-ХХ)" \
             "\n\n/cancel - скасувати реєстрацію."

HELP: str = "Мої можливості:" \
            "\n/start - пройти реєстрацію;" \
            "\n/menu - головне меню;" \
            "\n/today - розклад на сьогодні;" \
            "\n/tomorrow - розклад на завтра."

REGISTRATION_INFO: str = "<b>Вітаю! Ви успішно пройшли реєстрацію!</b>" \
                         "\n\nЯкщо Ви знайшли помилку в роботі бота - повідомте нам!" \
                         "\n( <i>Налаштування ➡ Зворотній зв'язок</i> )" \
                         "\n\n<b>Вдалого користування!</b>"

MODERATOR_INFO: str = "<b>Вітаю! Ви успішно пройшли реєстрацію!</b>" \
                      "\n\nМої вітання, Вам випала честь бути <b>модератором</b> групи!" \
                      "\nВ меню <i>Керування</i> Ви можете керувати посиланнями на пари, або передати" \
                      " свою роль іншому члену Вашої групи." \
                      "\n\nЯкщо Ви знайшли помилку в роботі бота - повідомте нам!" \
                      "\n( <i>Налаштування ➡ Зворотній зв'язок</i> )" \
                      "\n\n<b>Вдалого користування!</b>"


@dataclass(slots=True, frozen=True)
class Answers:
    BACK: str = "Повернутися"
    GOT_IT: str = "Зрозуміло"
    CANCEL: str = "Скасувати"

    REG_NO: str = "Ні"
    REG_MORNING: str = "Лише зранку"
    REG_ALL: str = "Зранку та ввечері"

    MAIN_SCHEDULE: str = "Розклад"
    MAIN_GAME: str = "Гра"
    MAIN_SETTINGS: str = "Налаштування"
    MAIN_INFO: str = "Корисна Інформація"
    MAIN_CONTROLS: str = "Керування"

    SCHEDULE_TODAY: str = "Сьогодні"
    SCHEDULE_TOMORROW: str = "Завтра"
    SCHEDULE_WEEK: str = "Поточний тиждень"
    SCHEDULE_ALL: str = "Два тижні"

    GAME_START: str = "Так"
    GAME_STOP: str = "Ні"

    SETTINGS_TIME: str = "Змінити час розсилки"
    SETTINGS_NO: str = "Ніколи"
    SETTINGS_MORNING: str = "Лише зранку"
    SETTINGS_ALL: str = "Зранку та ввечері"
    SETTINGS_GROUP: str = "Змінити групу"
    SETTINGS_DENY: str = "Відмінити зміни"
    SETTINGS_BUG: str = "Повідомити про помилку"

    CONTROLS_LINKS: str = "Змінити посилання на пару"
    CONTROLS_ROLE: str = "Передати роль модератора"


@dataclass(slots=True, frozen=True)
class Results:
    REG_NO: str = "Готово! Ви відмовилися від розсилки розкладу."
    REG_MORNING: str = "Вітаю! Ви підписалися на ранкову розсилку розкладу."
    REG_ALL: str = "Вітаю! Ви підписалися на повну розсилку розкладу."


class RoutineChoice(NamedTuple):
    Answers = Answers()
    Results = Results()
