"""
    Description: Contains logic of daily schedule conversation.

    Author: Ivan Maruzhenko
    Version: 0.1
"""

from telegram.constants import ParseMode
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from Services.schedule_builder import ScheduleBuilder
from Database.db_function import today_day
from loger_config import logger

GET_TODAY_LINKS, GET_TOMORROW_LINKS = map(chr, range(10, 12))


def clear_markup(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, day: int):
        query = update.callback_query
        await func(update, context, day)
        await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([]))

    return wrapper


async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a message with lessons for today"""

    user = update.effective_user
    logger.info(f"User: {user.username}, user_id: {user.id}. The user requested the schedule for today.")

    await _schedule_for_the_day(update, context, 3, "СЬОГОДНІ", "today_links")

    return GET_TODAY_LINKS


async def today_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends message with special links for today's lessons with more than one link"""

    user = update.effective_user
    logger.info(f"User: {user.username}, user_id: {user.id}. The user requested special links for today.")

    await clear_markup(send_links)(update, context, 3)


async def tomorrow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a message with lessons for tomorrow"""

    user = update.effective_user
    logger.info(f"User: {user.username}, user_id: {user.id}. The user requested the schedule for tomorrow.")

    await _schedule_for_the_day(update, context, 9, "ЗАВТРА", "tomorrow_links")

    return GET_TOMORROW_LINKS


async def tomorrow_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends message with special links for tomorrow's lessons with more than one link"""

    user = update.effective_user
    logger.info(f"User: {user.username}, user_id: {user.id}. The user requested special links for tomorrow.")

    await clear_markup(send_links)(update, context, 9)


async def _schedule_for_the_day(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        day: int,
        title: str,
        callback: str
):
    """
    Sends a message with lessons for the selected day.

    Arguments:
            day - day whose schedule is to be displayed ;
            title - title of the message ;
            callback - Callback data for get links button.

    """

    builder: ScheduleBuilder = ScheduleBuilder(update.effective_chat.id, day)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=builder.build_text(f"<b>РОЗКЛАД НА {title}:</b>"),
                                   parse_mode=ParseMode.HTML,
                                   reply_markup=builder.build_keyboard(callback),
                                   disable_web_page_preview=True)


async def send_links(update: Update, context: ContextTypes.DEFAULT_TYPE, day: int):
    """Sends message with links for lessons with more than one link"""

    builder: ScheduleBuilder = ScheduleBuilder(update.effective_chat.id, day)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=builder.build_link_list(),
                                   parse_mode=ParseMode.HTML,
                                   disable_web_page_preview=True)

    return ConversationHandler.END
