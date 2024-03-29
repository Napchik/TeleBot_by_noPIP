"""
    Description: Settings conversation handlers.

    Author: Ivan Skorobagatko
    Version: 1.0
"""

import os

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, ConversationHandler
from telegram.constants import ParseMode
from loger_config import logger
from Services.messages import RoutineChoice
from Database.db_function import add_log
from Database.db_function_user import (
    update_schedule_switch,
    change_group,
    add_new_group,
    check_group,
    choose_role,
    check_user_group
)
from Services.conversation_states import (
    CHANGE_TIME,
    CHANGE_GROUP,
    SEND_BUG
)

answers = RoutineChoice.Answers


async def switch_schedule_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
       Switch Schedule Mode (0, 1, 2)

       :param update: an object that contains all the information and data that are coming from telegram itself;
       :param context: an object that contains information and data about the status of the library itself.
    """

    user = update.effective_user
    logger.info(f"User: {user.username}, user_id: {user.id}. The user requested a schedule mode change.")

    reply_markup = ReplyKeyboardMarkup([[KeyboardButton(text=answers.SETTINGS_NO),
                                         KeyboardButton(text=answers.SETTINGS_MORNING),
                                         KeyboardButton(text=answers.SETTINGS_ALL)]],
                                       one_time_keyboard=True,
                                       resize_keyboard=True)

    await context.bot.send_message(chat_id=user.id, text="<b>Виберіть бажаний час з переліку нижче</b>", reply_markup=reply_markup,
                                   parse_mode=ParseMode.HTML)

    return CHANGE_TIME


async def switch_group_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
        Switch Group Mode

        :param update: an object that contains all the information and data that are coming from telegram itself;
        :param context: an object that contains information and data about the status of the library itself.
    """

    user = update.effective_user
    logger.info(f"User: {user.username}, user_id: {user.id}. The user requested a group change.")

    text = f"""<b>
    Ваша поточна група: {check_user_group(user.id)}
    \nВведіть, будь ласка, назву нової групи.
    \n(ХХ-ХХ).</b>
    """

    await context.bot.send_message(chat_id=user.id, text=text, parse_mode=ParseMode.HTML,
                                   reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text=answers.SETTINGS_DENY,
                                                                                            callback_data="deny")]]))

    return CHANGE_GROUP


async def update_schedule_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
        Update DB Schedule Mode for User

        :param update: an object that contains all the information and data that are coming from telegram itself;
        :param context: an object that contains information and data about the status of the library itself.
    """

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

    await context.bot.send_message(chat_id=user.id, text="<b>Час змінено успішно ✅</b>",
                                   reply_markup=reply_markup, parse_mode=ParseMode.HTML)

    return ConversationHandler.END


async def update_group_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
        Update DB Group for User

        :param update: an object that contains all the information and data that are coming from telegram itself;
        :param context: an object that contains information and data about the status of the library itself.
    """

    user = update.effective_user
    logger.info(f"User: {user.username}, user_id: {user.id}. The user updates a group.")
    add_log(f"User: {user.username}, user_id: {user.id}. The user changes his group.")

    new_group = update.message.text.upper()
    if not check_group(new_group):
        add_new_group(new_group)
    if check_user_group(user.id) == new_group:
        await context.bot.send_message(chat_id=user.id, text=f"<b>Ви вже в групі {new_group}</b>",
                                       parse_mode=ParseMode.HTML)
        return ConversationHandler.END

    change_group(user.id, new_group, choose_role(new_group))

    await context.bot.send_message(chat_id=user.id, text="<b>Групу змінено успішно ✅</b>", parse_mode=ParseMode.HTML)
    return ConversationHandler.END


async def cancel_change(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
        Cancel Group Change for User

        :param update: an object that contains all the information and data that are coming from telegram itself;
        :param context: an object that contains information and data about the status of the library itself.
    """

    user = update.effective_user
    logger.info(f"User: {user.username}, user_id: {user.id}. The user canceled change.")
    query = update.callback_query
    await query.edit_message_text(text="Окей! Дані не будуть збережні", parse_mode=ParseMode.HTML)

    return ConversationHandler.END


async def report_bug(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
        Report Bug

        :param update: an object that contains all the information and data that are coming from telegram itself;
        :param context: an object that contains information and data about the status of the library itself.
    """

    user = update.effective_user
    logger.info(f"User: {user.username}, user_id: {user.id}. The user reports a bug.")

    await context.bot.send_message(chat_id=user.id, text="Будь-ласка, вкажіть вашу проблему 📝",
                                   parse_mode=ParseMode.HTML)

    return SEND_BUG


async def send_bug_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
        Send Bug

        :param update: an object that contains all the information and data that are coming from telegram itself;
        :param context: an object that contains information and data about the status of the library itself.
    """

    user = update.effective_user

    text = f"Користувач {user.username} повідомляє про промилку:\n\n"
    text += update.message.text
    logger.info(f"User: {user.username}, user_id: {user.id}. The user reports a bug.")

    add_log(f"User: {user.username}, user_id: {user.id}. The user reports a bug.")

    await context.bot.send_message(chat_id=int(os.getenv("REPORTCHATID")), text=text)
    await context.bot.send_message(chat_id=user.id, text="Ваше повідомлення надіслано адміністрації.")

    return ConversationHandler.END
