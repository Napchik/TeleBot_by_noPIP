"""
    Description: Contains logic of registration conversation.

    Author: Ivan Maruzhenko
    Version: 0.2
"""

from telegram.constants import ParseMode
from loger_config import logger
from Services.messages import START, REGISTRATION_INFO, MODERATOR_INFO, RoutineChoice
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler
from Database.db_function_user import choose_role, add_user


class UserData:
    def __init__(self, user_id):
        self.user_id: int = user_id
        self.name: str | None = None
        self.surname: str | None = None
        self.username: str | None = None
        self.group: str | None = None
        self.schedule_mode: int | None = None
        self.role: str | None = None

    def send_data(self):
        add_user(self.name, self.surname, self.username, self.user_id, self.group, self.schedule_mode, self.role)


GROUP, ROUTINE, REG_INFO, REG_EXIT = map(chr, range(4))
answers = RoutineChoice.Answers
results = RoutineChoice.Results
users_dictionary: dict[int: UserData] = {}


async def start_reg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Displays the first welcome message for the user"""
    user = update.message.from_user
    global users_dictionary

    users_dictionary[user.id] = UserData(user_id=user.id)
    user_data = users_dictionary[user.id]
    user_data.name = user.first_name
    user_data.surname = user.last_name
    user_data.username = user.username
    user_data.user_id = user.id

    logger.info(f"User: {user.username}, user_id: {user.id}. The user has started conversation.")

    await context.bot.send_message(chat_id=user.id, text=START, parse_mode=ParseMode.HTML,
                                   reply_markup=ReplyKeyboardRemove())

    return GROUP


async def group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Prompts the user for their group"""
    user = update.message.from_user
    global users_dictionary
    group_name: str = update.message.text.upper()

    user_data = users_dictionary[user.id]
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
    global users_dictionary
    user_data = users_dictionary[user.id]

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
    global users_dictionary
    user_data = users_dictionary[user.id]

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

    del users_dictionary[user.id]

    return REG_EXIT


async def misunderstand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    logger.info(f"User: {user.username}, user_id: {user.id}. Invalid input: {update.message.text}")

    await update.message.reply_text(text="Вибачте, я Вас не розумію. Спробуйте знову.",
                                    parse_mode=ParseMode.HTML)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    global users_dictionary

    logger.info(f"User: {user.username}, user_id: {user.id}. The user has canceled the conversation.")

    await update.message.reply_text(text="❌ Ви перервали реєстрацію."
                                         "\nЩоб продовжити спілкування з ботом - напишіть /start",
                                    parse_mode=ParseMode.HTML,
                                    reply_markup=ReplyKeyboardRemove())

    del users_dictionary[user.id]
    return ConversationHandler.END
