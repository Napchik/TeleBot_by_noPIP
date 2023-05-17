from telegram import Update
from telegram.ext import ContextTypes
from loger_config import logger
from Services.schedule_builder import ScheduleBuilder
from Database.db_function import today_day
from telegram.constants import ParseMode

current_day: int = today_day()
CHANGE_DAY = chr(9)


async def send_all_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Schedule for current_week"""

    user = update.effective_user
    logger.info(f"User: {user.username}, user_id: {user.id}. The user requested a schedule for two weeks.")

    builder: ScheduleBuilder = ScheduleBuilder(update.effective_chat.id, current_day)
    await update.message.reply_text(text=builder.build_text("<b>РОЗКЛАД НА СЬОГОДНІ:</b>"),
                                    parse_mode=ParseMode.HTML,
                                    reply_markup=builder.build_extended_keyboard(mode="all"))

    return CHANGE_DAY


async def next_day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_day

    user = update.effective_user
    logger.info(f"User: {user.username}, user_id: {user.id}. The user requested a schedule for the next day.")

    if current_day != 14:
        current_day += 1
    else:
        current_day = 1

    await _build_schedule_message(update, context, current_day)


async def previous_day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_day

    user = update.effective_user
    logger.info(f"User: {user.username}, user_id: {user.id}. The user requested a schedule for the previous day.")

    if current_day != 1:
        current_day -= 1
    else:
        current_day = 14

    await _build_schedule_message(update, context, current_day)


async def _build_schedule_message(update: Update, context: ContextTypes.DEFAULT_TYPE, day: int):
    query = update.callback_query
    builder: ScheduleBuilder = ScheduleBuilder(update.effective_chat.id, day)

    await query.edit_message_text(text=builder.build_text(f"<b>РОЗКЛАД НА ДЕНЬ № {day}:</b>"),
                                  parse_mode=ParseMode.HTML,
                                  reply_markup=builder.build_extended_keyboard(mode="all"))
