#Написать скрипт, содержащий функцию, принимающую на вход дату (тип datetime) и возвращающий данные для этой даты (из файла) 
#или None если данных для этой даты нет.
import os
import pandas as pd
from datetime import datetime

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

def main():
    # Получить текущую директорию
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Собрать полный путь к CSV файлу в текущей директории
    input_csv_file = os.path.join(current_directory, "dataset.csv")
    
    # Запросить пользователя ввести дату
    target_date_str = input("Введите дату в формате dd.mm.yyyy: ")
    
    try:
        # Попробовать преобразовать введенную строку в объект datetime
        target_date = datetime.strptime(target_date_str, "%d.%m.%Y")
    except ValueError:
        print("Ошибка в формате даты. Пожалуйста, введите дату в правильном формате.")
        return

    data_for_date = get_data_for_date(input_csv_file, target_date)

    if data_for_date is not None:
        print(f"Значение для даты {target_date_str}:")
        print(data_for_date['Value'].values[0])
    else:
        print(f"Данных для даты {target_date_str} нет.")


if __name__ == "__main__":
    main()
