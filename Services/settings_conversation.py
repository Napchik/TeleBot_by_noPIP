"""
    Description: Settings conversation handlers.

    Author: Ivan Skorobagatko
    Version: 0.1.1
"""

import os

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes, ConversationHandler
from loger_config import logger
from Database.db_function_user import update_schedule_switch, change_group
from telegram.constants import ParseMode
from Services.messages import RoutineChoice

answers = RoutineChoice.Answers
CHANGE_TIME = chr(10)
CHANGE_GROUP = chr(11)
SEND_BUG = chr(12)


async def switch_schedule_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Switch Schedule Mode (0, 1, 2)"""

    user = update.effective_user
    logger.info(f"User: {user.username}, user_id: {user.id}. The user requested a schedule mode change.")

    reply_markup = ReplyKeyboardMarkup([[KeyboardButton(text=answers.SETTINGS_NO),
                                         KeyboardButton(text=answers.SETTINGS_MORNING),
                                         KeyboardButton(text=answers.SETTINGS_ALL)]],
                                       one_time_keyboard=True,
                                       resize_keyboard=True)

    await context.bot.send_message(chat_id=user.id, text="<b>Виберіть бажаний час</b>", reply_markup=reply_markup,
                                   parse_mode=ParseMode.HTML)

    return CHANGE_TIME


async def switch_group_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Switch Group Mode"""

    user = update.effective_user
    logger.info(f"User: {user.username}, user_id: {user.id}. The user requested a group change.")

    text = """<b>
    Введіть, будь ласка, Вашу групу.
    \n(ХХ-ХХ)
    \n\nНапишіть "Відмінити зміни" для скасування.</b>
    """

    await context.bot.send_message(chat_id=user.id, text=text, parse_mode=ParseMode.HTML)

    return CHANGE_GROUP


async def update_schedule_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Update DB Schedule Mode for User"""

    user = update.effective_user
    logger.info(f"User: {user.username}, user_id: {user.id}. The user updates a schedule mode.")

    user_choice = update.message.text

    if user_choice == answers.SETTINGS_NO:
        update_schedule_switch(user.id, 0)
    elif user_choice == answers.SETTINGS_MORNING:
        update_schedule_switch(user.id, 1)
    elif user_choice == answers.SETTINGS_ALL:
        update_schedule_switch(user.id, 2)

    reply_markup = ReplyKeyboardMarkup([[KeyboardButton(text=answers.SETTINGS_TIME)],

                                        [KeyboardButton(text=answers.SETTINGS_GROUP),
                                         KeyboardButton(text=answers.SETTINGS_BUG)],

                                        [KeyboardButton(text=answers.BACK)]],
                                       one_time_keyboard=True,
                                       resize_keyboard=True)

    await context.bot.send_message(chat_id=user.id, text="<b>Час змінено успішно</b>",
                                   reply_markup=reply_markup, parse_mode=ParseMode.HTML)

    return ConversationHandler.END


async def update_group_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Update DB Group for User"""

    user = update.effective_user
    logger.info(f"User: {user.username}, user_id: {user.id}. The user updates a group.")

    new_group = update.message.text

    change_group(user.id, new_group.upper())

    await context.bot.send_message(chat_id=user.id, text="<b>Групу змінено успішно</b>", parse_mode=ParseMode.HTML)

    return ConversationHandler.END


async def cancel_change(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel Group Change for User"""

    user = update.effective_user
    logger.info(f"User: {user.username}, user_id: {user.id}. The user canceled a group change.")

    await update.message.reply_text(text="Окей! Дані не будуть збережні.", parse_mode=ParseMode.HTML)

    return ConversationHandler.END


async def report_bug(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Report Bug"""

    user = update.effective_user
    logger.info(f"User: {user.username}, user_id: {user.id}. The user reports a bug.")

    await context.bot.send_message(chat_id=user.id, text="Будь-ласка, вкажіть вашу проблему.",
                                   parse_mode=ParseMode.HTML)

    return SEND_BUG


async def send_bug_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send Bug"""

    user = update.effective_user

    text = update.message.text
    logger.info(f"User: {user.username}, user_id: {user.id}. The user reports a bug.")

    # add_log(f"User: {user.username}, user_id: {user.id}. The user reports a bug.")

    REPORT_CHAT_ID = os.getenv("REPORTCHATID")

    await context.bot.send_message(chat_id=int(REPORT_CHAT_ID), text=text)
    await context.bot.send_message(chat_id=user.id, text="Ваше повідомлення надіслано адміністрації.")

    return ConversationHandler.END
