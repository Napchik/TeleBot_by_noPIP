
"""
    Description: Sends daily schedule every day.

    Author: Ivan Maruzhenko

    version 0.1
"""

import telegram


from telegram.ext import ContextTypes
from TeleBot_by_noPIP.services.exceptions import FailedToSend
from TeleBot_by_noPIP.services.day import Day
from TeleBot_by_noPIP.DataBase.db_function import today_day, all_groups, users_by_group, group_by_user

current_day = today_day()


async def daily_schedule(context: ContextTypes.DEFAULT_TYPE):
    """Sends daily schedule every day"""
    for user in _get_users_id():
        try:
            await context.bot.send_message(chat_id=user,
                                           text=Day(group_by_user(user), current_day).get_all_lessons())
        except telegram.error.BadRequest:
            raise FailedToSend


def _get_users_id() -> list[int]:
    list_of_users: list[int] = []
    for group in all_groups():
        for user in users_by_group(group):
            list_of_users.append(user)

    return list_of_users
