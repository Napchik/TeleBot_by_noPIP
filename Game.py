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
from telegram.ext import ContextTypes, ApplicationBuilder, CommandHandler,CallbackQueryHandler
import logging




# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO
# )


async def dice_game(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,text="Привіт, давай грати")
    await sleep(1)
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Ви підкидаєте кубик')
    first_roll = await context.bot.send_dice(chat_id=update.effective_chat.id)
    first_roll
    print(first_roll)
    data_user = first_roll["dice"]["value"]
    await sleep(5)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text='Бот підкидаєте кубик')
    second_roll = await context.bot.send_dice(chat_id=update.effective_chat.id)
    second_roll
    data_bot = second_roll["dice"]["value"]
    await sleep(5)
    if data_bot > data_user:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text='Ви програли')

    elif data_user > data_bot:
        await  context.bot.send_message(chat_id=update.effective_chat.id,
                                   text='Ви виграли')


    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text='Нічия')




# if __name__ == '__main__':
#     application = ApplicationBuilder().token('Token').build()
#
#     start_handler = CommandHandler('start', start)
#     application.add_handler(start_handler)
#
#     application.run_polling()



