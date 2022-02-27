#!/usr/bin/env python
# -*- coding: utf-8 -*- # строка нужна, чтобы не было ошибки Non-UTF-8 code starting with '\xd1' in file ...
import random
import os.path
import os
import pandas as pd
import base_update
import addUser
import getUserByEmail
import connection_data
from flask import Flask, render_template, request,redirect,url_for,send_file,flash, Response,g,session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)




predmety_en={'ecology': 'Экология', 'literature':'Литература', 'life_safety_fundamentals':'ОБЖ', 'english':'Английский', 'technology_Home_Culture':'Технология (культура дома)',	'technology_TT_and_TT':'Технология (робототехника)', 'technology_robotics':'Робототехника', 'astronomy':'Астрономия', 'french':'Французкий язык', 'russian_language':'Русский язык', 'physical_education':'Психология', 'german_language':'Немецкий язык', 'social_studies':'social_studies','physics':'Физика', 'biology':'Биология', 'spanish':'Испанский язык', 'maths':'Математика', 'economics':'Экономика', 'chemistry':'Химия', 'italian_language':'Итальянский язык', 'history':'История', 'geography':'География', 'informatics':'Информитика','art_mhc':'МХК', 'law':'Право', 'chinese':'Китайский язык'}
predmety_ru={'Экология':'ecology', 'Литература':'literature', 'ОБЖ':'life_safety_fundamentals', 'Английский':'english', 'Технология (культура дома)':'technology_Home_Culture',	'Технология (робототехника)':'technology_TT_and_TT', 'Робототехника':'technology_robotics', 'Астрономия':'astronomy', 'Французкий язык':'french', 'Русский язык':'russian_language', 'Психология':'physical_education', 'Немецкий язык':'german_language', 'social_studies':'social_studies','Физика':'physics', 'Биология':'biology', 'Испанский язык':'spanish', 'Математика':'maths', 'Экономика':'economics', 'Химия':'chemistry', 'Итальянский язык':'italian_language', 'История':'history', 'География':'geography', 'Информитика':'informatics','МХК':'art_mhc', 'Право':'law', 'Китайский язык':'chinese'}
excel_name=''
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'cb02820a3e94d72c9f950ee10ef7e3f7a35b3f5b'



@app.route('/', methods=['POST', 'GET'])
@app.route('/<name_table_get>')
def main(name_table_get="klass_0"):
    if g.user:  # если глобальный user то будет выполняться
        mas=connection_data.connection.connection_data(name_table_get)
        name_col=mas[0]
        spisok_table=mas[1]
        return render_template('index.html',name_col=name_col,spisok_table=spisok_table,name_table_get=name_table_get, \
                               user=session['user']) #user=session это как раз сессии для авторизации

    return redirect(url_for('login'))

#============================================================================================================

@app.route('/<name_table_get>/file',methods=['POST', 'GET'])
def main_file(name_table_get="klass_0"):
    if g.user:  # если глобальный user то будет выполняться
        mas = connection_data.connection.connection_data(name_table_get)
        name_col = mas[0]
        spisok_table = mas[1]
        return render_template('index_file.html', name_col=name_col, spisok_table=spisok_table,\
                               name_table_get=name_table_get, \
                               user=session['user'])  # user=session это как раз сессии для авторизации

    return redirect(url_for('login'))


#============================================================================================================

@app.route('/<name_table_get>/text',methods=['POST', 'GET'])
def main_text(name_table_get="klass_0"):
    if g.user:  # если глобальный user то будет выполняться

        mas = connection_data.connection.connection_data(name_table_get)
        name_col = mas[0]
        spisok_table = mas[1]
        return render_template('index_text.html', name_col=name_col, spisok_table=spisok_table,\
                               name_table_get=name_table_get, \
                               user=session['user'])  # user=session это как раз сессии для авторизации

    return redirect(url_for('login'))

#============================================================================================================

@app.route('/download', methods=['POST','GET'])
def download():
    return send_file("123.xlsx", as_attachment=True)



# ============================================================================================================

@app.route('/update/text', methods=['POST','GET'])
def update_text():
    if request.method == 'POST':

        predmet = request.form['predmet']
        kol = int(request.form['kol_pas'])
        name_table = request.form['table_name']

        name_col = connection_data.connection.connection_data(name_table)[0]
        # --------------------------------------------------------------------------------------------

        # ------------ для того чтобы сопоставить название столбца с его порядковым номером----------------
        for i in range(len(name_col)):
            if name_col[i] == predmet:
                num_predmet = i + 1
        # -----------------------------------------------------------------------------------------------

        # -------------выборка паролей-----------
        passw = base_update.base_update.base_update(kol, name_table, num_predmet, predmet)
        fio = []

        for lll in range(int(kol)):
            ddddd = 'item' + str(lll + 1)
            fio.append(request.form[ddddd])
        # --------------------------------------------------------

        # формирование файла для скачивания------------------------------------------------------------------
        DataFrame_downloads = pd.DataFrame({'ФИО': fio, 'Пароль': passw, 'Предмет': predmet, 'Класс': name_table})
        excel_name = str(random.randint(1, 10000))
        DataFrame_downloads.to_excel(excel_name + '.xlsx', index=False)  # запись в файл


        # time.sleep(3)!
        path = excel_name + ".xlsx"

        return send_file(path, as_attachment=True)
    return 'Неверный запрос, если хотите забрать файл перейдите на главную'

#============================================================================================================

@app.route('/update/file', methods=['POST','GET'])
def update_file():
    if request.method == 'POST':
        f = request.files['file']
        file_name = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
        rf = pd.read_excel('uploads/' + file_name)
        kol = len(rf.index)
        fio = rf['ФИО'].tolist()

        predmet = request.form['predmet']
        name_table = request.form['table_name']

        klass=[]
        for i in range(kol):
            klass.append(name_table)
        predmet_mas=[]
        for i in range(kol):
            predmet_mas.append(predmet)




        # --------узнать имена столбцов sql таблицы---------------------------------------------------
        name_col = connection_data.connection.connection_data(name_table)[0]

        # ------------ для того чтобы сопоставить название столбца с его порядковым номером----------------
        for i in range(len(name_col)):
            if name_col[i] == predmet:
                num_predmet = i + 1

        # -------------выборка паролей-----------
        passw=base_update.base_update.base_update(kol, name_table, num_predmet, predmet)

        print(len(fio),len(passw),len(predmet_mas),len(klass))

        # формирование файла для скачивания------------------------------------------------------------------
        DataFrame_downloads = pd.DataFrame({'ФИО': fio, 'Пароль': passw, 'Предмет': predmet_mas, 'Класс': klass})
        excel_name = str(random.randint(1, 10000))+'.xlsx'
        DataFrame_downloads.to_excel(excel_name, index=False)  # запись в файл

        # time.sleep(3)
        return send_file(excel_name, as_attachment=True)
    return 'Неверный запрос, если хотите забрать файл перейдите на главную'


#============================================================================================================


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        session.pop('user', None)

        if request.method == "POST":
            user = getUserByEmail.getUserByEmail.getUserByEmail(request.form['email']) # забирает всю строку в таблице пользователей
            if user and check_password_hash(user[3],request.form['psw']): # проверка совпадает ли hash с введенным паролем

                session['user'] = user[3]
                return redirect(url_for('main'))

            else:
                flash("Неверный email или пароль", "error")
    return render_template("login.html")

#============================================================================================================

@app.before_request
def before_request():
    g.user=None

    if 'user' in session:
        g.user = session['user']

#============================================================================================================


#============================================================================================================

@app.route('/base', methods=['POST','GET'])
def base():
    import sqlite3
    connection = sqlite3.connect('xls_to_sql.db')
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    table = cursor.fetchall()
    connection.close()
    # -----------------------------------------------------------------------------------
    if request.method == 'POST':
        f = request.files['file']
        file_name = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
        rf = pd.read_excel('uploads/' + file_name)

        titul = rf.columns
        kol_strok = len(rf.index) - 1
        mas_numpay = rf.to_numpy()

        # -----------------------------------------------------------------------------------
        connection = sqlite3.connect('xls_to_sql.db')
        cursor = connection.cursor()
        # -----------------------------------------------------------------------------------
        nazvania_stolb = 'id INTEGER PRIMARY KEY AUTOINCREMENT, '

        for i in range(len(titul)):
            nazvania_stolb += titul[i]
            nazvania_stolb += ' TEXT NOT NULL,'
        nazvania_stolb = nazvania_stolb[:-1]
        tableName = file_name[:file_name.find('.')]
        # -----------------------------------------------------------------------------------
        cursor.execute("""CREATE TABLE IF NOT EXISTS {} ({})""".format(tableName, nazvania_stolb))
        # -----------------------------------------------------------------------------------

        name_sql='id,'
        for i in range(len(titul)):
            name_sql += titul[i]+','
        name_sql = name_sql[:-1]
        # -----------------------------------------------------------------------------------
        znach_stroki = ''
        for i in range(len(titul) + 1):
            znach_stroki += '?,'
        znach_stroki = znach_stroki[:-1]
        # -----------------------------------------------------------------------------------
        for i in range(1,kol_strok+1):
            data_stroki=[None]
            for j in range (len(titul)):
                data_stroki.append(mas_numpay[i,j])
            # -----------------------------------------------------------------------------------
            sql = 'INSERT INTO {} ({}) values ({})'.format(tableName, name_sql, znach_stroki)

            data = [data_stroki]  # None для того чтобы id ключ автонумеровался

            cursor.executemany(sql, data)
            connection.commit()
        # -----------------------------------------------------------------------------------

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        table = cursor.fetchall()
        connection.close()

    return render_template('base.html', table=table)

#============================================================================================================

@app.route('/dropsession')
def dropsession():
    session.pop('user',None)
    return render_template('login.html')

#============================================================================================================

@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        #session.pop('user', None)
        if len(request.form['name']) > 1 and len(request.form['email']) > 4 \
                and len(request.form['psw']) > 4 and request.form['psw'] == request.form['psw2']:
            hash = generate_password_hash(request.form['psw'])
            res = addUser.addUser.addUser(request.form['name'], request.form['email'], hash)
            if res:
                flash("Вы успешно зарегистрированы", "success")
                return redirect(url_for('login'))
            else:
                flash("Ошибка при добавлении в БД", "error")
        else:
            flash("Неверно заполнены поля", "error")

    return render_template('register.html')

#============================================================================================================

if __name__ == '__main__':
    app.run(debug=True)
    #app.run()