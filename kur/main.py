# -*- coding: utf-8 -*-
from flask import Flask
from database import create_tables
from database import execute_query
import webbrowser
from threading import Timer
import routes
import os
import config

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Маршруты
#на одну дату
app.add_url_rule('/selection/<date>', 'get_viewers_by_date', routes.get_viewers_by_date, methods=['GET'])
#на диапозон дат 
app.add_url_rule('/selection_range/<start_date>&<end_date>','selection_range',routes.selection_range, methods=['GET'])
#Ошибка404
app.register_error_handler(404, routes.not_found)
#Ошибка405
app.register_error_handler(405, routes.method_not_allowed)

app.add_url_rule('/index', 'index', routes.index, methods=['GET', 'POST'])
app.add_url_rule('/login', 'login', routes.login, methods=['GET', 'POST'])
app.add_url_rule('/', 'welcome', routes.welcome, methods=['GET', 'POST'])
app.add_url_rule('/register', 'register', routes.register, methods=['POST'])
app.add_url_rule('/reviews', 'show_reviews', routes.show_reviews, methods=['GET', 'POST'])
app.add_url_rule('/delete_review', 'delete_review', routes.delete_review, methods=['POST'])
app.add_url_rule('/export_reviews', 'export_reviews', routes.export_reviews, methods=['POST'])

if __name__ == '__main__':
    # Проверяем наличие файла базы данных
    if not os.path.exists('reviews.db'):
        create_tables()  # Если файл базы данных не существует, создаем таблицы
    
    # Проверяем переменную окружения для определения режима тестирования
    if os.getenv('FLASK_ENV') != 'testing':
        url = f"{config.SERVER_ADDRESS}:{config.SERVER_PORT}"
        Timer(1, lambda: webbrowser.open(url)).start() # Открываем браузер через 1 секунду
    
    app.run()
