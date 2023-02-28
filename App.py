
"""
    Description: Description of the Bot work.

    Author: Ivan Maruzhenko

    version 0.4

"""

import handlers
import logging
import os

from dotenv import load_dotenv, find_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler

load_dotenv(find_dotenv())

API_TOKEN = os.getenv("TOKEN")

# Configure logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

COMMAND_HANDLERS = {
    "start": handlers.start,
    "today": handlers.today,
    "tomorrow": handlers.tomorrow,
    "help": handlers.help
}

delivery_days: tuple[int, ...] = tuple(range(1, 7))


def app():
    """The main function of the program"""
    application = ApplicationBuilder().token(API_TOKEN).build()

    for command_name, command_handler in COMMAND_HANDLERS.items():
        application.add_handler(CommandHandler(command_name, command_handler))

    application.run_polling()
