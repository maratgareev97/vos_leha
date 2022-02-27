#!/usr/bin/env python
# -*- coding: utf-8 -*- # строка нужна, чтобы не было ошибки Non-UTF-8 code starting with '\xd1' in file ...

class base_update:
    def base_update(kol, name_table, num_predmet, predmet):
        import sqlite3
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
                       'technology_TT_and_TT': 'technology_TT_and_TT', 'Робототехника': 'technology_robotics',
                       'Астрономия': 'astronomy', 'Французкий язык': 'french', 'Русский язык': 'russian_language',
                       'Психология': 'physical_education', 'Немецкий язык': 'german_language',
                       'social_studies': 'social_studies', 'Физика': 'physics', 'Биология': 'biology',
                       'Испанский язык': 'spanish', 'Математика': 'maths', 'Экономика': 'economics',
                       'Химия': 'chemistry', 'Итальянский язык': 'italian_language', 'История': 'history',
                       'География': 'geography', 'Информитика': 'informatics', 'МХК': 'art_mhc', 'Право': 'law',
                       'Китайский язык': 'chinese'}

        connection = sqlite3.connect('../my/xls_to_sql.db')
        cursor = connection.cursor()

        predmet = predmety_ru[str(predmet)]
        passw = []

        for lll in range(kol):
            cursor.execute("SELECT * FROM {}".format(name_table))
            rows = cursor.fetchall()
            for i in range(len(rows)):
                if rows[i][num_predmet] == '0':
                    notnull = rows[i - 1][num_predmet]  # забираемый пароль
                    break

            passw.append(notnull)  # добавление в массив удаленных паролей

            sqlite_update_query = "UPDATE {} SET {} = '0' WHERE id = ?".format(name_table, predmet)
            a = i  # это id строки откуда забирается пароль
            stroka = (a,)  # запятая ВАЖНО. Без нее не получалось
            cursor.execute(sqlite_update_query, stroka)
        connection.commit()  # Подтеверждение записи!!!
        connection.close()
        return passw