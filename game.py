"""
    Description: Game logics.

    Author: Evhen Miholat
    Version: 0.5
"""

from asyncio import sleep
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, ConversationHandler
from telegram.constants import ParseMode
from loger_config import logger
from Services.messages import RoutineChoice
from Database.db_function_game import (
    user_check,
    update_score_by_user,
    add_new_gamer,
    update_games_by_user,
    score_by_gamer,
    games_by_gamer,
    top_gamers,
    name_by_gamer,
    change_name_gamer
)
from Services.conversation_states import (
    ADD_PLAYER,
    CHANGE_NAME,
    DICE
)

answers = RoutineChoice.Answers


async def game_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Entry Point for Game"""
    user = update.message.from_user
    logger.info(f"User: {user.username}, user_id: {user.id}. The user has started game.")
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text=answers.GAME_START, callback_data="game_start"),
                                          InlineKeyboardButton(text=answers.GAME_STOP, callback_data="game_stop")]])

    if user_check(user.id):
        await update.message.reply_text(text=f"Привіт {name_by_gamer(user.id)}, граємо?", reply_markup=reply_markup)
        return DICE

    await context.bot.send_message(chat_id=user.id, text="Привіт, бачу, ви тут вперше. Як Вас звати?")
    return ADD_PLAYER


async def add_player(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add Player to Database"""
    user_name = update.message.text
    user = update.message.from_user
    add_new_gamer(update.effective_user.id, user_name)
    logger.info(f"User: {user.username}, user_id: {user.id}. The user has been added to game database.")
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text=answers.GAME_START, callback_data="game_start"),
                                          InlineKeyboardButton(text=answers.GAME_STOP, callback_data="game_stop")]])

    await update.message.reply_text(text=f"Ви успішно додані до списку гравців, тепер ви можете \
                                           відслідковувати свій рейтинг серед всіх участників гри."
                                         f"\n{user_name}, починаємо грати?",
                                    reply_markup=reply_markup)
    return DICE


async def change_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Changing player name"""
    user = update.message.from_user
    if not user_check(user.id):
        await context.bot.send_message(chat_id=user.id, text="Спочатку пройдіть реестрацію!\nВведіть своє ім'я.")
        return ADD_PLAYER
    await context.bot.send_message(chat_id=user.id, text="Введіть нове ім'я.")
    return CHANGE_NAME


async def update_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Triggers function to update database"""
    new_user_name = update.message.text
    user = update.message.from_user
    change_name_gamer(user.id, new_user_name)
    await context.bot.send_message(chat_id=user.id, text="Ім'я змінено успішно ✅")


async def dice_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Main Game (DICE)"""

    async def roll_dice(chat_id, message) -> int:
        await context.bot.send_message(chat_id=chat_id, text=message)
        data = await context.bot.send_dice(chat_id=chat_id)
        return data["dice"]["value"]

    user = update.effective_user
    logger.info(f"User: {user.username}, user_id: {user.id}. The user has started the game of dice.")

    data_user = await roll_dice(update.effective_chat.id, 'Ви 👨 підкидаєте кубик')
    await sleep(5)

    data_bot = await roll_dice(update.effective_chat.id, 'Бот 🤖 підкидає кубик')
    await sleep(5)

    if data_bot > data_user:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Бот виграв 🌧')

    elif data_user > data_bot:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Ви виграли 🎉')
        update_score_by_user(update.effective_user.id, score_by_gamer(update.effective_user.id) + 1)

    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Нічия 🤯')
        update_score_by_user(update.effective_user.id, score_by_gamer(update.effective_user.id) + 1)

    update_games_by_user(update.effective_user.id, games_by_gamer(update.effective_user.id) + 1)
    games = games_by_gamer(update.effective_user.id)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f'Кількість виграшів: {score_by_gamer(update.effective_user.id)} 🥇\n'
                                        f'Кількість спроб: {games} 🧩')

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text=answers.GAME_START, callback_data="game_start"),
                                          InlineKeyboardButton(text=answers.GAME_STOP, callback_data="game_stop")]])

    await context.bot.send_message(chat_id=update.effective_chat.id, text='Граємо ще раз?', reply_markup=reply_markup)
    return DICE


async def top_players(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Top 10 Players in Database"""
    user = update.message.from_user
    logger.info(f"User: {user.username}, user_id: {user.id}. The user requested list of top players.")
    top_list = top_gamers()
    top10 = '```\nТоп 10 гравців 🏆:'

    for i in range(len(top_list[0])):
        top10 += "\n{0:>2}) {2:<10}  -  {1}".format(i + 1, top_list[0][i], top_list[1][i][:10:])

    top10 += '```'

    await context.bot.send_message(chat_id=update.effective_chat.id, text=top10, parse_mode=ParseMode.MARKDOWN)


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """End Game"""
    user = update.effective_user
    query = update.callback_query
    logger.info(f"User: {user.username}, user_id: {user.id}. The user has ended the game.")
    await query.edit_message_text(text="До наступної гри!")
    return ConversationHandler.END
