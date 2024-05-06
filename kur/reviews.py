import sqlite3
import requests
from bs4 import BeautifulSoup
# Инициализация объекта ReviewScraper
class ReviewScraper:
    def __init__(self, film_id, max_pages):
        self.film_id = film_id  # ID фильма на КиноПоиске
        self.max_pages = max_pages  # Максимальное количество страниц для обработки
        self.conn = sqlite3.connect('reviews.db')  # Создаем соединение с базой данных SQLite
        self.create_tables()  # Создаем таблицы, если они не существуют
    # Метод создания таблицы
    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS films (
                id TEXT PRIMARY KEY,
                name TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                film_id TEXT,
                review_type TEXT,
                review_text TEXT,
                FOREIGN KEY(film_id) REFERENCES films(id)
            )
        ''')
        self.conn.commit()
    # Метод для получения и сохранения отзывов
    def fetch_reviews(self):
        # Проверяем, есть ли фильм с данным ID в базе данных
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM films WHERE id = ?', (self.film_id,))
        count = cursor.fetchone()[0]
        if count > 0:
            print('Фильм с данным ID уже существует в базе данных.')
            return  # Если фильм уже есть, выходим из метода

        for review_type in ['good', 'bad', 'neutral']:
            for page in range(1, self.max_pages + 1):
                url = self.create_review_url(review_type, page)  # Создаем URL для страницы с отзывами
                response = requests.get(url)  # Отправляем GET-запрос к URL

                if response.status_code != 200:
                    print(f"Не удалось подключиться.")
                    continue  # Пропускаем текущую страницу, если нет ответа от сервера

                soup = BeautifulSoup(response.text, 'html.parser')  # Парсим HTML страницы
                reviews = soup.find_all('div', {'itemprop': 'reviews'})  # Находим блоки с отзывами

                film_name_element = soup.find('a', class_='breadcrumbs__link')
                if film_name_element is not None:
                    film_name = film_name_element.text
                else:
                    film_name = "Unknown"  # Если название фильма не найдено, присваиваем его значение "Unknown"

                self.save_film_to_database(self.film_id, film_name)  # Сохраняем информацию о фильме в базу данных

                for i, review in enumerate(reviews):
                    film_name = soup.find('a', class_='breadcrumbs__link').text
                    review_text = review.find('span', {'itemprop': 'reviewBody'}).text
                    film_id = self.film_id
                    self.save_review_to_database(film_id, review_type, review_text)

    # Метод для создания URL страницы с отзывами
    def create_review_url(self, review_type, page):
        return f'https://www.kinopoisk.ru/film/{self.film_id}/reviews/ord/rating/status/{review_type}/perpage/10/page/{page}/'
    # Метод для сохранения отзыва в sql
    def save_review_to_database(self, film_id, review_type, review_text):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO reviews (film_id, review_type, review_text) VALUES (?, ?, ?)',
                       (film_id, review_type, review_text))
        self.conn.commit()
    # Метод для сохранения фильма в sql
    def save_film_to_database(self, film_id, film_name):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id FROM films WHERE id = ?', (film_id,))
        existing_film = cursor.fetchone()
        if existing_film is None:
            cursor.execute('INSERT INTO films (id, name) VALUES (?, ?)', (film_id, film_name))
            self.conn.commit()



# Изменения в методе main()
def main(film_id):
    max_pages = 1  # Максимальное количество страниц для обработки (по умолчанию 1)

    scraper = ReviewScraper(film_id, max_pages)  # Создаем экземпляр класса ReviewScraper
    scraper.fetch_reviews()  

    print('Готово')

if __name__ == "__main__":
    import sys
    film_id = int(sys.argv[1])  # Получаем film_id из аргументов командной строки
    main(film_id) 