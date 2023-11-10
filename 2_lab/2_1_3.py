#Написать скрипт, который разобъёт исходный csv файл на N файлов, где каждый отдельный файл будет соответствовать одной неделе.
import os
import pandas as pd

# Получаю список всех файлов в текущей директории
def find_csv_files():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    files_in_directory = os.listdir(current_directory)
    csv_files = []
    for file in files_in_directory:
        if file.endswith('.csv'):
            csv_files.append(os.path.join(current_directory, file))

    if not csv_files:
        raise FileNotFoundError("CSV файлы не найдены в текущей директории.")
    
    return csv_files

# Выполнение
def split_csv_by_week(input_csv_file):
    date_column = 'Date'
    df = pd.read_csv(input_csv_file, delimiter=';', parse_dates=[date_column], dayfirst=True)
    script_directory = os.path.dirname(__file__)
    output_directory = os.path.join(script_directory, '3 Задание')
    os.makedirs(output_directory, exist_ok=True)
    date_ranges = pd.date_range(start=df[date_column].min(), end=df[date_column].max(), freq='W-MON')

    # Разбиваем данные по неделям и сохраняем в отдельные файлы
    split_dataframes = []
    for i in range(len(date_ranges) - 1):
        start_date = date_ranges[i].strftime('%Y%m%d')
        end_date = date_ranges[i + 1].strftime('%Y%m%d')

        week_data = df[(df[date_column] >= date_ranges[i]) & (df[date_column] < date_ranges[i + 1])]

        if not week_data.empty:
            split_dataframes.append((week_data, os.path.join(output_directory, f'{start_date}_{end_date}.csv')))

    return split_dataframes

# Сохраняем
def save_to_csv(df, output_csv_file):
    df.to_csv(output_csv_file, sep=';', index=False)

# Запуск
def process_csv_files_3():
    try:
        input_csv_files = find_csv_files()
        
        for input_csv_file in input_csv_files:
            split_dataframes = split_csv_by_week(input_csv_file)
            for split_dataframe, output_csv_file in split_dataframes:
                save_to_csv(split_dataframe, output_csv_file)

    except FileNotFoundError as e:
        print(e)

def main():
    process_csv_files_3()

if __name__ == "__main__":
    main()
