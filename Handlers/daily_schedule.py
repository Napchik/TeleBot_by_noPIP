"""
    Description: Sends daily schedule.

    Author: Ivan Maruzhenko
    Version: 0.4
"""

from telegram.ext import ContextTypes
from Services.routine import routine
from Database.db_function import today_day


async def daily_schedule(context: ContextTypes.DEFAULT_TYPE):
    """Sends daily schedule"""
    await routine(context=context, day=today_day(), title="<b>РОЗКЛАД НА СЬОГОДНІ:</b>\n\n")

