# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, send_file
import sqlite3
import webbrowser
from threading import Timer
import subprocess
from tempfile import NamedTemporaryFile
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your-secret-key' 
# Функция для получения отзывов о фильме из базы данных
def get_reviews(film_id):
    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM reviews WHERE film_id = ?', (film_id,))
    reviews = cursor.fetchall()
    conn.close()
    return reviews
# Маршрут для главной страницы, отображает страницу приветствия или страницу пользователя в зависимости от того, вошел ли пользователь в систему
@app.route('/index', methods=['GET', 'POST'])
def index():
    username = session.get('username')  
    user_logs = []
    if username is not None:
        conn = sqlite3.connect('reviews.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        user_row = cursor.fetchone()
        if user_row:
            user_id = user_row[0]
            cursor.execute('SELECT film_name, timestamp FROM user_logs WHERE user_id = ? ORDER BY timestamp DESC', (user_id,))
            user_logs = cursor.fetchall()
        conn.close()
    return render_template('index.html', username=username, user_logs=user_logs)
# Маршрут для страницы входа, обрабатывает вход пользователя или гостя
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user_type = request.form.get('user_type')
        if user_type == 'guest':
            session.pop('username', None)  
            return redirect('/index')
        username = request.form.get('username')
        password = request.form.get('password')
        conn = sqlite3.connect('reviews.db')
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        if user is None:
            error = "Ошибка: такого логина нет в базе данных"
        else:
            password_hash = user[0]
            if check_password_hash(password_hash, password):
                session['username'] = username  
                return redirect('/index')
            else:
                error = "Ошибка: неверный пароль"
    return render_template('welcome.html', error=error)


# Маршрут для начальной страницы, обрабатывает выбор пользователя войти как гость или как пользователь
@app.route('/', methods=['GET', 'POST'])
def welcome():
    if request.method == 'POST':
        user_type = request.form.get('user_type')
        if user_type == 'guest':
            return redirect('/index')
        elif user_type == 'user':
            return redirect('/login')
    return render_template('welcome.html')
# Маршрут для страницы регистрации, обрабатывает регистрацию нового пользователя
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('new_username')
    password = request.form.get('new_password')
    password_hash = generate_password_hash(password)
    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password_hash))
    conn.commit()
    conn.close()
    return redirect('/index')
# Маршрут для страницы отзывов, отображает отзывы о выбранном фильме и обрабатывает добавление отзыва в лог пользователя
@app.route('/reviews', methods=['GET', 'POST'])
def show_reviews():
    if request.method == 'POST':
        film_id = request.form.get('film_id')
    else:
        film_id = request.args.get('film_id')
    if film_id:
        process = subprocess.Popen(["python3", "reviews.py", str(film_id)])
        process.wait()
        conn = sqlite3.connect('reviews.db')
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM films WHERE id = ?', (film_id,))
        film_row = cursor.fetchone()
        if film_row:
            film_name = film_row[0]
            reviews = get_reviews(film_id)
            positive_count = sum(1 for review in reviews if review[2] == 'good')
            neutral_count = sum(1 for review in reviews if review[2] == 'neutral')
            negative_count = sum(1 for review in reviews if review[2] == 'bad')
            username = session.get('username')
            if username is not None:
                cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
                user_row = cursor.fetchone()
                if user_row:
                    user_id = user_row[0]
                    cursor.execute('INSERT INTO user_logs (user_id, film_name) VALUES (?, ?)', (user_id, film_name))
                    conn.commit()
            conn.close()
            return render_template('reviews.html', film_name=film_name, film_id=film_id, reviews=reviews, 
                                   positive_count=positive_count, neutral_count=neutral_count, negative_count=negative_count)
        else:
            conn.close()
            return "Фильм не найден"
    else:
        return "Нет ID фильма"

    
# Маршрут для удаления отзыва, обрабатывает удаление отзыва из базы данных
@app.route('/delete_review', methods=['POST'])
def delete_review():
    review_id = request.form['review_id']
    film_id = request.form['film_id']  
    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM reviews WHERE id = ?', (review_id,))
    conn.commit()
    conn.close()
    return redirect(f'/reviews?film_id={film_id}')  



# Маршрут для экспорта отзывов, обрабатывает экспорт отзывов о выбранном фильме в текстовый файл
@app.route('/export_reviews', methods=['POST'])
def export_reviews():
    film_name = request.form.get('film_name')
    film_id = request.form.get('film_id')
    if film_id:
        reviews = get_reviews(film_id)
        
        # Создаем временный файл для записи отзывов с названием "Отзывы"
        with NamedTemporaryFile(mode='w', delete=False, encoding='utf-8', suffix='.txt', prefix='Отзывы_') as temp_file:
            temp_file.write(f"Название фильма: {film_name}\n\n")
            for review in reviews:
                temp_file.write(f"Тип отзыва: {review[2]}\nТекст отзыва: {review[3]}\n\n")
        
        # Отправляем временный файл в качестве ответа
        return send_file(temp_file.name, as_attachment=True, mimetype='text/plain')
    else:
        return "Ошибка: отсутствует идентификатор фильма"
# Функция для создания таблицы пользователей и таблицы логов пользователей в базе данных
def create_users_table():
    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            film_name TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    conn.close()
if __name__ == '__main__':
    create_users_table()
    url = "http://127.0.0.1:5000"
    Timer(1, lambda: webbrowser.open(url)).start()  # Открываем браузер через 1 секунду
    app.run()
