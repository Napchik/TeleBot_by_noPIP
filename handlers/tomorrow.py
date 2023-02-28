
"""
    Description: Displays the user's schedule for next day.

    Author: Ivan Maruzhenko

    version 0.1
"""

from telegram import Update
from telegram.ext import ContextTypes
from TeleBot_by_noPIP.services.day import Day
from TeleBot_by_noPIP.DataBase.db_function import today_day

next_day = today_day() + 1
current_group = "ІО-11"


async def tomorrow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Schedule for tomorrow"""
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=Day(current_group, next_day).get_all_lessons())
