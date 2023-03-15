"""
    Description: Displays the user's schedule for next day.

    Author: Ivan Maruzhenko

    version 0.4
"""
import telegram.constants
from telegram import Update
from telegram.ext import ContextTypes
from services.day import Day
from DataBase.db_function import today_day, group_by_user


async def tomorrow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Schedule for tomorrow"""
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=Day(group_by_user(update.effective_user.id), today_day() + 1).get_all_lessons(),
                                   parse_mode=telegram.constants.ParseMode.HTML)
