"""
    Description: Contains static phrases.

    Author: Ivan Maruzhenko
    Version: 0.2
"""

from dataclasses import dataclass
from typing import NamedTuple

START: str = "Привіт, я твій бот-помічник. Давай знайомитися!" \
             "\nВведи, будь ласка, свою групу." \
             "\n(ХХ-ХХ) <b>Латиницею!</b>" \
             "\n\n/cancel - скасувати реєстрацію."

HELP: str = "Мої можливості:" \
            "\n/start - почати спілкування;" \
            "\n/today - розклад на сьогодні;" \
            "\n/tomorrow - розклад на завтра."

REGISTRATION_INFO: str = "<b>Вдалого користування!</b>" \
                         "\n\nЯкщо Ви знайшли помилку в роботі бота - повідомте нам!" \
                         "\n( <i>Налаштування ➡ Зворотній зв'язок</i> )"


@dataclass(slots=True, frozen=True)
class Answers:
    REG_NO: str = "Ні"
    REG_MORNING: str = "Лише зранку"
    REG_ALL: str = "Зранку та ввечері"

    MAIN_SCHEDULE: str = "Розклад"
    MAIN_GAME: str = "Гра"
    MAIN_SETTINGS: str = "Налаштування"
    MAIN_INFO: str = "Корисна Інформація"
    MAIN_CONTROLS: str = "Керування"


@dataclass(slots=True, frozen=True)
class Results:
    NO: str = "Готово! Ви відмовилися від розсилки розкладу."
    MORNING: str = "Вітаю! Ви підписалися на ранкову розсилку розкладу."
    ALL: str = "Вітаю! Ви підписалися на повну розсилку розкладу."


class RoutineChoice(NamedTuple):
    Answers = Answers()
    Results = Results()
