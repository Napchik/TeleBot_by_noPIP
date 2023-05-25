"""
    Description: Game logics. (BETA! EDIT IN FUTURE)

    Author: Evhen Miholat
    Version: 0.1
"""

from asyncio import sleep
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from telegram.constants import ParseMode
from loger_config import logger
from Database.db_function_game import (
    user_check, update_score_by_user, add_new_gamer, update_games_by_user,
    score_by_gamer, games_by_gamer, top_gamers
)

ADD_PLAYER = chr(13)
MAIN_GAME = chr(14)


async def game_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Entry Point for Game"""
    user = update.message.from_user

    logger.info(f"User: {user.username}, user_id: {user.id}. The user has started game.")

    if user_check(user.id):
        await context.bot.send_message(chat_id=user.id, text="Привіт, граємо? (так/ні)")

        return MAIN_GAME

    await context.bot.send_message(chat_id=user.id, text="Привіт, бачу, ви тут вперше. Як вас звати?")

    return ADD_PLAYER


async def add_player(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add Player to Database"""
    user_name = update.message.text
    user = update.message.from_user
    add_new_gamer(update.effective_user.id, user_name)

    logger.info(f"User: {user.username}, user_id: {user.id}. The user has been added to game database.")

    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f"Ви успішно додані до списку гравців, тепер ви можете \
                                          відслідковувати свій рейтинг серед всіх участників гри."
                                        f"\n{user_name}, починаємо грати? (так/ні)")
    return MAIN_GAME


async def dice_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Main Game (DICE)"""
    user_answer = update.message.text
    user = update.message.from_user

    logger.info(f"User: {user.username}, user_id: {user.id}. The user has started the game of dice.")

    if user_answer.lower() == 'так':

        async def roll_dice(chat_id, message) -> int:
            await context.bot.send_message(chat_id=chat_id, text=message)
            data = await context.bot.send_dice(chat_id=chat_id)
            return data["dice"]["value"]

        data_user = await roll_dice(update.effective_chat.id, 'Ви підкидаєте кубик')
        await sleep(5)
        data_bot = await roll_dice(update.effective_chat.id, 'Бот підкидає кубик')
        await sleep(4)

        if data_bot > data_user:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='Ви програли')

        elif data_user > data_bot:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='Ви виграли')
            update_score_by_user(update.effective_user.id, score_by_gamer(update.effective_user.id) + 1)

        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='Нічия')

        update_games_by_user(update.effective_user.id, games_by_gamer(update.effective_user.id) + 1)
        games = games_by_gamer(update.effective_user.id)
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f'Кількість виграшів: {score_by_gamer(update.effective_user.id)}\n'
                                            f'Кількість спроб: {games}')

        await context.bot.send_message(chat_id=update.effective_chat.id, text='Граємо ще раз? (так/ні)')
        return MAIN_GAME

    elif user_answer.lower() == 'ні':

        logger.info(f"User: {user.username}, user_id: {user.id}. The user has ended the game.")
        await context.bot.send_message(chat_id=update.effective_chat.id, text='До нової зустрічі!')
        return ConversationHandler.END


async def top_players(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Top 10 Players in Database"""
    user = update.message.from_user

    logger.info(f"User: {user.username}, user_id: {user.id}. The user requested list of top players.")

    top_list = top_gamers()
    top10 = '```\nТоп 10 гравців:'

    for i in range(len(top_list[0])):
        top10 += "\n{0:>2}) {2:<10}  -  {1}".format(i + 1, top_list[0][i], top_list[1][i][:10:])

    top10 += '```'

    await context.bot.send_message(chat_id=update.effective_chat.id, text=top10, parse_mode=ParseMode.MARKDOWN)
    await context.bot.send_message(chat_id=update.effective_chat.id, parse_mode=ParseMode.HTML,
                                   text='Щоб розпочати гру, напишіть <b>/start_game</b>')


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """End Game"""
    user = update.message.from_user

    logger.info(f"User: {user.username}, user_id: {user.id}. The user has ended the game.")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="До наступної гри!")
    return ConversationHandler.END
