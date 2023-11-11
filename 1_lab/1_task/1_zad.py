import requests
import xml.etree.ElementTree as ET
import csv
import os

# URL для получения данных
url = "http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1=01/07/1992&date_req2=15/09/2023&VAL_NM_RQ=R01235"

# Отправляем запрос на сервер
response = requests.get(url)

# Парсим ответ сервера с помощью ElementTree
root = ET.fromstring(response.content)

# Открываем файл для записи данных
with open(os.path.join("C:\\Users\\Andrey\\Desktop\\piton\\1_task", "dataset.csv"), 'w', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(["Date", "Value"])  # Заголовки столбцов

    # Извлекаем данные из каждой записи
    for record in root.findall('Record'):
        date = record.get('Date')
        value = record.find('Value').text.replace(',', '.')
        # Записываем данные в файл
        writer.writerow([date, value])
print('Готово')