from telegram.ext import ContextTypes, ConversationHandler
from loger_config import logger
from Database.db_function import update_link_by_subject
from telegram.constants import ParseMode
from Services.messages import RoutineChoice

from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    KeyboardButton
)

from Database.db_function_user import (
    list_lessons,
    check_user_group,
    users_nickname_by_group,
    transfer_role,
    get_userid_by_nickname,
    count_moderators
)

from Services.conversation_states import (
    CONTROLS_CHOOSE_LESSON,
    CONTROLS_UPDATE_LINK,
    CHECK_CORRECT,
    CONTROLS_CHOOSE_USER,
    CHECK_ROLE_CORRECT
)

answers = RoutineChoice.Answers

chosen_lesson = int()
chosen_user = int()
chosen_link = str()


async def choose_lesson_from_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """S"""
    current_lesson_id = 0
    user = update.effective_user
    logger.info(f"User: {user.username}, user_id: {user.id}. The user requested a change lesson link.")
    lessons = list_lessons(check_user_group(user.id))
    if len(lessons) == 0:
        text = "У базі нема розкладу для Вашої групи. \nМожливо Ви вказали не дійсну групу, або розкладу ще немає."
        await context.bot.send_message(chat_id=user.id, text=text, parse_mode=ParseMode.HTML)
        return ConversationHandler.END

    text = f"<b>Виберіть предмет, щоб змінити посилання на нього:</b>" \
           f"\n\n{current_lesson_id + 1}. {lessons[current_lesson_id]}"

    for _ in range(len(lessons) - 1):
        current_lesson_id += 1
        text += f"\n\n{current_lesson_id + 1}. {lessons[current_lesson_id]}"
    await context.bot.send_message(chat_id=user.id, text=text, parse_mode=ParseMode.HTML)

    return CONTROLS_CHOOSE_LESSON


async def put_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global chosen_lesson

    chosen_lesson = int(update.message.text)
    user = update.effective_user
    lessons = list_lessons(check_user_group(user.id))
    if chosen_lesson - 1 > len(lessons) or chosen_lesson - 1 < 0:
        await context.bot.send_message(chat_id=user.id,
                                       text="Помилка! Введіть дійсний номер предмету.",
                                       parse_mode=ParseMode.HTML)
        return CONTROLS_CHOOSE_LESSON
    else:
        await context.bot.send_message(chat_id=user.id,
                                       text="Введіть посилання.\nЯкщо посилань більше одного - введіть їх через кому.",
                                       parse_mode=ParseMode.HTML)
        return CONTROLS_UPDATE_LINK


async def check_update_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global chosen_lesson
    global chosen_link

    chosen_link = update.message.text
    user = update.effective_user
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text=answers.GAME_START, callback_data="confirm"),
                                          InlineKeyboardButton(text=answers.SETTINGS_DENY,
                                                               callback_data="cancel_change")]])
    text = f"Підтвердіть зміну: " \
           f"\n{chosen_lesson}. {list_lessons(check_user_group(user.id))[chosen_lesson - 1]} - {chosen_link}"

    await context.bot.send_message(chat_id=user.id,
                                   text=text,
                                   parse_mode=ParseMode.HTML, reply_markup=reply_markup)
    return CHECK_CORRECT


async def update_link_db(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global chosen_lesson
    global chosen_link
    query = update.callback_query
    user = update.effective_user
    update_link_by_subject(check_user_group(user.id), list_lessons(check_user_group(user.id))[chosen_lesson - 1],
                           chosen_link)
    await query.edit_message_text(text="Успішно змінено ✅")

    return ConversationHandler.END


async def choose_user_from_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """S"""
    current_user = 0
    user = update.effective_user
    logger.info(f"User: {user.username}, user_id: {user.id}. The user requested a change lesson link.")
    users = users_nickname_by_group(check_user_group(user.id))

    if len(users) == 0:
        text = "У Вашій групі нема користувачів, яким можна передати Вашу роль."
        await context.bot.send_message(chat_id=user.id, text=text, parse_mode=ParseMode.HTML)
        return ConversationHandler.END

    text = f"<b>Виберіть користувача щоб передати роль:</b>\n\n{current_user + 1}. {users[current_user]}"
    for _ in range(len(users) - 1):
        current_user += 1
        text += f"\n{current_user + 1}. {users[current_user]}"
    await context.bot.send_message(chat_id=user.id, text=text, parse_mode=ParseMode.HTML,
                                   reply_markup=ReplyKeyboardRemove())

    return CONTROLS_CHOOSE_USER


async def check_update_role(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global chosen_user
    chosen_user = int(update.message.text)
    user = update.effective_user
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text=answers.GAME_START, callback_data="confirm"),
                                          InlineKeyboardButton(text=answers.SETTINGS_DENY,
                                                               callback_data="cancel_change")]])
    users = users_nickname_by_group(check_user_group(user.id))
    if chosen_user - 1 > len(users) or chosen_user - 1 < 0:
        await context.bot.send_message(chat_id=user.id,
                                       text="Помилка! Введіть дійсний номер юзера.",
                                       parse_mode=ParseMode.HTML)
        return CONTROLS_CHOOSE_USER
    else:
        await context.bot.send_message(chat_id=user.id,
                                       text=f"Підтвердіть передачу ролі: \n{chosen_user}. {users[chosen_user - 1]}",
                                       parse_mode=ParseMode.HTML, reply_markup=reply_markup)
        return CHECK_ROLE_CORRECT


async def update_role_db(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global chosen_user
    user = update.effective_user
    moderators = count_moderators(check_user_group(user.id))
    reply_markup = ReplyKeyboardMarkup([[KeyboardButton(text=answers.GOT_IT)]],
                                       one_time_keyboard=True,
                                       resize_keyboard=True)
    text = "Помилка! Ви не можете передати свою роль у цій групі.\nПоверніться у свою вихідну групу."

    if moderators not in range(0, 4):
        await context.bot.send_message(chat_id=user.id,
                                       text=text,
                                       parse_mode=ParseMode.HTML, reply_markup=reply_markup)
        return ConversationHandler.END

    transfer_role(user.id, get_userid_by_nickname(users_nickname_by_group(check_user_group(user.id))[chosen_user - 1]))
    await context.bot.send_message(chat_id=user.id, text="Успішно передано ✅", reply_markup=reply_markup)

    return ConversationHandler.END
