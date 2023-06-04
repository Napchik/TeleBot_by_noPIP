"""
    Description: Tasks to add to the queue.

    Author: Ivan Maruzhenko
    Version: 1.0
"""

from telegram.ext import ContextTypes
from Services.routine_conversation import routine
from Database.db_function import today_day, tomorrow_day, change_week
from Database.db_function_user import deleting_blocked_user
from Database.schedule_uploader import schedule_info_uploader
from Services.registration_conversation import users_dictionary


async def daily_schedule(context: ContextTypes.DEFAULT_TYPE):
    """
        Sends daily schedule

        :param context: an object that contains information and data about the status of the library itself.
    """
    await routine(context=context,
                  day=today_day(),
                  title="<b>РОЗКЛАД НА СЬОГОДНІ:</b>",
                  callback="routine_today_links")


async def schedule_for_tomorrow(context: ContextTypes.DEFAULT_TYPE):
    """
        Sends schedule for tomorrow

        :param context: an object that contains information and data about the status of the library itself.
    """
    await routine(context=context,
                  day=tomorrow_day(),
                  title="<b>РОЗКЛАД НА ЗАВТРА:</b>",
                  callback="routine_tomorrow_links")


async def daily_routine(context: ContextTypes.DEFAULT_TYPE):
    """
        Bot daily routine

        :param context: an object that contains information and data about the status of the library itself.
    """
    schedule_info_uploader()
    deleting_blocked_user()
    change_week()
    users_dictionary.clear()
