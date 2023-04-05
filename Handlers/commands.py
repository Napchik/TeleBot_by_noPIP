"""
    Description: Processes user commands.

    Author: Ivan Maruzhenko
    Version: 0.2
"""

import telegram.constants

from Services.messages import START, HELP
from telegram import Update
from telegram.ext import ContextTypes
from Services.schedule_builder import ScheduleBuilder
from Database.db_function import today_day


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Displays basic information to the user"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=HELP)


async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Daily schedule display function"""
    builder: ScheduleBuilder = ScheduleBuilder(update.effective_chat.id, today_day())
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=builder.build_text("<b>РОЗКЛАД НА СЬОГОДНІ:</b>"),
                                   parse_mode=telegram.constants.ParseMode.HTML,
                                   reply_markup=builder.build_markup())


async def tomorrow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Schedule for tomorrow"""
    builder: ScheduleBuilder = ScheduleBuilder(update.effective_chat.id, today_day() + 1)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=builder.build_text("<b>РОЗКЛАД НА ЗАВТРА:</b>"),
                                   parse_mode=telegram.constants.ParseMode.HTML,
                                   reply_markup=builder.build_markup())
