"""
    Description: Sends daily schedule every day.

    Author: Ivan Maruzhenko
    Version: 1.0
"""

import telegram

from loger_config import logger
from telegram.ext import ContextTypes
from telegram import Update
from Services.schedule_builder import ScheduleBuilder
from Database.db_function import all_groups, users_by_group
from Database.db_function_user import change_is_blocked
from Services.daily_schedule_conversation import send_links, clear_markup, today_day, tomorrow_day
from Services.conversation_states import TODAY_LINKS, TOMORROW_LINKS


async def routine(context: ContextTypes.DEFAULT_TYPE, day: int, callback: str, title: str = ""):
    """
        Function to build and send daily messages with schedule

        :param context: an object that contains information and data about the status of the library itself;
        :param day: day, for which the schedule is displayed;
        :param callback: Callback data for get links button;
        :param title: title of the message (usually name of week day). Default value - "".
    """

    for user in get_users_id():
        schedule = ScheduleBuilder(user, day)
        try:
            await context.bot.send_message(chat_id=user,
                                           text=schedule.build_text(title=title),
                                           parse_mode=telegram.constants.ParseMode.HTML,
                                           reply_markup=schedule.build_keyboard(callback=callback))
        except telegram.error.BadRequest:
            logger.warning(f"The user, with id - {user}, did not start a chat with the bot.")
            pass
        except telegram.error.Forbidden:
            logger.warning(f"The user, with id - {user}, blocked the bot.")
            change_is_blocked(user)
            pass


async def routine_today_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
        Sends message with special links for today's lessons with more than one link

        :param update: an object that contains all the information and data that are coming from telegram itself;
        :param context: an object that contains information and data about the status of the library itself.
    """

    user = update.effective_user
    logger.info(f"User: {user.username}, user_id: {user.id}. The user requested special links for today.")

    await clear_markup(send_links)(update, context, today_day())

    return TODAY_LINKS


async def routine_tomorrow_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
        Sends message with special links for today's lessons with more than one link

        :param update: an object that contains all the information and data that are coming from telegram itself;
        :param context: an object that contains information and data about the status of the library itself.
    """

    user = update.effective_user
    logger.info(f"User: {user.username}, user_id: {user.id}. The user requested special links for today.")

    await clear_markup(send_links)(update, context, tomorrow_day())

    return TOMORROW_LINKS


def get_users_id() -> list[int]:
    """ Get all users from all groups """
    list_of_users: list[int] = []
    for group in all_groups():
        for user in users_by_group(group):
            list_of_users.append(user)

    return list_of_users
