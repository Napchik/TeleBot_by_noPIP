#
# Description: some decr
#
# Authors: Evhen Miholat
#
# version 0.0
# a telegram bot dice game
from aiogram import Bot, Dispatcher, types, executor
from asyncio import sleep
from dotenv import load_dotenv, find_dotenv
import os
import telegram
from telegram.ext import ContextTypes, ApplicationBuilder, CommandHandler,CallbackQueryHandler, ConversationHandler, MessageHandler, filters
import logging
from DataBase.db_function_game import user_check, update_score_by_user, add_new_gamer,update_games_by_user, score_by_gamer, games_by_gamer, top_gamers



# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO
# )
async def start(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.id
    if user_check(name):
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Привіт, граємо ?")
        return 2
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Привіт, бачу, ви тут вперше. Як вас звати ?")
        return 1




async def add_gamer(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.text
    add_new_gamer(update.effective_user.id,user_name)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Ви успішно додані списку гравців, тепер ви можете відслідковувати свій рейтинг серед всіх участників гри."
                                        f"{user_name}починаємо грати ?")
    return 2

async def dice_game(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
        user_answer = update.message.text
        if user_answer.lower() == 'так' :
            await context.bot.send_message(chat_id=update.effective_chat.id, text='Ви підкидаєте кубик')
            first_roll = await context.bot.send_dice(chat_id=update.effective_chat.id)
            data_user = first_roll["dice"]["value"]
            await sleep(5)
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text='Бот підкидаєте кубик')
            second_roll = await context.bot.send_dice(chat_id=update.effective_chat.id)
            data_bot = second_roll["dice"]["value"]
            await sleep(5)
            if data_bot > data_user:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text='Ви програли')
                update_games_by_user(update.effective_user.id,games_by_gamer(update.effective_user.id))
                games = games_by_gamer(update.effective_user.id)
                await context.bot.send_message(chat_id=update.effective_chat.id,
                                               text=f'Кількість виграшів: {score_by_gamer(update.effective_user.id)}\nКількість спроб: {games}')



            elif data_user > data_bot:
                await  context.bot.send_message(chat_id=update.effective_chat.id,
                                           text='Ви виграли')
                wins_by_user = score_by_gamer(update.effective_user.id)
                wins_by_user+=1
                update_score_by_user(update.effective_user.id,wins_by_user)
                update_games_by_user(update.effective_user.id, games_by_gamer(update.effective_user.id))
                games = games_by_gamer(update.effective_user.id)
                await context.bot.send_message(chat_id=update.effective_chat.id,
                                               text=f'Кількість виграшів: {score_by_gamer(update.effective_user.id)}\nКількість спроб: {games}')


            else:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text='Нічия')
                update_games_by_user(update.effective_user.id, games_by_gamer(update.effective_user.id))
                games = games_by_gamer(update.effective_user.id)
                await context.bot.send_message(chat_id=update.effective_chat.id,
                        text=f'Кількість виграшів: {score_by_gamer(update.effective_user.id)}\nКількість спроб: {games}')
            await sleep(3)
            await context.bot.send_message(chat_id=update.effective_chat.id, text='Граємо ще раз ? (так/ні)')
            return 2
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='Тоді йди на пари')
            return ConversationHandler.END

async def gamers_top(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    top_list = top_gamers()
    str = 'Топ 10 гравців:'
    for i in range(len(top_list[0])):
        str += f"\n{i+1}) {top_list[1][i]}     -    {top_list[0][i]}"


    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=str)



async def stop(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="До наступної гри !")
    return ConversationHandler.END



conv_handler = ConversationHandler(entry_points=[CommandHandler('start', start)],
                                   states={1: [MessageHandler(filters.TEXT, add_gamer)],
                                           2: [MessageHandler(filters.TEXT, dice_game)]},

                                   fallbacks=[CommandHandler('stop', stop)])


# if __name__ == '__main__':
#     application = ApplicationBuilder().token('5400848360:AAFakNgh5y2MyS2DVXEoGHvpLuBXSsduOq4').build()
#
#     start_handler = CommandHandler('start', start)
#     top_handler = CommandHandler('top', gamers_top)
#     stop_handler = CommandHandler('stop', stop)
#     application.add_handler(conv_handler)
#     application.add_handler(start_handler)
#     application.add_handler(top_handler)
#     application.add_handler(stop_handler)
#     application.run_polling()


