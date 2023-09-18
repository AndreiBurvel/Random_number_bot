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
dp.message(Command(commands='/help'))
async def process_help(message:Message):
    await message.answer('')

#Реализуем хэндлер /stat - для вывода статистики пользователя.

