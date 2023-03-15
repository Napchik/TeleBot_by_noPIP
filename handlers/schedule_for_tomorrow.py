"""
    Description: Sends schedule for tomorrow.

    Author: Ivan Maruzhenko

    version 0.1
"""

from telegram.ext import ContextTypes
from services.routine import routine
from DataBase.db_function import today_day


async def schedule_for_tomorrow(context: ContextTypes.DEFAULT_TYPE):
    """Sends schedule for tomorrow"""
    await routine(context=context, day=today_day() + 1)

