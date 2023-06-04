"""
    Description: Contains logic of weekly schedule conversations (for week or all).

    Author: Ivan Maruzhenko
    Version: 1.0
"""

from telegram import Update
from telegram.ext import ContextTypes
from loger_config import logger
from Services.schedule_builder import ScheduleBuilder
from Services.daily_schedule_conversation import send_links, clear_markup
from Database.db_function import today_day, get_week, day_name
from telegram.constants import ParseMode
from Services.conversation_states import (
    WEEK_SCHEDULE,
    ALL_SCHEDULE
)

week_borders = {1: (1, 7), 2: (8, 14)}


async def send_week_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
        Sends a carousel of weekly schedules

        :param update: an object that contains all the information and data that are coming from telegram itself;
        :param context: an object that contains information and data about the status of the library itself;

        :return: state 'WEEK_SCHEDULE' of the SCHEDULE_CONVERSATION.
    """

    user = update.effective_user
    logger.info(f"User: {user.username}, user_id: {user.id}. The user requested a weekly schedule.")

    builder: ScheduleBuilder = ScheduleBuilder(update.effective_chat.id, today_day())
    await update.message.reply_text(text=builder.build_text("<b>РОЗКЛАД НА СЬОГОДНІ:</b>"),
                                    parse_mode=ParseMode.HTML,
                                    reply_markup=builder.build_extended_keyboard(step_back="previous_day",
                                                                                 step_forward="next_day",
                                                                                 callback="week_schedule_links"))

    return WEEK_SCHEDULE


async def next_day_in_week(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
        Switches to the next day in a particular week

        :param update: an object that contains all the information and data that are coming from telegram itself;
        :param context: an object that contains information and data about the status of the library itself.
    """

    user = update.effective_user
    current_week_day = find_day(update, context)
    logger.info(f"User: {user.username}, user_id: {user.id}. The user requested a schedule for the next day.")

    if current_week_day != week_borders.get(get_week())[1]:
        current_week_day += 1
    else:
        current_week_day = week_borders.get(get_week())[0]

    await _week_schedule_message(update, context, current_week_day)


async def previous_day_in_week(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
        Switches to the previous day in a particular week

        :param update: an object that contains all the information and data that are coming from telegram itself;
        :param context: an object that contains information and data about the status of the library itself.
    """

    user = update.effective_user
    current_week_day = find_day(update, context)
    logger.info(f"User: {user.username}, user_id: {user.id}. The user requested a schedule for the previous day.")

    if current_week_day != week_borders.get(get_week())[0]:
        current_week_day -= 1
    else:
        current_week_day = week_borders.get(get_week())[1]

    await _week_schedule_message(update, context, current_week_day)


async def send_all_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
        Sends a carousel of all schedule

        :param update: an object that contains all the information and data that are coming from telegram itself;
        :param context: an object that contains information and data about the status of the library itself;

        :return: state 'ALL_SCHEDULE' of the SCHEDULE_CONVERSATION.
    """

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
    """
        Switches to the next day in all schedule

        :param update: an object that contains all the information and data that are coming from telegram itself;
        :param context: an object that contains information and data about the status of the library itself.
    """

    user = update.effective_user
    current_day = find_day(update, context)
    logger.info(f"User: {user.username}, user_id: {user.id}. The user requested a schedule for the next day.")

    if current_day != 14:
        current_day += 1
    else:
        current_day = 1

    await _all_schedule_message(update, context, current_day)


async def previous_day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
        Switches to the previous day in all schedule

        :param update: an object that contains all the information and data that are coming from telegram itself;
        :param context: an object that contains information and data about the status of the library itself.
    """

    user = update.effective_user
    current_day = find_day(update, context)
    logger.info(f"User: {user.username}, user_id: {user.id}. The user requested a schedule for the previous day.")

    if current_day != 1:
        current_day -= 1
    else:
        current_day = 14

    await _all_schedule_message(update, context, current_day)


async def _build_schedule_message(update: Update,
                                  context: ContextTypes.DEFAULT_TYPE,
                                  day: int,
                                  step_back: str,
                                  step_forward: str,
                                  callback: str):
    """
        Builds the messages with schedule for the defined day with extended keyboard

        :param update: an object that contains all the information and data that are coming from telegram itself;
        :param context: an object that contains information and data about the status of the library itself;
        :param  day: day, for which the schedule is displayed;
        :param  step_back: Callback data for back button;
        :param  step_forward: Callback data for forward button;
        :param  callback: Callback data for get links button.
    """

    query = update.callback_query
    builder: ScheduleBuilder = ScheduleBuilder(update.effective_chat.id, day)

    await query.edit_message_text(text=builder.build_text(f"<b>РОЗКЛАД НА {day_name(day)}:</b>"),
                                  parse_mode=ParseMode.HTML,
                                  reply_markup=builder.build_extended_keyboard(step_back=step_back,
                                                                               step_forward=step_forward,
                                                                               callback=callback))


async def _week_schedule_message(update: Update, context: ContextTypes.DEFAULT_TYPE, day: int):
    """
        Collecting information for schedule builder for a week

        :param update: an object that contains all the information and data that are coming from telegram itself;
        :param context: an object that contains information and data about the status of the library itself;
        :param day: day, for which the schedule is displayed.
    """

    await _build_schedule_message(update, context, day, "previous_day", "next_day", "week_schedule_links")


async def _all_schedule_message(update: Update, context: ContextTypes.DEFAULT_TYPE, day: int):
    """
        Collecting information for schedule builder for both weeks

        :param update: an object that contains all the information and data that are coming from telegram itself;
        :param context: an object that contains information and data about the status of the library itself;
        :param day: day, for which the schedule is displayed.
    """

    await _build_schedule_message(update, context, day, "back", "forward", "all_schedule_links")


async def send_week_schedule_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
        Sends links for week schedule

        :param update: an object that contains all the information and data that are coming from telegram itself;
        :param context: an object that contains information and data about the status of the library itself.
    """

    await clear_markup(send_links)(update, context, find_day(update, context))


async def send_all_schedule_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
        Sends links for all schedule

        :param update: an object that contains all the information and data that are coming from telegram itself;
        :param context: an object that contains information and data about the status of the library itself.
    """

    await clear_markup(send_links)(update, context, find_day(update, context))


def find_day(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
        Looking for the right day

        :param update: an object that contains all the information and data that are coming from telegram itself;
        :param context: an object that contains information and data about the status of the library itself.
    """

    old_message = update.callback_query.message.text
    old_day = old_message.splitlines()[0][11:-1]

    for day in range(1, 15):
        if old_day == day_name(day):
            return day

    return today_day()
