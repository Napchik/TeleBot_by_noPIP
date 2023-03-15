"""
    Description: Description of the Bot work.

    Author: Ivan Maruzhenko

    version 0.5
"""

import datetime
import telegram.ext
import handlers
import logging
import os

from dotenv import load_dotenv, find_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler

load_dotenv(find_dotenv())

API_TOKEN = os.getenv("TOKEN")

# Configure logging

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

COMMAND_HANDLERS = {
    "start": handlers.start,
    "today": handlers.today,
    "tomorrow": handlers.tomorrow,
    "help": handlers.help
}


def app():
    """The main function of the program"""
    settings = telegram.ext.Defaults(tzinfo=datetime.timezone(offset=datetime.timedelta(hours=2)))
    application = ApplicationBuilder().token(API_TOKEN).defaults(settings).build()

    job_queue = application.job_queue
    job_queue.run_daily(handlers.daily_schedule, time=datetime.time(8, 00, 00), days=tuple(range(1, 7)))
    job_queue.run_daily(handlers.schedule_for_tomorrow, time=datetime.time(18, 00, 00), days=tuple(range(1, 7)))

    for command_name, command_handler in COMMAND_HANDLERS.items():
        application.add_handler(CommandHandler(command_name, command_handler))

    application.run_polling()
