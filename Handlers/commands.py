"""
    Description: Processes user commands.

    Author: Ivan Maruzhenko
    Version: 0.1
"""
from Services.messages import START, HELP
import telegram.constants
from telegram import Update
from telegram.ext import ContextTypes
from Services.schedulebuilder import ScheduleBuilder
from Database.db_function import today_day


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Displays the first welcome message for the user"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=START)


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Displays basic information to the user"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=HELP)


async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Daily schedule display function"""
    builder: ScheduleBuilder = ScheduleBuilder("ІО-13", today_day())
    print(today_day())
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=builder.build_text("<b>РОЗКЛАД НА СЬОГОДНІ:</b>"),
                                   parse_mode=telegram.constants.ParseMode.HTML,
                                   reply_markup=builder.build_markup())


async def tomorrow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Schedule for tomorrow"""
    builder: ScheduleBuilder = ScheduleBuilder(update, today_day() + 1)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=builder.build_text("<b>РОЗКЛАД НА ЗАВТРА:</b>"),
                                   parse_mode=telegram.constants.ParseMode.HTML,
                                   reply_markup=builder.build_markup())
