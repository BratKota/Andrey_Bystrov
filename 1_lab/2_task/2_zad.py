import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import shutil
import requests

def download_images(query, folder_name, num_images):
    if not os.path.exists('2_task/dataset'):
        os.makedirs('2_task/dataset')

    folder_path = os.path.join('2_task/dataset', folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    # Инициализируем веб-драйвер Chrome
    driver = webdriver.Chrome()
    urls = []  # Объявляем список для хранения URL-адресов изображений

    try:
        url = f"https://yandex.ru/images/search?text={query}"
        driver.get(url)

        scroll_count = 0
        max_images = num_images

        
        # Прокручиваем страницу до получения необходимого количества изображений,путем проверки кол-во фото и url
        while len(urls) < max_images:
            driver.execute_script("window.scrollBy(0, window.innerHeight)")
            scroll_count += 1
            time.sleep(1)

            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            img_tags = soup.find_all('img', class_='serp-item__thumb justifier__thumb')
            new_urls = [img['src'] for img in img_tags]
            # Убираем дубликаты URL-адресов и добавляем новые 
            new_urls = list(set(new_urls))
            urls.extend(new_urls)
            urls = list(set(urls))
            if len(new_urls) == 0:
                break
            if len(urls) > max_images:
                urls = urls[:max_images]
        # Скачиваем изображения по URL-адресам
        for i, url in enumerate(urls):
            if url.startswith('//'):
                url = 'https:' + url
            response = requests.get(url, stream=True)
            file_name = os.path.join(folder_path, f"{str(i).zfill(4)}.jpg")
            with open(file_name, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            print(f"Downloaded {file_name}")
        

    finally:
        driver.quit()
download_images("dog", "dog", num_images=30)
download_images("cat", "cat", num_images=30)

print('Готов')
