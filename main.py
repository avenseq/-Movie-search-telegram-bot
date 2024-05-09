from aiogram.types import Message, CallbackQuery, KeyboardButton
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ParseMode
from aiogram import types
from aiogram import F
from random import *
from datetime import datetime
from asyncio import sleep
import requests
from bs4 import BeautifulSoup
import logging
import asyncio
import sqlite3 as sq
logging.basicConfig(level=logging.INFO)
router: Router = Router()
BOT_TOKEN = '6840000709:AAFhJxb9yqK5hkDrTD8P72qe9DwywfDy9lk'
films_repeat = []
films_names = {}

genres_dict_key_eng = {'animation': 'анимация', 'family': 'семейный', 'drama': 'драма',
                       'triller': 'триллер', 'actionmovie': 'боевик', 'adventure': 'приключения', 'fantasy': 'фэнтези',
                       'biography': 'биография', 'historical': 'исторический', 'comedy': 'комедия', 'melodrama': 'мелодрама', 'musical':'мюзикл',
                       'mistic': 'мистика', 'anime': 'аниме', 'music': 'музыка', 'military': 'военный',
                       'criminal': 'криминал', 'fairytale':'сказка', 'detective':'детектив',
                       'sport': 'спорт', 'western':'вестерн', 'horror': 'ужасы', 'documentary': 'документальный', 'nuar':'нуар', 'children': 'детский', 'concert': 'концерт'} #!!!!!!!!!!!!!!!!!!!

genres_dict_key_rus = {'анимация': 'animation'}

all_genges = ['анимация', 'семейный', 'драма', 'триллер', 'боевик', 'приключения', 'фэнтези', 'фантастика', 'биография', 'исторический', 'комедия', 'мелодрама', 'мюзикл', 'мистика', 'аниме', 'короткометражный', 'музыка', 'военный', 'криминал', 'сказка', 'детектив', 'спорт', 'вестерн', 'ужасы', 'документальный', 'нуар', 'детский', 'концерт']

with sq.connect("data_films.db") as con:
    #con.row_factory = sq.Row
    cur = con.cursor()
    cur.execute('SELECT MAX(film_id) FROM ifilms')
    max_number = cur.fetchone()[0]
    cur.execute("SELECT film_id, name, year, duration, href, contry, about, rate, genre FROM ifilms")
    for cur in cur.fetchall():
        films_names[cur[0]] = [cur[i] for i in range(1, 9)]


# #print(films_names)
# for i in films_names:                                 #НАХОЖДЕНИЕ ВСЕХ ЖАНРОВ
#     genres = films_names[i][7].split('_')
#     for j in genres:
#         if j not in all_genges:
#             all_genges.append(j)
# print(all_genges)


def keyboard_genres():
    #'анимация', 'семейный', 'драма', 'триллер', 'боевик', 'приключения', 'фэнтези', 'фантастика', 'биография', 'исторический', 'комедия
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text= 'Анимация', callback_data='genre_animation')
    keyboard_builder.button(text='Семейный', callback_data='genre_family')
    keyboard_builder.button(text='Драма', callback_data='genre_drama')
    keyboard_builder.button(text='Триллер', callback_data='genre_triller')
    keyboard_builder.button(text='Боевик', callback_data='genre_actionmovie')
    keyboard_builder.button(text='Приключения', callback_data='genre_adventure')
    keyboard_builder.button(text='Фэнтези', callback_data='genre_fantasy')
    keyboard_builder.button(text='Биография', callback_data='genre_biography')
    keyboard_builder.button(text='Исторический', callback_data='genre_historical')
    keyboard_builder.button(text='Комедия', callback_data='genre_comedy')
    keyboard_builder.button(text='Мелодрама', callback_data='genre_melodrama')
    keyboard_builder.button(text='Мюзикл', callback_data='genre_musical')
    keyboard_builder.button(text='Мистика', callback_data='genre_mistic')
    keyboard_builder.button(text='Музыка', callback_data='genre_music')
    keyboard_builder.button(text='Военный', callback_data='genre_military')
    keyboard_builder.button(text='Криминал', callback_data='genre_criminal')
    keyboard_builder.button(text='Сказка', callback_data='genre_fairytale')
    keyboard_builder.button(text='Детектив', callback_data='genre_detective')
    keyboard_builder.button(text='Спорт', callback_data='genre_sport')
    keyboard_builder.button(text='Вестерн', callback_data='genre_western')
    keyboard_builder.button(text='Ужасы', callback_data='genre_horror')
    keyboard_builder.button(text='Документалка', callback_data='genre_documentary')
    keyboard_builder.button(text='Нуар', callback_data='genre_nuar')
    keyboard_builder.button(text='Детский', callback_data='genre_children')
    keyboard_builder.button(text='Концерт', callback_data='genre_concert')
    keyboard_builder.adjust(3)
    return keyboard_builder.as_markup()


def keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text = 'Случайный фильм', callback_data='random_film')
    keyboard_builder.button(text='Выбрать жанр', callback_data='genres_film')
    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup()

@router.message(CommandStart())
async def start_chat(message: Message):
    await  message.answer(text='Привет! Этот бот, который рандомно подберет тебе фильм! Нажми на кнопку, чтобы подобрать фильм!', reply_markup=keyboard())
    while True:
        await asyncio.sleep(1)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        if current_time == '12:00:00' or current_time == '20:00:00':
            rand_num = randint(1, len(films_names))
            await message.answer(f'Фильм сегодняшнего дня -  "{films_names[rand_num][0]}". Подробнее на {films_names[rand_num][3]}')


@router.callback_query(F.data == 'genres_film')
async def get_genres(call: CallbackQuery):
    await call.message.answer('Выберете жанр фильма:', reply_markup = keyboard_genres())


@router.callback_query(F.data.startswith('genre_'))
async def get_genres(call: CallbackQuery):
    genre = genres_dict_key_eng[call.data.split('_')[1]]
    good_film = []
    repeat_film = []
    for i in films_names:
        film = films_names[i]
        if genre in film[7].split('_'):
            good_film.append(film[0])
    s = f'Фильмы в жанре "{genre.title()}": \n\n'
    # count = 1
    # len_films = len(good_film)
    # while True:
    #     s+= f'{count}: ' + good_film[count-1] + '\n'
    #     count+=1
    #     if count == 51:
    #         count = 1
    #         break

    for i in range(1, len(good_film)+1):
        if i >= 51:
            break
        while True:
            rand_num = randint(0, len(good_film)-1)
            if good_film[rand_num] not in repeat_film:
                s += f'{i}. ' + good_film[rand_num] + '\n'
                repeat_film.append(good_film[rand_num])
                break
       # s += f'{i}: ' + good_film[i-1][0] + good_film[i-1][1] + '\n'
    await  call.message.answer(s, reply_markup=keyboard())
   #await call.message.answer(*[(f'{i}:' + good_film[i] + '\n') for i in range(len(good_film))])






@router.callback_query(F.data == 'random_film')
async def random_film(call: CallbackQuery):
    rand = randint(1, max_number)
    film = films_names[rand]
    name = film[0]
    year = film[1]
    duration=film[2]
    href = film[3]
    contry = film[4]
    about = film[5]
    rate = film[6]
    genre = ' ' + ', '.join(film[7].split('_'))

    await call.message.answer(f'Вам стоит посмотреть: "{name}" '
                              f'\nГод выпуска: {year} '
                              f'\nДлительность: {duration} '
                              f'\nСтрана производства: {contry} '
                              f'\n{rate} '
                              f'\nЖанр:{genre}'
                              f'\n\n\nО чем фильм: {about}'
                              f'\nПодробнее на сайте: {href}'
                              f'\n', reply_markup=keyboard())





async def start():
    bot: Bot = Bot(token=BOT_TOKEN)
    dp: Dispatcher = Dispatcher()

    dp.include_router(router=router)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(start())
