# 4.py

import os
import pandas as pd
from datetime import datetime
import sys

# Функция для разбиения CSV файла на N файлов по неделям
def get_data_for_date(input_csv_file, target_date):
    date_column = 'Date'
    df = pd.read_csv(input_csv_file, delimiter=';', parse_dates=[date_column], dayfirst=True)

    # Выбираем данные для указанной даты
    target_data = df[df[date_column].dt.strftime('%d.%m.%Y') == target_date.strftime('%d.%m.%Y')]

    if not target_data.empty:
        return target_data
    else:
        return None

# Функция для сохранения данных в CSV файл
def save_to_csv(df, output_csv_file):
    df.to_csv(output_csv_file, sep=';', index=False)

# Изменяем функцию main, чтобы она принимала дату в качестве параметра
def main(target_date_str):
    # Получить текущую директорию
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Собрать полный путь к CSV файлу в текущей директории
    input_csv_file = os.path.join(current_directory, "dataset.csv")
    
    try:
        # Попробовать преобразовать введенную строку в объект datetime
        target_date = datetime.strptime(target_date_str, "%Y-%m-%d")
        # Преобразовать объект datetime в нужный формат
        target_date_str = target_date.strftime("%d.%m.%Y")
    except ValueError as e:
        print(f"Ошибка в формате даты: {e}")
        return


    data_for_date = get_data_for_date(input_csv_file, target_date)

    if data_for_date is not None:
        print(data_for_date['Value'].values[0])
        return data_for_date['Value'].values[0]
    else:
        print(f"Данных для даты {target_date_str} нет.")
        return None

# Пример вызова функции main с передачей даты в качестве параметра
if __name__ == "__main__":
    # Проверяем, есть ли аргументы командной строки
    if len(sys.argv) > 1:
        # Если есть, передаем первый аргумент (дату) в функцию main
        main(sys.argv[1])
    else:
        print("Необходимо передать дату в качестве аргумента командной строки.")
