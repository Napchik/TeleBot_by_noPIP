"""
    Description: Tasks to add to the queue.

    Author: Ivan Maruzhenko
    Version: 0.1
"""

from telegram.ext import ContextTypes
from Services.routine import routine
from Database.db_function import today_day
from Database.db_function_user import deleting_blocked_user
from Database.schedule_uploader import schedule_info_uploader


async def daily_schedule(context: ContextTypes.DEFAULT_TYPE):
    """Sends daily schedule"""
    await routine(context=context, day=today_day(), title="<b>РОЗКЛАД НА СЬОГОДНІ:</b>")


async def schedule_for_tomorrow(context: ContextTypes.DEFAULT_TYPE):
    """Sends schedule for tomorrow"""
    await routine(context=context, day=today_day() + 1, title="<b>РОЗКЛАД НА ЗАВТРА:</b>")


async def daily_routine(context: ContextTypes.DEFAULT_TYPE):
    schedule_info_uploader()
    deleting_blocked_user()
