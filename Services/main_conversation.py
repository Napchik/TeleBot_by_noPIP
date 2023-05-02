"""
    Description: Contains logic of main conversation.

    Author: Ivan Maruzhenko
    Version: 0.1
"""

from telegram.constants import ParseMode
from loger_config import logger
from Services.messages import RoutineChoice
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, BotCommand
from telegram.ext import (
    ContextTypes,
    ConversationHandler
)

SCHEDULE, GAME, SETTINGS, MAIN_INFO, CONTROLS = map(chr, range(5))

answers = RoutineChoice.Answers


async def main(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Start of main conversation"""
    user = update.message.from_user
    answer = update.message.text

    logger.info(f"User: {user.username}, user_id: {user.id}. The user has started main conversation.")

    reply_markup = ReplyKeyboardMarkup([[KeyboardButton(text=answers.MAIN_SCHEDULE),
                                         KeyboardButton(text=answers.MAIN_GAME),
                                         KeyboardButton(text=answers.MAIN_SETTINGS),
                                         KeyboardButton(text=answers.MAIN_INFO),
                                         KeyboardButton(text=answers.MAIN_CONTROLS)]],
                                       one_time_keyboard=True,
                                       resize_keyboard=True)

    await context.bot.send_message(chat_id=user.id, text="<b>Головне меню:</b>", reply_markup=reply_markup,
                                   parse_mode=ParseMode.HTML)

    if answer == answers.MAIN_SCHEDULE:
        return SCHEDULE
    elif answer == answers.MAIN_GAME:
        return GAME
    elif answer == answers.MAIN_SETTINGS:
        return SETTINGS
    elif answer == answers.MAIN_INFO:
        return MAIN_INFO
    elif answer == answers.MAIN_CONTROLS:
        return CONTROLS


async def schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    answer = update.message.text

    logger.info(f"User: {user.username}, user_id: {user.id}. The user has started schedule conversation.")

    await context.bot.send_message(chat_id=user.id, text="<b>Розклад</b>", parse_mode=ParseMode.HTML)

    return main


async def game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    answer = update.message.text

    logger.info(f"User: {user.username}, user_id: {user.id}. The user has started game conversation.")

    await context.bot.send_message(chat_id=user.id, text="<b>Гра</b>", parse_mode=ParseMode.HTML)

    return main


async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    answer = update.message.text

    logger.info(f"User: {user.username}, user_id: {user.id}. The user has started settings conversation.")

    await context.bot.send_message(chat_id=user.id, text="<b>Налаштування</b>", parse_mode=ParseMode.HTML)

    return main


async def main_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    answer = update.message.text

    logger.info(f"User: {user.username}, user_id: {user.id}. The user has started info conversation.")

    await context.bot.send_message(chat_id=user.id, text="<b>Корисна Інформація</b>", parse_mode=ParseMode.HTML)

    return main


async def controls(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    answer = update.message.text

    logger.info(f"User: {user.username}, user_id: {user.id}. The user has started controls conversation.")

    await context.bot.send_message(chat_id=user.id, text="<b>Керування</b>", parse_mode=ParseMode.HTML)

    return main
