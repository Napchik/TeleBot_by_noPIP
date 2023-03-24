"""
    Description: Sends daily schedule every day.

    Author: Ivan Maruzhenko
    Version: 0.3
"""

import logging

import telegram

from telegram.ext import ContextTypes
from Services.schedulebuilder import ScheduleBuilder
from Database.db_function import all_groups, users_by_group, group_by_user


async def routine(context: ContextTypes.DEFAULT_TYPE, day: int, title: str = ""):
    """Logic of daily mailings"""
    for user in _get_users_id():
        try:
            await context.bot.send_message(chat_id=user,
                                           text=title + ScheduleBuilder(group_by_user(user), day).build_text(),
                                           parse_mode=telegram.constants.ParseMode.HTML)
        except telegram.error.BadRequest:
            logging.warning(f"The user, with id - {user}, did not start a chat with the bot.")
            pass
        except telegram.error.Forbidden:
            logging.warning(f"The user, with id - {user}, blocked the bot.")
            pass


def _get_users_id() -> list[int]:
    """Get all users from all groups"""
    list_of_users: list[int] = []
    for group in all_groups():
        for user in users_by_group(group):
            list_of_users.append(user)

    return list_of_users
