"""
    Description: Displays basic information to the user about the Bot.

    Author: Ivan Maruzhenko
    Version: 0.2
"""

from Services.messages import HELP

from telegram import Update
from telegram.ext import ContextTypes


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Displays basic information to the user"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=HELP)
