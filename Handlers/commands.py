"""
    Description: Processes user commands.

    Author: Ivan Maruzhenko
    Version: 0.4
"""

from Services.messages import HELP
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Displays basic information to the user"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=HELP, parse_mode=ParseMode.HTML)
