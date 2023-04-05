"""
    Description: Sends daily schedule every day.

    Author: Ivan Maruzhenko
    Version: 0.5
"""

import telegram

from loger_config import logger
from telegram.ext import ContextTypes
from Services.schedule_builder import ScheduleBuilder
from Database.db_function import all_groups, users_by_group


async def routine(context: ContextTypes.DEFAULT_TYPE, day: int, title: str = ""):
    """Logic of daily mailings"""

    for user in _get_users_id():
        schedule = ScheduleBuilder(user, day)
        try:
            await context.bot.send_message(chat_id=user,
                                           text=schedule.build_text(title=title),
                                           parse_mode=telegram.constants.ParseMode.HTML,
                                           reply_markup=schedule.build_markup())
        except telegram.error.BadRequest:
            logger.warning(f"The user, with id - {user}, did not start a chat with the bot.")
            pass
        except telegram.error.Forbidden:
            logger.warning(f"The user, with id - {user}, blocked the bot.")
            pass


def _get_users_id() -> list[int]:
    """Get all users from all groups"""
    list_of_users: list[int] = []
    for group in all_groups():
        for user in users_by_group(group):
            list_of_users.append(user)

    return list_of_users
