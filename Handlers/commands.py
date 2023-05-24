"""
    Description: Processes user commands.

    Author: Ivan Maruzhenko
    Version: 0.4
"""

import telegram.constants

from Services.messages import HELP
from telegram import Update
from telegram.ext import ContextTypes
from Services.schedule_builder import ScheduleBuilder
from Database.db_function import today_day


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Displays basic information to the user"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=HELP)

