"""
    Description: Contains logic of registration conversation.

    Author: Ivan Maruzhenko
    Version: 0.1
"""

from telegram.constants import ParseMode
from loger_config import logger
from Services.messages import START, REGISTRATION_INFO, RoutineChoice
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from telegram.ext import (
    ContextTypes,
    ConversationHandler
)

GROUP, ROUTINE, INFO = map(chr, range(3))
answers = RoutineChoice.Answers
results = RoutineChoice.Results


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Displays the first welcome message for the user"""
    user = update.message.from_user
    logger.info(f"User: {user.username}, user_id: {user.id}. The user has started conversation.")
    await context.bot.send_message(chat_id=user.id, text=START, parse_mode=ParseMode.HTML)

    return GROUP


async def group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Prompts the user for their group"""
    user = update.message.from_user
    group_name: str = update.message.text

    reply_markup = ReplyKeyboardMarkup([[KeyboardButton(text=answers.NO),
                                         KeyboardButton(text=answers.MORNING),
                                         KeyboardButton(text=answers.ALL)]], one_time_keyboard=True,
                                       resize_keyboard=True)

    logger.info(f"User: {user.username}, user_id: {user.id}. The user has selected the group {group_name}.")

    await update.message.reply_text(text=f"Ваша група: <b>{group_name}</b>",
                                    parse_mode=ParseMode.HTML)
    await update.message.reply_text(text="Бажаєте отримувати щоденний розклад?",
                                    reply_markup=reply_markup,
                                    parse_mode=ParseMode.HTML)

    return ROUTINE


async def routine(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    user = update.message.from_user
    answer = update.message.text
    markup = ReplyKeyboardMarkup([[KeyboardButton(text="Зрозуміло"),
                                   KeyboardButton(text="Скасувати")]],
                                 one_time_keyboard=True,
                                 resize_keyboard=True)

    logger.info(f"User: {user.username}, user_id: {user.id}. The user is choosing routine.")

    if answer == "Ні":
        await update.message.reply_text(text=results.NO, parse_mode=ParseMode.HTML, reply_markup=markup)
    elif answer == "Лише зранку":
        await update.message.reply_text(text=results.MORNING, parse_mode=ParseMode.HTML, reply_markup=markup)
    elif answer == "Зранку та ввечері":
        await update.message.reply_text(text=results.ALL, parse_mode=ParseMode.HTML, reply_markup=markup)

    return INFO


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    logger.info(f"User: {user.username}, user_id: {user.id}. The user has ended the conversation.")
    await update.message.reply_text(text=REGISTRATION_INFO,
                                    parse_mode=ParseMode.HTML,
                                    reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


async def misunderstand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    logger.info(f"User: {user.username}, user_id: {user.id}. Invalid input: {update.message.text}")

    await update.message.reply_text(text="Вибачте, я Вас не розумію. Спробуйте знову.",
                                    parse_mode=ParseMode.HTML)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    logger.info(f"User: {user.username}, user_id: {user.id}. The user has canceled the conversation.")

    await update.message.reply_text(text="Окей! Дані не будуть збережні.",
                                    parse_mode=ParseMode.HTML,
                                    reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END
