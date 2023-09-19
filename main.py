import random

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

import os
from dotenv import load_dotenv, find_dotenv

#Импортируем токен из файла переменных среды.
load_dotenv(find_dotenv())
BOT_TOKEN:str = os.getenv('TOKEN')

#Инициализируем бота и диспетчера.
bot=Bot(BOT_TOKEN)
dp=Dispatcher()

#Реализуем функцию рандомных чисел.
def random_number():
    return random.randint(1, 100)

#Количество попыток на угадывание числа.
ATTEMPTS=5

#Создаём словарь для сохранения данных пользователя.
user:dict = {
            'in_game':False, 'secret_number':None,
            'attempts':None, 'count_game':0, 'count_win':0
              }

#Реализуем хэндлер /start.
@dp.message(CommandStart())
async def process_start(message:Message):
    await message.answer('''Привет!!! Я бот "Угадай число". Правила игры таковы я загадываю число,
                         а ты его должен угадать за выбранное тобой количество попыток.
                         Если вдруг ты забудешь правила введи /help.''')

#Реализуем хэндлер /help.
@dp.message(Command(commands='help'))
async def process_help(message:Message):
    await message.answer('h')

#Реализуем хэндлер /stat - для вывода статистики пользователя.
@dp.message(Command(commands='stat'))
async def process_stat(message:Message):
    await message.answer(f'Количество сыгранных игр {user["count_game"]}, количество побед {user["count_win"]}')

#Реализуем хэндлер /cancel - для выхода из игры.
@dp.message(Command(commands='cancel'))
async def process_cancel(message:Message):
    if user['in_game']:
        user['in_game']=False
        await message.answer('Игра окончена. Так жаль.')
        await message.answer('Если захочешь снова играть введи \"Игра\"')
    else:
        await message.answer('Мы ещё не играем.')

#Реализуем функцию по согласию пользователя на игру.
@dp.message(F.text.lower().in_['да', 'давай', 'сыграем', 'игра', 'давай сыграем', 'сыграть'])
async def process_yes(message:Message):
    if not user['in_game']:
        user['in_game']=True
        user['attempts']==ATTEMPTS
        

if __name__=='__main__':
    dp.run_polling(bot)