
"""
    Description: Displays the user's schedule for today.

    Author: Ivan Maruzhenko

    version 0.1
"""

from telegram import Update
from telegram.ext import ContextTypes
from TeleBot_by_noPIP.services.day import Day
from TeleBot_by_noPIP.db_function import today_day

current_day = today_day()
current_group = "ІО-11"


async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Daily schedule display function"""
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=Day(current_group, current_day).get_all_lessons())
