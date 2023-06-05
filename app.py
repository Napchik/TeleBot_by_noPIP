"""
    Description: Description of the Bot work.

    Author: Ivan Maruzhenko
    Version: 1.0
"""

import datetime
import Handlers
import os

from dotenv import load_dotenv, find_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, Application, ContextTypes, Defaults
from telegram import ReplyKeyboardRemove
from telegram.error import TelegramError
from Services.routine_conversation import get_users_id

load_dotenv(find_dotenv())

API_TOKEN = os.getenv("TOKEN")

COMMAND_HANDLERS = {
    "help": Handlers.help
}

CONVERSATION_HANDLERS = (
    Handlers.START_CONVERSATION,
    Handlers.REGISTRATION_CONVERSATION,
    Handlers.ROUTINE_CONVERSATION
)


async def post_init(my_app: Application) -> None:
    """
        Function, that starts after the initialization

        :param my_app: application.
    """
    await my_app.bot.set_my_commands([('start', 'Почати спілкування')])


async def post_stop(context: ContextTypes.DEFAULT_TYPE) -> None:
    """
        Function, that clear all keyboards after the applications stops

        :param context: an object that contains information and data about the status of the library itself.
    """
    for user_id in get_users_id():
        try:
            await context.bot.send_message(text="🚧 Бот тимчасово недоступний. Вибачте за незручності.",
                                           chat_id=user_id,
                                           reply_markup=ReplyKeyboardRemove(),
                                           disable_notification=True)
        except TelegramError:
            pass


def app():
    """ The main function of the program """

    time_zone = int(datetime.datetime.now().astimezone().strftime("%z")) / 100
    settings = Defaults(tzinfo=datetime.timezone(offset=datetime.timedelta(hours=time_zone)))
    application = ApplicationBuilder().token(API_TOKEN).defaults(settings).post_init(post_init).post_stop(
        post_stop).post_shutdown(post_stop).build()
    job_queue = application.job_queue
    job_queue.run_daily(Handlers.daily_schedule, time=datetime.time(7, 00, 00), days=tuple(range(1, 7)))
    job_queue.run_daily(Handlers.schedule_for_tomorrow, time=datetime.time(18, 00, 00), days=tuple(range(0, 7)))
    job_queue.run_daily(Handlers.daily_routine, time=datetime.time(00, 1, 00), days=tuple(range(0, 7)))

    for command_name, command_handler in COMMAND_HANDLERS.items():
        application.add_handler(CommandHandler(command_name, command_handler))

    for conversation in CONVERSATION_HANDLERS:
        application.add_handler(conversation)

    application.run_polling()
