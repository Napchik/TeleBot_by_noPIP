"""
    Description: Contains logic of start conversation.

    Author: Ivan Maruzhenko
    Version: 1.0
"""

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler
from loger_config import logger
from Database.db_function_user import check_user
from telegram.constants import ParseMode
from Services.messages import RoutineChoice
from Services.conversation_states import (
    RUN_REG,
    RUN_MAIN
)

answers = RoutineChoice.Answers


async def start_communication(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
        Starts a conversation with a user and checks if the user is logged in

        :param update: an object that contains all the information and data that are coming from telegram itself;
        :param context: an object that contains information and data about the status of the library itself;

        :return: state 'RUN_MAIN' or 'RUN_REG' of the START_CONVERSATION.
    """

    user = update.effective_user
    logger.info(f"User: {user.username}, user_id: {user.id}. The user has written '/start'.")

    if check_user(user.id):
        state = await _existing_user(update, context)
        return state

    state = await _new_user(update, context)
    return state


async def _existing_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
        Starts conversation for existing users

        :param update: an object that contains all the information and data that are coming from telegram itself;
        :param context: an object that contains information and data about the status of the library itself;

        :return: state 'RUN_MAIN' of the START_CONVERSATION.
    """

    user = update.effective_user
    text: str = f"Давно не бачились, <b>{user.username}</b>!\nНаправляю тебе до головного меню."
    reply_markup = ReplyKeyboardMarkup([[KeyboardButton(text=answers.GOT_IT)],
                                        [KeyboardButton(text=answers.CANCEL)]],
                                       one_time_keyboard=True,
                                       resize_keyboard=True)

    logger.info(f"User: {user.username}, user_id: {user.id}. "
                f"The user exists in the database. The user is prompted to go to the main menu.")

    await context.bot.send_message(chat_id=user.id, text=text, reply_markup=reply_markup,
                                   parse_mode=ParseMode.HTML)

    return RUN_MAIN


async def _new_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
        Starts conversation for new users

        :param update: an object that contains all the information and data that are coming from telegram itself;
        :param context: an object that contains information and data about the status of the library itself;

        :return: state 'RUN_REG' of the START_CONVERSATION.
    """

    user = update.effective_user
    text: str = "Вітаю тебе!\nБачу ти тут вперше? Давай знайомитись!"
    reply_markup = ReplyKeyboardMarkup([[KeyboardButton(text=answers.REG_START)],
                                        [KeyboardButton(text=answers.CANCEL)]],
                                       one_time_keyboard=True,
                                       resize_keyboard=True)

    logger.info(f"User: {user.username}, user_id: {user.id}. "
                f"The user does not exist in the database. The user is prompted to go to the registration menu.")

    await context.bot.send_message(chat_id=user.id, text=text, reply_markup=reply_markup,
                                   parse_mode=ParseMode.HTML)

    return RUN_REG


async def cancel_communication(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
        Stops communication with the user

        :param update: an object that contains all the information and data that are coming from telegram itself;
        :param context: an object that contains information and data about the status of the library itself;

        :return: end state of the START_CONVERSATION.
    """
    user = update.effective_user
    text: str = "Добре, повертайся коли передумаєш. 👋"

    await context.bot.send_message(chat_id=user.id, text=text, reply_markup=ReplyKeyboardRemove(),
                                   parse_mode=ParseMode.HTML)

    return ConversationHandler.END
