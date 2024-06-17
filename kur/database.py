import sqlite3

DATABASE_NAME = 'reviews.db'

CREATE_USERS_TABLE = '''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    );
'''

CREATE_USER_LOGS_TABLE = '''
    CREATE TABLE IF NOT EXISTS user_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        film_name TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
'''

CREATE_FILMS_TABLE = '''
    CREATE TABLE IF NOT EXISTS films (
        id TEXT PRIMARY KEY,
        name TEXT
    );
'''

CREATE_REVIEWS_TABLE = '''
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        film_id TEXT,
        review_type TEXT,
        review_text TEXT,
        review_date TEXT, 
        FOREIGN KEY(film_id) REFERENCES films(id)
    );
'''

# Функция для создания таблиц в базе данных
def create_tables():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(CREATE_USERS_TABLE)
    cursor.execute(CREATE_USER_LOGS_TABLE)
    cursor.execute(CREATE_FILMS_TABLE)
    cursor.execute(CREATE_REVIEWS_TABLE)
    conn.commit()
    conn.close()

# Функция для выполнения SQL-запросов
def execute_query(query, values=None):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    if values:
        cursor.execute(query, values)
    else:
        cursor.execute(query)
    conn.commit()
    result = cursor.fetchall()
    conn.close()
    return result
