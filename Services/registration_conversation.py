"""
    Description: Contains logic of registration conversation.

    Author: Ivan Maruzhenko
    Version: 0.2
"""

from telegram.constants import ParseMode
from loger_config import logger
from Services.messages import START, RE_START, REGISTRATION_INFO, MODERATOR_INFO, RoutineChoice
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from dataclasses import dataclass
from Database.db_function_user import choose_role, add_user, check_user


@dataclass
class UserData:
    name: str = None
    surname: str = None
    username: str = None
    id: int = None
    group: str = None
    schedule_mode: int = None
    role: str = None

    def send_data(self):
        add_user(self.name, self.surname, self.username, self.id, self.group, self.schedule_mode, self.role)


GROUP, ROUTINE, REG_INFO, REG_EXIT = map(chr, range(4))
answers = RoutineChoice.Answers
results = RoutineChoice.Results
user_data = UserData()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Displays the first welcome message for the user"""
    user = update.message.from_user
    user_data.name = user.first_name
    user_data.surname = user.last_name
    user_data.username = user.username
    user_data.id = user.id

    if check_user(user.id) and update.message.text == "/start":
        logger.info(f"User: {user.username}, user_id: {user.id}. The user has written 'start' but already registered.")
        await context.bot.send_message(chat_id=user.id, text=RE_START, parse_mode=ParseMode.HTML,
                                       reply_markup=ReplyKeyboardMarkup([[KeyboardButton(answers.GOT_IT)]],
                                                                        one_time_keyboard=True, resize_keyboard=True))
        return REG_EXIT

    logger.info(f"User: {user.username}, user_id: {user.id}. The user has started conversation.")

    await context.bot.send_message(chat_id=user.id, text=START, parse_mode=ParseMode.HTML)

    return GROUP


async def group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Prompts the user for their group"""
    user = update.message.from_user
    group_name: str = update.message.text.upper()

    user_data.group = group_name

    reply_markup = ReplyKeyboardMarkup([[KeyboardButton(text=answers.REG_NO),
                                         KeyboardButton(text=answers.REG_MORNING),
                                         KeyboardButton(text=answers.REG_ALL)]], one_time_keyboard=True,
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

    markup = ReplyKeyboardMarkup([[KeyboardButton(text=answers.GOT_IT),
                                   KeyboardButton(text=answers.CANCEL)]],
                                 one_time_keyboard=True,
                                 resize_keyboard=True)

    logger.info(f"User: {user.username}, user_id: {user.id}. The user is choosing routine.")

    if answer == answers.REG_NO:
        user_data.schedule_mode = 0
        await update.message.reply_text(text=results.REG_NO, parse_mode=ParseMode.HTML, reply_markup=markup)
    elif answer == answers.REG_MORNING:
        user_data.schedule_mode = 1
        await update.message.reply_text(text=results.REG_MORNING, parse_mode=ParseMode.HTML, reply_markup=markup)
    elif answer == answers.REG_ALL:
        user_data.schedule_mode = 2
        await update.message.reply_text(text=results.REG_ALL, parse_mode=ParseMode.HTML, reply_markup=markup)

    return REG_INFO


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    user_data.role = choose_role(user_data.group)

    logger.info(f"User: {user.username}, user_id: {user.id}. The user has been assigned a role '{user_data.role}'.")

    if user_data.role == "user":
        await update.message.reply_text(text=REGISTRATION_INFO,
                                        parse_mode=ParseMode.HTML,
                                        reply_markup=ReplyKeyboardMarkup([[KeyboardButton(answers.GOT_IT)]],
                                                                         one_time_keyboard=True, resize_keyboard=True))
    elif user_data.role == "moderator":
        await update.message.reply_text(text=MODERATOR_INFO,
                                        parse_mode=ParseMode.HTML,
                                        reply_markup=ReplyKeyboardMarkup([[KeyboardButton(answers.GOT_IT)]],
                                                                         one_time_keyboard=True, resize_keyboard=True))

    user_data.send_data()

    logger.info(f"User: {user.username}, user_id: {user.id}. User successfully completed registration."
                f"\nUser data: {user_data}")

    return REG_EXIT


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
                                    reply_markup=ReplyKeyboardMarkup([[KeyboardButton(answers.GOT_IT)]],
                                                                     one_time_keyboard=True, resize_keyboard=True))

    return REG_EXIT
