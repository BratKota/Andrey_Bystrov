#Написать скрипт, который разобъёт исходный csv файл на N файлов, где каждый отдельный файл будет соответствовать одному году.
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
#Выполнение
def split_csv_file_2(input_csv_file):
    df = pd.read_csv(input_csv_file, delimiter=';', parse_dates=['Date'], dayfirst=True)
    years = pd.to_datetime(df['Date']).dt.year.unique()
    
    split_dataframes = []

    for year in years:
        start_date = f'{year}0101'
        end_date = f'{year}1231'
        filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
        split_dataframes.append(filtered_df)

    return split_dataframes
#Сохраняем
def save_split_csv_files_2(split_dataframes):
    output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Папка по годам')
    os.makedirs(output_folder, exist_ok=True)

    for i, df in enumerate(split_dataframes):
        year = pd.to_datetime(df['Date']).dt.year.unique()[0]
        start_date = f'{year}0101'
        end_date = f'{year}1231'
        file_name = f'{start_date}_{end_date}.csv'
        output_csv_file = os.path.join(output_folder, file_name)
        df.to_csv(output_csv_file, sep=';', index=False)

    print(f'Файлы разбиты и сохранены')
#Запуск
def process_csv_files_2():
    try:
        input_csv_files = find_csv_files()
        
        for input_csv_file in input_csv_files:
            split_dataframes = split_csv_file_2(input_csv_file)
            save_split_csv_files_2(split_dataframes)

    except FileNotFoundError as e:
        print(e)
def main():
    process_csv_files_2()

if __name__ == "__main__":
    main()