"""
    Description: Contains logic of daily schedule conversation.

    Author: Ivan Maruzhenko
    Version: 1.0
"""

import re
from Database.db_function import today_day, tomorrow_day
from telegram.constants import ParseMode
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from Services.schedule_builder import ScheduleBuilder
from loger_config import logger
from Services.conversation_states import (
    TODAY_SCHEDULE,
    TOMORROW_SCHEDULE
)


def clear_markup(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, day: int):
        query = update.callback_query
        current_markup = query.message.reply_markup
        new_markup = []
        await func(update, context, day)
        for row in current_markup.inline_keyboard:
            new_markup.append([button for button in row if button.callback_data != query.data])
        await query.edit_message_reply_markup(InlineKeyboardMarkup(new_markup))

    return wrapper


async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
        Sends a message with lessons for today

        :param update: an object that contains all the information and data that are coming from telegram itself;
        :param context: an object that contains information and data about the status of the library itself.
    """

    user = update.effective_user
    logger.info(f"User: {user.username}, user_id: {user.id}. The user requested the schedule for today.")

    await _schedule_for_the_day(update, context, today_day(), "СЬОГОДНІ", "today_links")

    return TODAY_SCHEDULE


async def today_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
        Sends message with special links for today's lessons with more than one link

        :param update: an object that contains all the information and data that are coming from telegram itself;
        :param context: an object that contains information and data about the status of the library itself.
    """

    user = update.effective_user
    logger.info(f"User: {user.username}, user_id: {user.id}. The user requested special links for today.")

    await clear_markup(send_links)(update, context, today_day())


async def tomorrow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
        Sends a message with lessons for tomorrow

        :param update: an object that contains all the information and data that are coming from telegram itself;
        :param context: an object that contains information and data about the status of the library itself.
    """

    user = update.effective_user
    logger.info(f"User: {user.username}, user_id: {user.id}. The user requested the schedule for tomorrow.")

    await _schedule_for_the_day(update, context, tomorrow_day(), "ЗАВТРА", "tomorrow_links")

    return TOMORROW_SCHEDULE


async def tomorrow_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
        Sends message with special links for tomorrow's lessons with more than one link

        :param update: an object that contains all the information and data that are coming from telegram itself;
        :param context: an object that contains information and data about the status of the library itself.
    """

    user = update.effective_user
    logger.info(f"User: {user.username}, user_id: {user.id}. The user requested special links for tomorrow.")

    await clear_markup(send_links)(update, context, tomorrow_day())


async def _schedule_for_the_day(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        day: int,
        title: str,
        callback: str
):
    """
        Sends a message with lessons for the selected day.

        :param day: day whose schedule is to be displayed;
        :param title: title of the message;
        :param callback: callback data for get links button;
        :param update: an object that contains all the information and data that are coming from telegram itself;
        :param context: an object that contains information and data about the status of the library itself.
    """

    builder: ScheduleBuilder = ScheduleBuilder(update.effective_chat.id, day)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=builder.build_text(f"<b>РОЗКЛАД НА {title}:</b>"),
                                   parse_mode=ParseMode.HTML,
                                   reply_markup=builder.build_keyboard(callback),
                                   disable_web_page_preview=True)


async def send_links(update: Update, context: ContextTypes.DEFAULT_TYPE, day: int):
    """
        Sends message with links for lessons with more than one link

        :param day: day whose schedule is to be displayed;
        :param update: an object that contains all the information and data that are coming from telegram itself;
        :param context: an object that contains information and data about the status of the library itself.
    """
    lesson_number = int(re.search(r"\d+", update.callback_query.data).group())
    builder: ScheduleBuilder = ScheduleBuilder(update.effective_chat.id, day)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=builder.build_link_list(lesson_number),
                                   parse_mode=ParseMode.HTML,
                                   disable_web_page_preview=True)

    return ConversationHandler.END
