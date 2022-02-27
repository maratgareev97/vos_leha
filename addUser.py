#!/usr/bin/env python
# -*- coding: utf-8 -*- # строка нужна, чтобы не было ошибки Non-UTF-8 code starting with '\xd1' in file ...

class addUser:
    def addUser(name, email, psw):
        import sqlite3
        import time
        from flask import flash
        try:
            connection = sqlite3.connect('../my/xls_to_sql.db')
            cursor = connection.cursor()
            # ------------ проверка сучествует ли запись (по email)  таблице--------
            cursor.execute(f"SELECT COUNT() as 'count' FROM users WHERE email LIKE '{email}'")
            res = cursor.fetchone()
            print(res[0], type(res))
            if res[0] > 0:
                print("Пользователь с таким email уже существует")
                flash("Пользователь с таким email уже существует")
                return False
            # -------------------------------------------------------------------
            #tm = math.floor(time.time())
            #print(tm)
            cursor.execute("INSERT INTO users VALUES(NULL, ?, ?, ?, ?)", (name, email, psw, '0'))
            connection.commit()
            connection.close()
        except sqlite3.Error as e:
            print("Ошибка добавления пользователя в БД " + str(e))
            return False

        return True