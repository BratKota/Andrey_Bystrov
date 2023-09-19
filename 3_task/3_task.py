import os
import requests
from bs4 import BeautifulSoup

# Создайте папки для хранения отзывов
os.makedirs('3_task/dataset/good', exist_ok=True)
os.makedirs('3_task/dataset/bad', exist_ok=True)

# Список фильмов для анализа Автар(больше 1000 отзывов,но возьмем 100 отзывов,чтобы не было капчи )
films = ['251733']  # Замените на ID фильмов с КиноПоиска

for film in films:
    for review_type in ['good', 'bad']:
        for page in range(1, 2):  # Обработка 200 страниц отзывов
            url = f'https://www.kinopoisk.ru/film/{film}/reviews/ord/rating/status/{review_type}/perpage/200/page/{page}/'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            reviews = soup.find_all('div', {'itemprop': 'reviews'})

            for i, review in enumerate(reviews):
                film_name = soup.find('a', class_='breadcrumbs__link').text
                review_text = review.find('span', {'itemprop': 'reviewBody'}).text
                review_text_with_film_name = f'Фильм: {film_name}\n\n{review_text}'
                filename = f'3_task/dataset/{review_type}/{str(i + (page - 1) * 10).zfill(4)}.txt'
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(review_text_with_film_name)
print('готово')
