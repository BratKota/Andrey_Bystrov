#Рефакторинг:
#Создал класс ImageDownloader, чтобы инкапсулировать функциональность загрузки изображений и сделать код более организованным.
#Вынес инициализацию веб-драйвера Chrome и его завершение в методы initialize_webdriver и download_images соответственно.
#Заменил жестко закодированные строки пути на использование переменных

import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import shutil
import requests

#ImageDownloader, который инкапсулирует функциональность загрузки изображений.
class ImageDownloader:
    def __init__(self, query, folder_name, num_images):
        self.query = query  # Поисковый запрос (например, "собака" или "кошка")
        self.folder_name = folder_name  # Имя папки, в которую будут сохранены изображения
        self.num_images = num_images  # Количество изображений, которые нужно загрузить
        current_directory = os.path.dirname(__file__)  # Получаем текущую директорию скрипта
        self.base_folder = os.path.join(current_directory, self.folder_name)  # Создаем папку в текущей директории
    # Создает базовую папку, если она не существует
    def create_base_folder(self):
        if not os.path.exists(self.base_folder):
            os.makedirs(self.base_folder)
    # Метод для загрузки изображений
    def download_images(self):
        self.create_base_folder()  # Создаем базовую папку, если она не существует
        driver = self.initialize_webdriver()  # Используем метод для инициализации веб-драйвера
        try:
            urls = self.fetch_image_urls(driver)  # Получаем список URL-адресов изображений
            self.save_images(urls)  # Сохраняем изображения
        finally:
            driver.quit()  
    # Инициализация веб-драйвера Chrome с опцией --headless (без графического интерфейса)
    def initialize_webdriver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        return webdriver.Chrome(options=chrome_options)
    # Метод для получения URL-адресов изображений с веб-страницы
    def fetch_image_urls(self, driver):
        urls = []
        url = f"https://yandex.ru/images/search?text={self.query}"
        
        driver.get(url)

        scroll_count = 0
        max_images = self.num_images

        while len(urls) < max_images:
            driver.execute_script("window.scrollBy(0, window.innerHeight)")
            scroll_count += 1
            time.sleep(1)

            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            img_tags = soup.find_all('img', class_='serp-item__thumb justifier__thumb')
            new_urls = [img['src'] for img in img_tags]

            new_urls = list(set(new_urls))
            urls.extend(new_urls)
            urls = list(set(urls))
            if len(new_urls) == 0:
                break
            if len(urls) > max_images:
                urls = urls[:max_images]

        return urls
    # Метод для скачивания и сохранения изображений по URL-адресам
    def save_images(self, urls):
        for i, url in enumerate(urls):
            if url.startswith('//'):
                url = 'https:' + url
            response = requests.get(url, stream=True)
            file_name = os.path.join(self.base_folder, f"{str(i).zfill(4)}.jpg")
            with open(file_name, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            print(f"Downloaded {file_name}")

def main():
    # Создаем экземпляры класса ImageDownloader для скачивания изображений с запросами "собака" и "кошка"
    # и указываем количество изображений, которые нужно загрузить
    downloader_dog = ImageDownloader("dog", "dog", num_images=10)
    downloader_cat = ImageDownloader("cat", "cat", num_images=10)

    # Запускаем процесс загрузки изображений для каждого запроса
    downloader_dog.download_images()
    downloader_cat.download_images()

    print('Готов')

if __name__ == "__main__":
    main()