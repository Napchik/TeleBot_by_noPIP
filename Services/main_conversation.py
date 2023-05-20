"""
    Description: Contains logic of main conversation.

    Author: Ivan Maruzhenko
    Version: 0.2
"""

from telegram.constants import ParseMode
from loger_config import logger
from Services.messages import RoutineChoice
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes, ConversationHandler

MENU, SCHEDULE, GAME, SETTINGS, CONTROLS = map(chr, range(3, 8))

answers = RoutineChoice.Answers


async def start_main(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Start of main conversation"""
    user = update.message.from_user
    # answer = update.message.text

    logger.info(f"User: {user.username}, user_id: {user.id}. The user has started main conversation.")

    reply_markup = ReplyKeyboardMarkup([[KeyboardButton(text=answers.MAIN_SCHEDULE),
                                         KeyboardButton(text=answers.MAIN_SETTINGS)],

                                        [KeyboardButton(text=answers.MAIN_CONTROLS)],

                                        [KeyboardButton(text=answers.MAIN_GAME)]],
                                       one_time_keyboard=True,
                                       resize_keyboard=True)

    await context.bot.send_message(chat_id=user.id, text="<b>Головне меню:</b>", reply_markup=reply_markup,
                                   parse_mode=ParseMode.HTML)

    return MENU


async def schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Returned the keyboard with schedule options"""
    user = update.message.from_user
    answer = update.message.text

    logger.info(f"User: {user.username}, user_id: {user.id}. The user has asked to go to schedule conversation.")

    reply_markup = ReplyKeyboardMarkup([[KeyboardButton(text=answers.SCHEDULE_TODAY),
                                         KeyboardButton(text=answers.SCHEDULE_TOMORROW)],

                                        [KeyboardButton(text=answers.SCHEDULE_WEEK),
                                         KeyboardButton(text=answers.SCHEDULE_ALL)],

                                        [KeyboardButton(text=answers.BACK)]],
                                       one_time_keyboard=True,
                                       resize_keyboard=True)

    await context.bot.send_message(chat_id=user.id, text="<b>Розклад:</b>", reply_markup=reply_markup,
                                   parse_mode=ParseMode.HTML)

    return SCHEDULE


async def game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Open Game Conversation"""
    user = update.message.from_user
    answer = update.message.text

    logger.info(f"User: {user.username}, user_id: {user.id}. The user has started game conversation.")

    await context.bot.send_message(chat_id=user.id, text="<b>Гра</b>\nВ розробці...", parse_mode=ParseMode.HTML)


async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    answer = update.message.text

    logger.info(f"User: {user.username}, user_id: {user.id}. The user has started settings conversation.")

    reply_markup = ReplyKeyboardMarkup([[KeyboardButton(text=answers.SETTINGS_TIME)],

                                        [KeyboardButton(text=answers.SETTINGS_GROUP),
                                         KeyboardButton(text=answers.SETTINGS_BUG)],

                                        [KeyboardButton(text=answers.BACK)]],
                                       one_time_keyboard=True,
                                       resize_keyboard=True)

    await context.bot.send_message(chat_id=user.id, text="<b>Налаштування</b>", reply_markup=reply_markup,
                                   parse_mode=ParseMode.HTML)

    return SETTINGS


async def controls(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    answer = update.message.text

    logger.info(f"User: {user.username}, user_id: {user.id}. The user has started controls conversation.")

    reply_markup = ReplyKeyboardMarkup([[KeyboardButton(text=answers.CONTROLS_LINKS),
                                         KeyboardButton(text=answers.CONTROLS_ROLE)],

                                        [KeyboardButton(text=answers.BACK)]],
                                       one_time_keyboard=True,
                                       resize_keyboard=True)

    await context.bot.send_message(chat_id=user.id, text="<b>Керування</b>", reply_markup=reply_markup,
                                   parse_mode=ParseMode.HTML)


async def back_to_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Return to top level conversation"""

    user = update.message.from_user

    logger.info(f"User: {user.username}, user_id: {user.id}. The user has stopped {ConversationHandler.name}.")

    await start_main(update, context)

    return ConversationHandler.END
