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
    await message.answer(f'Привет!!! Я бот "Угадай число". Правила игры таковы я загадываю число,'
                         f'а ты его должен угадать за выбранное тобой количество попыток.\n'
                         f'Если вдруг ты забудешь правила введи /help.')

#Реализуем хэндлер /help.
@dp.message(Command(commands='help'))
async def process_help(message:Message):
    await message.answer(f'Этот бот служит для развлекательных целей.\n'
                         f'Основная задача бота - это игра в "Угадай число".\n'
                         f'Для старта игры введи "Да", "Игра", "Сыграем".\n'
                         f'Для выхода из игры введи /cancel.\n'
                         f'Для вывода статистики введите /stat.')

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
@dp.message(F.text.lower().in_(['да', 'давай', 'сыграем', 'игра', 'давай сыграем', 'сыграть']))
async def process_yes(message:Message):
    if not user['in_game']:
        user['in_game']=True
        user['attempts']=ATTEMPTS
        user['secret_number']=random_number()
        await message.answer('Я так рад с тобой сыграть.')
    else:
        await message.answer('Мы с Вами уже так играем. Введите число от 1 до 100.')

#Реализуем функцию по отказу пользователя от игры.
@dp.message(F.text.lower().in_(['нет', 'не хочу', 'в другой раз', 'не буду']))
async def process_no(message:Message):
    if not user['in_game']:
        await message.answer(f'Очень жаль. Я очень хочу с тобой сыграть.'
                             f'Если захочешь сыграть просто введи \'Игра\'')
    else:
        await message.answer('Мы с Вами уже так играем. Введите число от 1 до 100.')

#Реализуем игровой процесс.
@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_guess_the_number(message:Message):
    if user['in_game']:
        if user['secret_number']==int(message.text):
            user['count_game']+=1
            user['count_win']+=1
            user['in_game']=False
            message.answer('Ура!!! Ты угадал!')
        elif user['secret_number']>int(message.text):
            user['attempts']-=1
            message.answer('Загаданное число больше')
        elif user['secret_number']<int(message.text):
            user['attempts']-=1
            message.answer('Загаданное число меньше')
        if user['attempts']==0:
            user['in_game']=False
            user['count_game']+=1
            message.answer('Ты не угадал. Попробуй ещё раз.')
    else:
        message.answer('Мы еще не играем.')

#Функция которая отлавливает все оставшиеся варианты.
@dp.message()
async def process_all(message:Message):
    if user['in_game']:
        message.answer(f'Мы с Вами играем. Введите число от 1 до 100.'
                       f'Или команду /cancel.')
    else:
        message.answer('Я могу только играть в игру "Угадай число"')

if __name__=='__main__':
    dp.run_polling(bot)