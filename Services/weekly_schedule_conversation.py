"""
    Description: Contains logic of week schedule conversation.

    Author: Ivan Maruzhenko
    Version: 0.2
"""

from telegram import Update
from telegram.ext import ContextTypes
from loger_config import logger
from Services.schedule_builder import ScheduleBuilder
from Services.daily_schedule_conversation import send_links, clear_markup
from Database.db_function import today_day, get_week
from telegram.constants import ParseMode

current_week_day: int = today_day()
current_day: int = today_day()
current_week: int = get_week()
week_borders = {1: (1, 7), 2: (8, 14)}
WEEK_SCHEDULE, ALL_SCHEDULE = map(chr, range(8, 10))
link_message_id: bool = False


async def send_week_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Schedule for current week"""

    global current_week_day

    current_week_day = today_day()
    user = update.effective_user
    logger.info(f"User: {user.username}, user_id: {user.id}. The user requested a weekly schedule.")

    builder: ScheduleBuilder = ScheduleBuilder(update.effective_chat.id, current_week_day)
    await update.message.reply_text(text=builder.build_text("<b>РОЗКЛАД НА СЬОГОДНІ:</b>"),
                                    parse_mode=ParseMode.HTML,
                                    reply_markup=builder.build_extended_keyboard(step_back="previous_day",
                                                                                 step_forward="next_day",
                                                                                 callback="week_schedule_links"))

    return WEEK_SCHEDULE


async def next_day_in_week(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_week_day

    user = update.effective_user
    logger.info(f"User: {user.username}, user_id: {user.id}. The user requested a schedule for the next day.")

    if current_week_day != week_borders.get(current_week)[1]:
        current_week_day += 1
    else:
        current_week_day = week_borders.get(current_week)[0]

    await _week_schedule_message(update, context)


async def previous_day_in_week(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_week_day

    user = update.effective_user
    logger.info(f"User: {user.username}, user_id: {user.id}. The user requested a schedule for the previous day.")

    if current_week_day != week_borders.get(current_week)[0]:
        current_week_day -= 1
    else:
        current_week_day = week_borders.get(current_week)[1]

    await _week_schedule_message(update, context)


async def send_all_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """All schedule"""

    global current_day

    current_day = today_day()
    user = update.effective_user
    logger.info(f"User: {user.username}, user_id: {user.id}. The user requested a schedule for two weeks.")

    builder: ScheduleBuilder = ScheduleBuilder(update.effective_chat.id, current_day)
    await update.message.reply_text(text=builder.build_text("<b>РОЗКЛАД НА СЬОГОДНІ:</b>"),
                                    parse_mode=ParseMode.HTML,
                                    reply_markup=builder.build_extended_keyboard(step_back="back",
                                                                                 step_forward="forward",
                                                                                 callback="all_schedule_links"))

    return ALL_SCHEDULE


async def next_day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_day

    user = update.effective_user
    logger.info(f"User: {user.username}, user_id: {user.id}. The user requested a schedule for the next day.")

    if current_day != 14:
        current_day += 1
    else:
        current_day = 1

    await _all_schedule_message(update, context)


async def previous_day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_day

    user = update.effective_user
    logger.info(f"User: {user.username}, user_id: {user.id}. The user requested a schedule for the previous day.")

    if current_day != 1:
        current_day -= 1
    else:
        current_day = 14

    await _all_schedule_message(update, context)


async def _build_schedule_message(update: Update,
                                  context: ContextTypes.DEFAULT_TYPE,
                                  day: int,
                                  step_back: str,
                                  step_forward: str,
                                  callback: str):
    query = update.callback_query
    builder: ScheduleBuilder = ScheduleBuilder(update.effective_chat.id, day)

    await query.edit_message_text(text=builder.build_text(f"<b>РОЗКЛАД НА ДЕНЬ № {day}:</b>"),
                                  parse_mode=ParseMode.HTML,
                                  reply_markup=builder.build_extended_keyboard(step_back=step_back,
                                                                               step_forward=step_forward,
                                                                               callback=callback))


async def _week_schedule_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _build_schedule_message(update, context, current_week_day, "previous_day", "next_day", "week_schedule_links")


async def _all_schedule_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _build_schedule_message(update, context, current_day, "back", "forward", "all_schedule_links")


async def send_week_schedule_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await clear_markup(send_links)(update, context, current_week_day)


async def send_all_schedule_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await clear_markup(send_links)(update, context, current_day)
