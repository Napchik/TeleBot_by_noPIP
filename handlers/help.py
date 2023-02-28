#
# Description: Displays basic information to the user about the Bot.
#
# Author: Ivan Maruzhenko
#
# version 0.1

from TeleBot_by_noPIP.services.messages import HELP

from telegram import Update
from telegram.ext import ContextTypes


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Displays basic information to the user"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=HELP)
