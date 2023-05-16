from telegram import Update
from telegram.ext import ContextTypes
from loger_config import logger
from Services.schedule_builder import ScheduleBuilder
from Database.db_function import today_day, get_week
from telegram.constants import ParseMode

current_week_day: int = today_day()
current_week: int = get_week()
week_borders = {1: (1, 7), 2: (8, 14)}
CHANGE_DAY_IN_WEEK = chr(8)


async def send_week_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Schedule for current_week"""

    user = update.effective_user
    logger.info(f"User: {user.username}, user_id: {user.id}. The user requested a weekly schedule.")

    builder: ScheduleBuilder = ScheduleBuilder(update.effective_chat.id, current_week_day)
    await update.message.reply_text(text=builder.build_text("<b>РОЗКЛАД НА СЬОГОДНІ:</b>"),
                                    parse_mode=ParseMode.HTML,
                                    reply_markup=builder.build_extended_keyboard(mode="week"))

    return CHANGE_DAY_IN_WEEK


async def next_day_in_week(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_week_day

    user = update.effective_user
    logger.info(f"User: {user.username}, user_id: {user.id}. The user requested a schedule for the next day.")

    if current_week_day != week_borders.get(current_week)[1]:
        current_week_day += 1
    else:
        current_week_day = week_borders.get(current_week)[0]

    await _build_week_schedule_message(update, context, current_week_day)


async def previous_day_in_week(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_week_day

    user = update.effective_user
    logger.info(f"User: {user.username}, user_id: {user.id}. The user requested a schedule for the previous day.")

    if current_week_day != week_borders.get(current_week)[0]:
        current_week_day -= 1
    else:
        current_week_day = week_borders.get(current_week)[1]

    await _build_week_schedule_message(update, context, current_week_day)


async def _build_week_schedule_message(update: Update, context: ContextTypes.DEFAULT_TYPE, day: int):
    query = update.callback_query
    builder: ScheduleBuilder = ScheduleBuilder(update.effective_chat.id, day)

    await query.edit_message_text(text=builder.build_text(f"<b>РОЗКЛАД НА ДЕНЬ № {day}:</b>"),
                                  parse_mode=ParseMode.HTML,
                                  reply_markup=builder.build_extended_keyboard(mode="week"))
