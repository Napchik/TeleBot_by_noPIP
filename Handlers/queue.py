"""
    Description: Tasks to add to the queue.

    Author: Ivan Maruzhenko
    Version: 0.1
"""

from telegram.ext import ContextTypes
from Services.routine import routine
from Database.db_function import today_day


async def daily_schedule(context: ContextTypes.DEFAULT_TYPE):
    """Sends daily schedule"""
    await routine(context=context, day=today_day(), title="<b>РОЗКЛАД НА СЬОГОДНІ:</b>")


async def schedule_for_tomorrow(context: ContextTypes.DEFAULT_TYPE):
    """Sends schedule for tomorrow"""
    await routine(context=context, day=today_day() + 1, title="<b>РОЗКЛАД НА ЗАВТРА:</b>")
