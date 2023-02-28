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

load_dotenv(find_dotenv())

API_TOKEN = str(os.getenv("TOKEN"))



users = []
bot = Bot(API_TOKEN)
dp = Dispatcher(bot)  # function to get event from user



@dp.message_handler() # creating decorator to handle the concret message type from user
async def dice(message: types.Message):
    await bot.send_message(message.from_user.id, f'Привіт, {message.from_user.username}, давай грати')
    await sleep(1)
    await bot.send_message(message.from_user.id, 'Ваш кубик підкидається')
    dice_user = await bot.send_dice(message.from_user.id)
    print(dice_user)
    data_user = dice_user['dice']['value']
    await sleep(5)
    await bot.send_message(message.from_user.id, 'Бот підкидає кубик')
    dice_bot = await bot.send_dice(message.from_user.id)
    data_bot = dice_bot['dice']['value']
    await sleep(5)

    if data_bot > data_user:

        await bot.send_message(message.from_user.id, "Ви програли(")
    elif data_user > data_bot:
        await  bot.send_message(message.from_user.id, "Вітаю ! Ви виграли")

    else:
        await bot.send_message(message.from_user.id, f"Нічия!")






if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
