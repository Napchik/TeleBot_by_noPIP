"""
    Description: Sends daily schedule every day.

    Author: Ivan Maruzhenko

    version 0.1
"""

import logging

import telegram

from telegram.ext import ContextTypes
from services.day import Day
from DataBase.db_function import all_groups, users_by_group, group_by_user


async def schedule_for_tomorrow(context: ContextTypes.DEFAULT_TYPE):
    """Sends schedule for tomorrow"""
    await _routine(context=context, day=next_day)


async def routine(context: ContextTypes.DEFAULT_TYPE, day: int):
    """Logic of daily mailings"""
    for user in _get_users_id():
        try:
            await context.bot.send_message(chat_id=user,
                                           text=Day(group_by_user(user), day).get_all_lessons())
        except telegram.error.BadRequest:
            logging.warning(f"The user with id - {user} not in database!")
            pass


def _get_users_id() -> list[int]:
    """Get all users from all groups"""
    list_of_users: list[int] = []
    for group in all_groups():
        for user in users_by_group(group):
            list_of_users.append(user)

    return list_of_users
