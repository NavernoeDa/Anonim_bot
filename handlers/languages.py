from json import loads, load, dump
from codecs import open as opening
from os.path import exists

""" Добавление/смена языка """


def set_language(id_, language, is_change=False):
    old_json = load(opening('./languages/users_lang.json', 'rb'))

    if str(id_) not in old_json or is_change:
        new_json = {id_: {"lang": language}}
        old_json.pop(id_, None)
        old_json.update(new_json)
        dump(old_json, open('./languages/users_lang.json', 'w'))


""" Проверка на наличие языка """


def check_language(language):
    return exists(f'./languages/main/{language}.json')


""" Получение языка """


def get_language(id_):
    with opening('./languages/users_lang.json', 'r', 'utf-8') as file:
        language = loads(file.read())
        return language[str(id_)]['lang']


""" Взятие перевода из файла """


def choose_language(id_, section, message):
    with opening(f'./languages/main/{get_language(id_)}.json', 'r', 'utf-8') as file:
        data = loads(file.read())
        return data[section][message]
