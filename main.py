from database import DataBase
from sqlite3 import IntegrityError
from handlers import send_message, choose_language, set_language, check_language
from os import walk

from telebot import TeleBot

bot = TeleBot("")


def push(id_, section, message):
    id_two = DataBase().getting_the_id(id_)
    if id_two == 0 or id_two is None:
        pass
    else:
        bot.send_message(id_two, choose_language(id_two, section, message))


@bot.message_handler(commands=['start'])
def start(message):
    try:
        DataBase().adding_to_the_database(message.from_user.id)
        set_language(message.from_user.id, 'english')
        bot.reply_to(message, choose_language(message.from_user.id, 'start', 'message'))
    except IntegrityError:
        bot.reply_to(message, choose_language(message.from_user.id, 'start', 'error'))


@bot.message_handler(commands=['create_room'])
def create_room(message):
    try:
        code_room = DataBase().create_room(message.from_user.id)
        text = f'{choose_language(message.from_user.id, "create_room", "message")}{code_room}'
        bot.reply_to(message, text)
        for id_ in DataBase().collecting_ids(0):
            bot.send_message(id_[0], f'A new room has been created: {code_room}')
    except IntegrityError:
        bot.reply_to(message, choose_language(message.from_user.id, 'create_room', 'error'))


@bot.message_handler(commands=['join_room'])
def join_room(message):
    try:
        if DataBase().get_private_on(message.from_user.id) == 1:
            bot.reply_to(message, choose_language(message.from_user.id, 'join_room', 'error'))
        else:
            code_room = message.text.split()[1]
            DataBase().join_room(message.from_user.id, int(code_room))
            bot.reply_to(message, choose_language(message.from_user.id, 'join_room', 'message'))
            push(message.from_user.id, 'join_room', 'message_user_join')
    except ValueError:
        bot.reply_to(message, choose_language(message.from_user.id, 'join_room', 'error_room_busy'))
    except TypeError:
        bot.reply_to(message, choose_language(message.from_user.id, 'join_room', 'error_room_not_found'))
    except IndexError:
        bot.reply_to(message, choose_language(message.from_user.id, 'join_room', 'error_number'))


@bot.message_handler(commands=['disconnect'])
def disconnect_room(message):
    push(message.from_user.id, 'disconnect', 'message')
    DataBase().disconnect(message.from_user.id)
    bot.reply_to(message, choose_language(message.from_user.id, 'disconnect', 'message_left'))


@bot.message_handler(commands=['delete_room'])
def remove_room(message):
    push(message.from_user.id, 'delete_room', 'message')
    try:
        DataBase().delete_room(message.from_user.id)
        bot.reply_to(message, choose_language(message.from_user.id, 'delete_room', 'message_room_delete'))
    except TypeError:
        bot.reply_to(message, choose_language(message.from_user.id, 'delete_room', 'error'))


@bot.message_handler(commands=['change_language'])
def change_language(message):
    if check_language(message.text.split()[1]):
        set_language(message.from_user.id, message.text.split()[1], is_change=True)
        bot.reply_to(message, choose_language(message.from_user.id, 'change_language', 'message'))
    else:
        bot.reply_to(message, choose_language(message.from_user.id, 'change_language', 'error'))

        text = f'{choose_language(message.from_user.id, "service_messages", "all_languages")}\n'
        for i in walk('./languages/main'):
            for lang in i[2]:
                text += f'\n{lang.split(".json")[0]}'

        bot.send_message(message.from_user.id, text)


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

    bot.reply_to(message, choose_language(message.from_user.id, 'service_messages', 'message_send'))


if __name__ == "__main__":
    bot.infinity_polling()
