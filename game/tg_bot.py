import sqlite3
import random
from datetime import datetime

import telebot
from telebot import types
from game.config import token

valid_commands = ['помощь', 'с', 'ю', 'з', 'в', 'поднять', 'положить', 'расположение']

movements_available = 28
HELP = '''
Семь пещер образуют лабиринт. В каждой пещере находится ящик с сокровищами.
Вы должны собрать все сокровища в одну пещеру за 28 движений.
Можно переносить одновременно только один ящик с сокровищами.

Эти команды понятны компьютеру:
помощь: Информация о правилах игры
<b>с, в, ю, з</b>: двигаться в направлении С (север), В (восток), Ю (юг), З (запад)
<b>поднять</b>: Поднять сокровище
<b>положить</b>: Положить сокровище
<b>расположение</b>: Вывести текущее расположение сокровищ
Каждая команда - это одно движение

'''

MAP = '''
    С          _______________________________
  З + В        | 2   темная и | 4 туманная и |
    Ю          |   закопченая |   призрачная |
      _________|              |              |
      |          [Жевательная]   [Сендвичи]  |
      |    ____  [  резинка  ]   [        ]  |
______|   |____|_____    _____|_____    _____|
| 1 холодная и | 7 наполненная| 4  грязная и |
|       мокрая |      жуткими |      мрачная |
|              | привидениями |              |
|   [Золото]       [Монеты]       [Мусор]    |
|   [      ]       [      ]       [     ]    |
|_____    _____|_____    _____|_____    _____|  
| 6 наполненная| 5     пустаяя|     |   |
|      ужасными|    и страшная|     |   |        
|    призраками|              |_____|   |
| [Драгоценные]   [Горшки с]            |
| [   камни   ]   [ медом  ]   _________|
|______________|______________| 

'''

N = [2, 0, 0, 3, 7, 1, 2]
E = [7, 3, 0, 0, 4, 5, 4]
S = [6, 7, 4, 5, 0, 0, 5]
W = [0, 1, 2, 7, 6, 0, 1]

DS = ['Холодная и мокрая',
      'Темная и закоптелая',
      'Туманная и призрачная',
      'Грязная и мрачная',
      'Пустая и страшная',
      'Наполненная ужасными призраками',
      'Наполненная жуткими привидениями']

T = [1, 2, 3, 4, 5, 6, 7]
TS = ['Ящик с золотом',
      'Ящик жевательной резинки',
      'Ящик сандвичей',
      'Ящик мусора',
      'Ящик с медом',
      'Ящик с драгоценными камнями',
      'Ящик с монетами']

m = 0
c = 0
r = 0

bot = telebot.TeleBot(token)

conn = sqlite3.connect('game_stat.db3', check_same_thread=False)
cursor = conn.cursor()

main_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton('/newgame')
btn2 = types.KeyboardButton('/about')
main_keyboard.add(btn1, btn2)

game_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton('помощь')
btn2 = types.KeyboardButton('с')
btn3 = types.KeyboardButton('ю')
btn4 = types.KeyboardButton('з')
btn5 = types.KeyboardButton('в')
btn6 = types.KeyboardButton('поднять')
btn7 = types.KeyboardButton('положить')
btn8 = types.KeyboardButton('расположение')
game_keyboard.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8)


def insert_new_user(user_id: int, user_name: str, user_surname: str, username: str, date_register: datetime):
    cursor.execute(f'SELECT user_id FROM users WHERE user_id ={user_id}')
    if cursor.fetchone() is None:
        cursor.execute(
            'INSERT INTO users (user_id, user_name, user_surname, username, date_register) VALUES (?, ?, ?, ?, ?)',
            (user_id, user_name, user_surname, username, date_register))
        conn.commit()


def insert_result(user_id: int, date_result: datetime, movements: int, cave: int, done: bool):
    cursor.execute(
        'INSERT INTO results (user_id, date_result, movements, cave, done) VALUES (?, ?, ?, ?, ?)',
        (user_id, date_result, movements, cave, done))
    conn.commit()


def cave_description():
    fl = 0
    vtext = ''
    for k in range(7):
        if T[k] == r:
            vtext = TS[k]
            fl = 1
    if fl == 0:
        vtext = 'Ничего'
    text = f'Вы в пещере {r}\nЭто {DS[r - 1]} пещера\nВ ней находится:\n{vtext}'
    return text


@bot.message_handler(commands=['start'])
def start_command(message):
    text = f'<b>Приветствую, {message.chat.first_name}.</b>\nДобро пожаловать в игру "Поиски сокровищ"!\n' \
           f'Новая игра - /newgame\n' \
           f'О проекте - /about'
    bot.send_message(message.chat.id, text, parse_mode='html', reply_markup=main_keyboard)


@bot.message_handler(commands=['about'])
def about(message):
    text = 'О проекте. Написать разработчику. Придумать username в tg.'
    bot.send_message(message.chat.id, text)
    # keyboard = telebot.types.InlineKeyboardMarkup()
    # keyboard.add(
    #     telebot.types.InlineKeyboardButton(
    #         'Написать разработчику', url='telegram.me/s_evg13'
    #     )
    # )
    # bot.send_message(message.chat.id, HELP, reply_markup=keyboard)


@bot.message_handler(commands=['newgame'])
def newgame(message):
    global r
    global m
    text = f'<b>Приветствую, {message.chat.first_name}.</b>\nДобро пожаловать в игру "Поиски сокровищ"!\n{HELP}'
    bot.send_message(message.chat.id, text, parse_mode='html', reply_markup=game_keyboard)
    bot.send_photo(message.chat.id, open('map.gif', 'rb'))

    us_id = message.from_user.id
    us_name = str(message.from_user.first_name)
    us_sname = str(message.from_user.last_name)
    username = str(message.from_user.username)

    insert_new_user(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username,
                    date_register=datetime.today())

    r = random.choice(T)
    text = cave_description()
    m = 0
    bot.send_message(message.chat.id, text)
    bot.send_message(message.chat.id, 'Что вы намерены делать?')
    bot.register_next_step_handler(message, get_text_messages)


def get_text_messages(message):
    global r
    global m
    global c

    if message.text == '/newgame':
        return
    if message.text not in valid_commands:
        msg = bot.send_message(message.chat.id, 'Команда не распознана. Движение не засчитано.')
        bot.register_next_step_handler(msg, get_text_messages)
        return

    us_id = message.from_user.id
    if (m < movements_available) and (not all(x == T[0] for x in T)):
        if message.text.lower() == 'помощь':
            text = f'<b>Приветствую, {message.chat.first_name}.</b>\nДобро пожаловать в игру "Поиски сокровищ"!\n{HELP}'
            bot.send_message(message.chat.id, text, parse_mode='html')
            bot.register_next_step_handler(message, get_text_messages)
        elif message.text == 'с' or message.text == 'в' or message.text == 'ю' or message.text == 'з':
            x = 0
            if message.text == 'с':
                x = N[r - 1]
            elif message.text == 'в':
                x = E[r - 1]
            elif message.text == 'ю':
                x = S[r - 1]
            elif message.text == 'з':
                x = W[r - 1]
            if x == 0:
                bot.send_message(message.chat.id, 'Нельзя идти в эту сторону')
            else:
                r = x
            text = cave_description()
            bot.send_message(message.chat.id, text)
            bot.register_next_step_handler(message, get_text_messages)
        elif message.text == 'поднять':
            y = -1
            if c == 1:
                text = 'Нельзя переносить больше одного ящика'
            else:
                for k in range(7):
                    if T[k] == r:
                        y = k
                if y == -1:
                    text = 'Эта пещера пуста'
                else:
                    T[y] = 999
                    text = f'Хорошо. Вы перенесете {TS[y]}'
                    c = 1
            bot.send_message(message.chat.id, text)
            bot.register_next_step_handler(message, get_text_messages)
        elif message.text == 'положить':
            if c == 0:
                text = 'Вы ничего не несете'
            else:
                for k in range(7):
                    if T[k] == 999:
                        text = f'{TS[k]} поставлен в пещере {r}'
                        T[k] = r
                        c = 0
            bot.send_message(message.chat.id, text)
            bot.register_next_step_handler(message, get_text_messages)
        elif message.text == 'расположение':
            vtext = 'Вы несете:'
            if c == 0:
                text = f'{vtext} Ничего\n'
            else:
                for k in range(7):
                    if T[k] == 999:
                        text = f'{vtext} {TS[k]}\n'
            text += 'В пещерах находятся:\n'
            for k in range(7):
                if T[k] != 999:
                    text += f'{T[k]} : {TS[k]}\n'
            bot.send_message(message.chat.id, text)
            bot.register_next_step_handler(message, get_text_messages)

        m += 1

        if all(x == T[0] for x in T):
            text = f'Отличная работа. Вы перенесли все сокровища в пещеру {r} за {m} движений'
            insert_result(user_id=us_id, date_result=datetime.today(), movements=m, cave=r, done=True)
            bot.send_message(message.chat.id, text)
            bot.send_message(message.chat.id, 'Начать новую игру: /newgame')

        if m >= movements_available:
            insert_result(user_id=us_id, date_result=datetime.today(), movements=m, cave=r, done=False)
            bot.send_message(message.chat.id, 'К сожалению, вы превысили допустимый лимит движений')
            bot.send_message(message.chat.id, 'Начать новую игру: /newgame')


bot.polling(none_stop=True)
