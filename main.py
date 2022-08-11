"""

Надо доделать кумчатке:
в except вставить ошибку, где будет две ошибки, их нужно через кортеж.
 Пример: except(ValueError, IndexError) Если нужно выводить одно сообщение для нескольких ошибок

Если нужно для определенных ошибок выводить какое-то соо то
ПРИМЕР
try:
    <code>
except название ошибки:
    <code>
except название ошибки:
    <code>
ну разберешься

Так же протестируй, т.к у меня нет другого акка для тестов

"""

from database import DataBase
from sqlite3 import IntegrityError
from handlers import send_message

from telebot import TeleBot

bot = TeleBot("token")


def push(id_, text):
    id_two = DataBase().getting_the_id(id_)
    if id_two == 0 or id_two is None:
        pass
    else:
        bot.send_message(id_two, text)


@bot.message_handler(commands=['start'])
def start(message):
    try:
        DataBase().adding_to_the_database(message.from_user.id)
        bot.reply_to(message, "Вы зарегистрированы\nОтправлять фотки БЕЗ СЖАТИЯ, ДОКУМЕНТОМ")
    except IntegrityError:
        bot.reply_to(message, "Вы уже зареганы!")


@bot.message_handler(commands=['create_room'])
def create_room(message):
    try:
        code_room = DataBase().create_room(message.from_user.id)
        bot.reply_to(message, f"Комната с кодом {code_room} создана!")
        for id_ in DataBase().collecting_ids(0):
            bot.send_message(id_[0], f"Комната с кодом {code_room} создана!")
    except IntegrityError:
        bot.reply_to(message, "Ты уже в комнате")


@bot.message_handler(commands=['join_room'])
def join_room(message):
    try:
        if DataBase().get_private_on(message.from_user.id) == 1:
            bot.reply_to(message, 'Ты уже в комнате')
        else:
            code_room = message.text.split()[1]
            DataBase().join_room(message.from_user.id, int(code_room))
            bot.reply_to(message, "Ты вошел в комнату!")
            push(message.from_user.id, 'Собеседник присоединился')
    except ValueError:
        bot.reply_to(message, "Комната занята")
    except TypeError:
        bot.reply_to(message, "Такой комнаты нет")
    except IndexError:
        bot.reply_to(message, "Ты не ввёл комнату")


@bot.message_handler(commands=['disconnect'])
def disconnect_room(message):
    push(message.from_user.id, 'Собеседник отключился')
    DataBase().disconnect(message.from_user.id)
    bot.reply_to(message, "Ты вышел из комнаты!")


@bot.message_handler(commands=['delete_room'])
def remove_room(message):
    push(message.from_user.id, 'Комната удалена и ты в ней не состоишь')
    try:
        DataBase().delete_room(message.from_user.id)
        bot.reply_to(message, "Комната удалена!")
    except TypeError:
        bot.reply_to(message, "У тебя нет комнаты во владении")


@bot.message_handler(content_types=['text', 'sticker', 'audio', 'document', 'voice',
                                    'video_note', 'video', 'animation', 'forward_message'])
def main(message):
    in_private = DataBase().get_private_on(message.from_user.id)
    if in_private == 0:
        ids = DataBase().collecting_ids(in_private)
        for id_ in ids:
            if id_[0] != message.from_user.id:
                send_message(message, bot, id_[0])
    else:
        friend_id = DataBase().getting_the_id(message.from_user.id)
        send_message(message, bot, friend_id)

    bot.reply_to(message, "Сообщение отправлено!")


if __name__ == "__main__":
    bot.infinity_polling()
