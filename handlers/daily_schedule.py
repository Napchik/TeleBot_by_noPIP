"""
    Description: Sends daily schedule.

    Author: Ivan Maruzhenko

    version 0.3
"""

from telegram.ext import ContextTypes
from services.routine import routine
from DataBase.db_function import today_day


async def daily_schedule(context: ContextTypes.DEFAULT_TYPE):
    """Sends daily schedule"""
    await routine(context=context, day=today_day())

