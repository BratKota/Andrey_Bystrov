#Рефакторинг:
#Добавлен класс CurrencyData для удобного хранения данных о валюте.
#Добавлена функция get_current_directory, которая определяет текущую директорию скрипта.
#Функциональность разделена на более мелкие методы
#Параметры запроса, выбор браузера и URL теперь вынесены в начало скрипта и могут быть легко настроены.
import requests
import xml.etree.ElementTree as ET
import csv
import os
# Создаем класс CurrencyData для хранения данных о валюте
class CurrencyData:
    def __init__(self, date, value):
        self.date = date
        self.value = value
# Функция для получения текущей директории скрипта
def get_current_directory():
    return os.path.dirname(os.path.realpath(__file__))
# Функция для получения данных о валюте
def fetch_currency_data(currency_code, start_date, end_date):
    url = f"http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1={start_date}&date_req2={end_date}&VAL_NM_RQ={currency_code}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Не удалось получить данные с сервера!")
    
    return ET.fromstring(response.content)
# Функция для сохранения данных о валюте в CSV файл
def save_currency_data_to_csv(currency_data, file_path):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(["Date", "Value"])  

        for data_point in currency_data:
            writer.writerow([data_point.date, data_point.value])

def main():
    currency_code = "R01235"
    start_date = "01/07/1992"
    end_date = "15/09/2023"

    currency_data = []
    root = fetch_currency_data(currency_code, start_date, end_date)
    for record in root.findall('Record'):
        date = record.get('Date')
        value = record.find('Value').text.replace(',', '.')
        currency_data.append(CurrencyData(date, value))

    file_path = os.path.join(get_current_directory(), "dataset.csv")
    save_currency_data_to_csv(currency_data, file_path)
    print('Готово')

if __name__ == "__main__":
    main()