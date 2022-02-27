#!/usr/bin/env python
# -*- coding: utf-8 -*- # строка нужна, чтобы не было ошибки Non-UTF-8 code starting with '\xd1' in file ...

class getUserByEmail:
    def getUserByEmail(email):
        import sqlite3
        try:
            connection = sqlite3.connect('../my/xls_to_sql.db')
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            res = cursor.fetchone()
            connection.close()
            if not res:
                print("Пользователь не найден")
                return False
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))
        return False