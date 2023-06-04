"""
    Description: Processes user commands.

    Author: Ivan Maruzhenko
    Version: 1.0
"""

from Services.messages import HELP
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
        Displays basic information to the user

        :param update: an object that contains all the information and data that are coming from telegram itself;
        :param context: an object that contains information and data about the status of the library itself.
    """
    await context.bot.send_message(chat_id=update.effective_chat.id, text=HELP, parse_mode=ParseMode.HTML)
