"""
    Description: Bot greeting.

    Author: Ivan Maruzhenko
    Version: 0.2
"""

from Services.messages import START

from telegram import Update
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Displays the first welcome message for the user"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=START)
