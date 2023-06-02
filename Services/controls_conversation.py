from telegram import Update, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, ConversationHandler
from loger_config import logger
from Database.db_function_user import list_lessons, check_user_group
from telegram.constants import ParseMode
from Services.messages import RoutineChoice
from Services.schedule_builder import ScheduleBuilder

answers = RoutineChoice.Answers
CONTROLS_CHOOSE_LESSON = chr(25)
#current_lesson_id: int = 0
#reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text="<", callback_data="previous_lesson"),
#                                      InlineKeyboardButton(text=">", callback_data="next_lesson")]])


async def choose_lesson_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("asdasd")



#async def previous_lesson(update: Update, context: ContextTypes.DEFAULT_TYPE):
#    global current_lesson_id
#    user = update.effective_user
#    lessons = list_lessons(check_user_group(user.id))
#    if current_lesson_id == 0:
#        current_lesson_id = len(lessons) - 1
#    else:
#        current_lesson_id -= 1
#
#    await _build_choose_lesson_message(update, context, current_lesson_id)
#
#
#async def next_lesson(update: Update, context: ContextTypes.DEFAULT_TYPE):
#    global current_lesson_id
#    user = update.effective_user
#    lessons = list_lessons(check_user_group(user.id))
#    if current_lesson_id == len(lessons) - 1:
#        current_lesson_id = 0
#    else:
#        current_lesson_id += 1
#
#    await _build_choose_lesson_message(update, context, current_lesson_id)
#
#
#async def _build_choose_lesson_message(update: Update, context: ContextTypes.DEFAULT_TYPE, lesson_id: int):
#    global reply_markup
#    user = update.effective_user
#    lessons = list_lessons(check_user_group(user.id))
#    query = update.callback_query
#    text = f"<b>Виберіть предмет, щоб змінити посилання на нього.</b>\n\n{current_lesson_id+1}. {lessons[lesson_id]}"
#    await query.edit_message_text(text=text, parse_mode=ParseMode.HTML,
#                                  reply_markup=reply_markup)
#