"""
    Description: Displays the user's schedule for today.

    Author: Ivan Maruzhenko
    Version: 0.4
"""
import telegram.constants
from telegram import Update
from telegram.ext import ContextTypes
from Services.day import Day
from Database.db_function import today_day, group_by_user


async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Daily schedule display function"""
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="<b>РОЗКЛАД НА СЬОГОДНІ:</b>\n\n" + Day(
                                       group_by_user(update.effective_user.id), today_day()).get_all_lessons(),
                                   parse_mode=telegram.constants.ParseMode.HTML)
