# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, send_file, session, jsonify
from database import execute_query
import subprocess
import pandas as pd
from tempfile import NamedTemporaryFile
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
def get_reviews(film_id):
    query = 'SELECT * FROM reviews WHERE film_id = ?'
    return execute_query(query, (film_id,))

def index():
    username = session.get('username')  
    user_logs = []
    if username:
        user_row = execute_query('SELECT id FROM users WHERE username = ?', (username,))
        if user_row:
            user_id = user_row[0][0]
            user_logs = execute_query('SELECT film_name, timestamp FROM user_logs WHERE user_id = ? ORDER BY timestamp DESC', (user_id,))
    return render_template('index.html', username=username, user_logs=user_logs)

def login():
    error = None
    if request.method == 'POST':
        user_type = request.form.get('user_type')
        if user_type == 'guest':
            session.pop('username', None)  
            return redirect('/index')
        username = request.form.get('username')
        password = request.form.get('password')
        result = execute_query('SELECT password FROM users WHERE username = ?', (username,))
        if result:
            password_hash = result[0][0]
            if check_password_hash(password_hash, password):
                session['username'] = username  
                return redirect('/index')
            else:
                error = "Ошибка: неверный пароль"
        else:
            error = "Ошибка: такого логина нет в базе данных"
    return render_template('welcome.html', error=error)

def welcome():
    if request.method == 'POST':
        user_type = request.form.get('user_type')
        if user_type == 'guest':
            return redirect('/index')
        elif user_type == 'user':
            return redirect('/login')
    return render_template('welcome.html')

def register():
    username = request.form.get('new_username')
    password = request.form.get('new_password')
    password_hash = generate_password_hash(password)
    execute_query('INSERT INTO users (username, password) VALUES (?, ?)', (username, password_hash))
    session['username'] = username  
    return redirect('/index')

def show_reviews():
    if request.method == 'POST':
        film_id = request.form.get('film_id')
    else:
        film_id = request.args.get('film_id')
        
    if film_id:
        # Проверка наличия отзывов в базе данных
        reviews = get_reviews(film_id)
        
        if not reviews:
            process = subprocess.Popen(["python3", "reviews.py", str(film_id)])
            process.wait()
            reviews = get_reviews(film_id)
        
        film_row = execute_query('SELECT name FROM films WHERE id = ?', (film_id,))
        if film_row:
            film_name = film_row[0][0]

            # Инициализация счетчиков
            positive_count = 0
            neutral_count = 0
            negative_count = 0

            # Один цикл для подсчета всех типов отзывов
            for review in reviews:
                if review[2] == 'good':
                    positive_count += 1
                elif review[2] == 'neutral':
                    neutral_count += 1
                elif review[2] == 'bad':
                    negative_count += 1

            username = session.get('username')
            if username is not None:
                user_row = execute_query('SELECT id FROM users WHERE username = ?', (username,))
                if user_row:
                    user_id = user_row[0][0]
                    execute_query('INSERT INTO user_logs (user_id, film_name) VALUES (?, ?)', (user_id, film_name))
            return render_template('reviews.html', film_name=film_name, film_id=film_id, reviews=reviews, 
                                   positive_count=positive_count, neutral_count=neutral_count, negative_count=negative_count)
        else:
            return "Фильм не найден"
    else:
        return "Нет ID фильма"

def delete_review():
    review_id = request.form['review_id']
    film_id = request.form['film_id']  
    execute_query('DELETE FROM reviews WHERE id = ?', (review_id,))
    return redirect(f'/reviews?film_id={film_id}')



def export_reviews():
    film_name = request.form.get('film_name')
    film_id = request.form.get('film_id')
    if film_id:
        reviews = get_reviews(film_id)
        if reviews:
            # Получаем данные о фильме из базы данных
            film_row = execute_query('SELECT name FROM films WHERE id = ?', (film_id,))
            if film_row:
                film_name = film_row[0][0]

                # Создаем DataFrame из отзывов с добавлением столбца film_name и преобразованием даты
                df = pd.DataFrame(reviews, columns=['id', 'film_id', 'review_type', 'review_text', 'review_date'])
                df['film_name'] = film_name
                df['review_date'] = pd.to_datetime(df['review_date'], format='%Y-%m-%d %H:%M:%S')  # Преобразуем строковое представление даты в формат даты

                # Удаляем столбец "id"
                df.drop(columns=['id'], inplace=True)

                # Создаем временный файл для записи отзывов с названием "Отзывы"
                temp_file = NamedTemporaryFile(delete=False, suffix='.csv', prefix='Отзывы_')

                # Записываем DataFrame в CSV-файл
                df.to_csv(temp_file.name, index=False, encoding='utf-16')

                # Отправляем временный файл в качестве ответа
                return send_file(temp_file.name, as_attachment=True, mimetype='text/csv')
            else:
                return "Фильм не найден"
        else:
            return "Нет отзывов для данного фильма"
    else:
        return "Ошибка: отсутствует идентификатор фильма"

def get_viewers_by_date(date):
    try:
        # Запрос к базе данных для извлечения данных о просмотрах за указанную дату
        query = '''
            SELECT users.username, 
                   user_logs.film_name,
                   (SELECT COUNT(*) FROM reviews WHERE film_id = films.id AND review_type = 'good') AS positive_reviews,
                   (SELECT COUNT(*) FROM reviews WHERE film_id = films.id AND review_type = 'bad') AS negative_reviews,
                   (SELECT COUNT(*) FROM reviews WHERE film_id = films.id AND review_type = 'neutral') AS neutral_reviews
            FROM user_logs
            JOIN users ON user_logs.user_id = users.id
            JOIN films ON user_logs.film_name = films.name
            WHERE DATE(user_logs.timestamp) = ?
        '''
        # Выполнение SQL запроса
        viewers = execute_query(query, (date,))
        
        # Формирование списка словарей с данными о пользователях, фильмах и количестве отзывов
        result = [{'username': viewer[0], 
                   'film_name': viewer[1], 
                   'positive_reviews': viewer[2],
                   'negative_reviews': viewer[3],
                   'neutral_reviews': viewer[4]} for viewer in viewers]

        # Возвращение результата в формате JSON
        return jsonify(result), 200
    except Exception as e:
        # В случае ошибки возвращаем JSON с сообщением об ошибке и статусом 500
        return jsonify({'error': str(e)}), 500
    
def selection_range(start_date, end_date):
    try:
        # Выполнение запроса к базе данных для получения данных о просмотрах в заданном диапазоне дат
        query = '''
            SELECT users.username, 
                   user_logs.film_name,
                   user_logs.timestamp AS view_date,
                   (SELECT COUNT(*) FROM reviews WHERE film_id = films.id AND review_type = 'good') AS positive_reviews,
                   (SELECT COUNT(*) FROM reviews WHERE film_id = films.id AND review_type = 'bad') AS negative_reviews,
                   (SELECT COUNT(*) FROM reviews WHERE film_id = films.id AND review_type = 'neutral') AS neutral_reviews
            FROM user_logs
            JOIN users ON user_logs.user_id = users.id
            JOIN films ON user_logs.film_name = films.name
            WHERE user_logs.timestamp BETWEEN ? AND ?
        '''
        viewers = execute_query(query, (start_date, end_date))

        # Формирование списка словарей с данными о просмотрах в заданном диапазоне дат
        result = [{'username': viewer[0], 
                   'film_name': viewer[1],
                   'date': viewer[2], 
                   'positive_reviews': viewer[3], 
                   'negative_reviews': viewer[4], 
                   'neutral_reviews': viewer[5]} 
                  for viewer in viewers]

        # Возвращение результатов в формате JSON
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def not_found(error):
    response = jsonify({
        "status": "error",
        "message": "Запрошенный URL-адрес не был найден на сервере."
    })
    response.status_code = 404
    return response

def method_not_allowed(error):
    response = jsonify({
        "status": "error",
        "message": "Этот метод не разрешен для запрошенного URL-адреса."
    })
    response.status_code = 405
    return response