from random import randint

import sqlite3


class DataBase:
    def __init__(self, path_to_db="./database/DataBase.db"):
        self.connection = sqlite3.connect(path_to_db)
        self.cursor = self.connection.cursor()

    """ Добавление в базу данных """
    def adding_to_the_database(self, id_: int):
        with self.connection:
            self.cursor.execute('INSERT INTO users(id, in_private) VALUES(?, 0)', [id_])

    """ Язык по дефолту """
    def add_language(self, id_: int):
        with self.connection:
            self.cursor.execute('INSERT INTO')

    """ Сбор id по значению in_private """
    def collecting_ids(self, in_private: int) -> list:
        with self.connection:
            self.cursor.execute('SELECT id FROM users WHERE in_private = ?', [in_private])
            return self.cursor.fetchall()

    """ Меняет приват id """
    def update_private_on(self, id_: int, in_private: int):
        with self.connection:
            self.cursor.execute('UPDATE users SET in_private = ? WHERE id = ?', [in_private, id_])

    """ Получение приват id """
    def get_private_on(self, id_: int) -> int:
        with self.connection:
            self.cursor.execute('SELECT in_private FROM users WHERE id = ?', [id_])
        return self.cursor.fetchone()[0]

    """ Создание комнаты """
    def create_room(self, id_: int) -> int:
        code_room = randint(1000, 9999)
        with self.connection:
            self.cursor.execute('INSERT INTO rooms(code, id_one, id_two) VALUES(?, ?, 0)', [code_room, id_])
            self.update_private_on(id_, 1)
        return code_room

    """ Присоединение к комнате """
    def join_room(self, id_: int, code_room: int):
        with self.connection:
            self.cursor.execute('SELECT id_two FROM rooms WHERE code = ?', [code_room])
            if self.cursor.fetchone()[0] == 0:
                self.cursor.execute('UPDATE rooms SET id_two = ? WHERE code = ?', [id_, code_room])
                self.update_private_on(id_, 1)
            else:
                raise ValueError

    """ Получение id собеседника """
    def getting_the_id(self, id_: int) -> int:
        with self.connection:
            self.cursor.execute('SELECT id_one FROM rooms WHERE id_two = ?', [id_])
            id_two = self.cursor.fetchone()
            if id_two is None:
                self.cursor.execute('SELECT id_two FROM rooms WHERE id_one = ?', [id_])
                id_two = self.cursor.fetchone()

            return id_two[0]

    """ Удаление комнаты """
    def delete_room(self, id_: int):
        with self.connection:
            self.cursor.execute("SELECT id_two FROM rooms WHERE id_one = ?", [id_])

            self.update_private_on(self.cursor.fetchone()[0], 0)
            self.update_private_on(id_, 0)

            self.cursor.execute("DELETE FROM rooms WHERE id_one = ?", [id_])

    """ Выход из комнаты """
    def disconnect(self, id_: int):
        with self.connection:
            self.update_private_on(id_, 0)
            self.cursor.execute("UPDATE rooms SET id_two = 0 WHERE id_two = ?", [id_])
