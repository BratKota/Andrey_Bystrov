#Рефакторинг:
#Создан класс ReviewScraper, который инкапсулирует функциональность скрапинга отзывов.
#Внесены изменения для использования параметров запроса и констант для URL и папок.
#Созданы методы fetch_reviews, create_review_url, get_review_folder и save_preview_to_file для декомпозиции функциональности.

import os
import requests
from bs4 import BeautifulSoup
# Инициализация объекта ReviewScraper
class ReviewScraper:
    def __init__(self, film_id, max_pages):
        self.film_id = film_id  # ID фильма на КиноПоиске
        self.max_pages = max_pages  # Максимальное количество страниц для обработки
        current_directory = os.path.dirname(__file__)  # Получаем текущую директорию скрипта
        self.good_folder = os.path.join(current_directory, 'good')  # Папка для хранения хороших отзывов
        self.bad_folder = os.path.join(current_directory, 'bad')  # Папка для хранения плохих отзывов
        os.makedirs(self.good_folder, exist_ok=True)  # Создаем папку good, если она не существует
        os.makedirs(self.bad_folder, exist_ok=True)  # Создаем папку bad, если она не существует
    # Метод для получения и сохранения отзывов
    def fetch_reviews(self):
        for review_type in ['good', 'bad']:
            for page in range(1, self.max_pages + 1):
                url = self.create_review_url(review_type, page)  # Создаем URL для страницы с отзывами
                response = requests.get(url)  # Отправляем GET-запрос к URL

                if response.status_code != 200:
                    print(f"Не удалось подключится.")
                    continue  # Пропускаем текущую страницу, если нет ответа от сервера

                soup = BeautifulSoup(response.text, 'html.parser')  # Парсим HTML страницы
                reviews = soup.find_all('div', {'itemprop': 'reviews'})  # Находим блоки с отзывами

                for i, review in enumerate(reviews):
                    film_name = soup.find('a', class_='breadcrumbs__link').text  # Получаем название фильма
                    review_text = review.find('span', {'itemprop': 'reviewBody'}).text  # Получаем текст отзыва
                    review_text_with_film_name = f'Фильм: {film_name}\n\n{review_text}'  # Добавляем название фильма
                    filename = os.path.join(self.get_review_folder(review_type),
                                            f'{str(i + (page - 1) * 10).zfill(4)}.txt')  # Создаем имя файла
                    self.save_review_to_file(filename, review_text_with_film_name)  # Сохраняем отзыв в файл
    # Метод для создания URL страницы с отзывами
    def create_review_url(self, review_type, page):
        return f'https://www.kinopoisk.ru/film/{self.film_id}/reviews/ord/rating/status/{review_type}/perpage/200/page/{page}/'
    # Метод для определения папки (good или bad) для хранения отзывов
    def get_review_folder(self, review_type):
        return self.good_folder if review_type == 'good' else self.bad_folder
    # Метод для сохранения отзыва в текстовый файл
    def save_review_to_file(self, filename, review_text):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(review_text)

def main():
    film_id = '251733'  # Заменяю на ID фильма с КиноПоиска
    max_pages = 2  # Максимальное количество страниц для обработки (по умолчанию 2)

    scraper = ReviewScraper(film_id, max_pages)  # Создаем экземпляр класса ReviewScraper
    scraper.fetch_reviews()  # Вызываем метод для получения и сохранения отзывов

    print('Готово')

if __name__ == "__main__":
    main()
