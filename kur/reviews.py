import requests
from bs4 import BeautifulSoup
from database import execute_query,create_tables
import sys
import os
import config
from datetime import datetime 
# Инициализация объекта ReviewScraper
class ReviewScraper:
    def __init__(self, film_id, max_pages):
        self.film_id = film_id  # ID фильма на КиноПоиске
        self.max_pages = max_pages  # Максимальное количество страниц для обработки
        if not os.path.exists('reviews.db'):
            create_tables()  # Если файл базы данных не существует, создаем таблицы
    # Словарь для соответствия названий месяцев и их номеров
    months_ru_to_en = {
        'января': 'January',
        'февраля': 'February',
        'марта': 'March',
        'апреля': 'April',
        'мая': 'May',
        'июня': 'June',
        'июля': 'July',
        'августа': 'August',
        'сентября': 'September',
        'октября': 'October',
        'ноября': 'November',
        'декабря': 'December'
    }
    # Метод для получения и сохранения отзывов
    def fetch_reviews(self):
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
                    review_text = review.find('span', {'itemprop': 'reviewBody'}).text
                    review_date_str = review.find('span', class_='date').text
                    
                    # Заменяем русские названия месяцев на английские
                    for month_ru, month_en in self.months_ru_to_en.items():
                        review_date_str = review_date_str.replace(month_ru, month_en)

                    review_date_format = "%d %B %Y | %H:%M"  # Предполагаемый формат даты
                    review_date = datetime.strptime(review_date_str, review_date_format)

                    film_id = self.film_id
                    self.save_review_to_database(film_id, review_type, review_text, review_date)

     # Метод для создания URL страницы с отзывами
    def create_review_url(self, review_type, page):
        return f'{config.SITE_URL}/film/{self.film_id}/reviews/ord/rating/status/{review_type}/perpage/10/page/{page}/'

    # Метод для сохранения отзыва в SQL
    def save_review_to_database(self, film_id, review_type, review_text, review_date):
        execute_query('INSERT INTO reviews (film_id, review_type, review_text, review_date) VALUES (?, ?, ?, ?)',(film_id, review_type, review_text, review_date))


    # Метод для сохранения фильма в SQL
    def save_film_to_database(self, film_id, film_name):
        execute_query('INSERT OR IGNORE INTO films (id, name) VALUES (?, ?)', (film_id, film_name))


# Изменения в методе main()
def main(film_id):
    max_pages = 1  # Максимальное количество страниц для обработки (по умолчанию 1)
    scraper = ReviewScraper(film_id, max_pages)  # Создаем экземпляр класса ReviewScraper
    scraper.fetch_reviews()
    print('Готово')

if __name__ == "__main__":
    film_id = int(sys.argv[1])  # Получаем film_id из аргументов командной строки
    main(film_id)
