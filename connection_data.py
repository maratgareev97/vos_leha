#!/usr/bin/env python
# -*- coding: utf-8 -*- # строка нужна, чтобы не было ошибки Non-UTF-8 code starting with '\xd1' in file ...
class connection:
    def connection_data(name_table):
        import sqlite3
        from flask import Flask, render_template, request, redirect, url_for, send_file, flash, Response, g, session
        predmety_en = {'ecology': 'Экология', 'literature': 'Литература', 'life_safety_fundamentals': 'ОБЖ',
                       'english': 'Английский', 'technology_Home_Culture': 'Технология (культура дома)',
                       'technology_TT_and_TT': 'Технология (робототехника)', 'technology_robotics': 'Робототехника',
                       'astronomy': 'Астрономия', 'french': 'Французкий язык', 'russian_language': 'Русский язык',
                       'physical_education': 'Психология', 'german_language': 'Немецкий язык',
                       'social_studies': 'social_studies', 'physics': 'Физика', 'biology': 'Биология',
                       'spanish': 'Испанский язык', 'maths': 'Математика', 'economics': 'Экономика',
                       'chemistry': 'Химия', 'italian_language': 'Итальянский язык', 'history': 'История',
                       'geography': 'География', 'informatics': 'Информитика', 'art_mhc': 'МХК', 'law': 'Право',
                       'chinese': 'Китайский язык'}
        predmety_ru = {'Экология': 'ecology', 'Литература': 'literature', 'ОБЖ': 'life_safety_fundamentals',
                       'Английский': 'english', 'Технология (культура дома)': 'technology_Home_Culture',
                       'Технология (робототехника)': 'technology_TT_and_TT', 'Робототехника': 'technology_robotics',
                       'Астрономия': 'astronomy', 'Французкий язык': 'french', 'Русский язык': 'russian_language',
                       'Психология': 'physical_education', 'Немецкий язык': 'german_language',
                       'social_studies': 'social_studies', 'Физика': 'physics', 'Биология': 'biology',
                       'Испанский язык': 'spanish', 'Математика': 'maths', 'Экономика': 'economics',
                       'Химия': 'chemistry', 'Итальянский язык': 'italian_language', 'История': 'history',
                       'География': 'geography', 'Информитика': 'informatics', 'МХК': 'art_mhc',  'Право': 'law',
                       'Китайский язык': 'chinese'}

        connection = sqlite3.connect('../my/xls_to_sql.db')
        cursor = connection.cursor()

        # ----------- названия таблиц ----------------------------------------------------------------------
        cursor.execute(
            "SELECT name FROM(SELECT * FROM sqlite_master UNION ALL SELECT * FROM sqlite_temp_master) WHERE type = 'table' ORDER BY name")
        spisok_table_tuple = cursor.fetchall()
        spisok_table = []
        for i in range(len(spisok_table_tuple)):
            if (str(spisok_table_tuple[i]))[2:-3:1] == 'users' or (str(spisok_table_tuple[i]))[
                                                                  2:-3:1] == 'sqlite_sequence':
                continue
            spisok_table.append(((str(spisok_table_tuple[i]))[2:-3:1]))

        # ------------------------------------------------------------------- чтобы небыло ошибки в словаре
        if name_table == 'klass_0':
            return [['none'], spisok_table]
        # ----------- названия столбцов -------------------------------------------------------------------
        sql='PRAGMA table_info({})'.format(name_table)
        cursor.execute(sql)
        colu = cursor.fetchall()
        name_col = []
        for i in range(1, len(colu)):
            mmm = str(colu[i])
            mmm = mmm.split(',')
            mmm = predmety_en[str(mmm[1][2:-1:1])]
            name_col.append(mmm)

        connection.close()
        return [name_col, spisok_table]