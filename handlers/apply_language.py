from json import loads, load, dump
from codecs import open as opening

""" Добавление/смена языка """
def set_language(id_, lang, is_change=False):
    old_json = load(open('./languages/users_lang.json', 'r'))

    if str(id_) not in old_json or is_change:
        new_json = {id_: {"lang": lang}}
        old_json.pop(id_, None)
        old_json.update(new_json)
        dump(old_json, open('./languages/users_lang.json', 'w'))


""" Получение языка """
def get_language(id_):
    with opening('./languages/users_lang.json', 'r', 'utf-8') as file:
        language = loads(file.read())
        return language[str(id_)]['lang']


""" Взятие перевода из файла """
def choose_language(id_, section, message):
    with opening(f'./languages/{get_language(id_)}.json', 'r', 'utf-8') as file:
        data = loads(file.read())
        return data[section][message]
