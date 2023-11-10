#Написать скрипт, который разобъёт исходный csv файл на файл X.csv и Y.csv, с одинаковым количеством строк. 
import os
import pandas as pd
# Получваю список всех файлов в текущей директории
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
def split_csv_file(input_csv_file):
    df = pd.read_csv(input_csv_file, delimiter=';')
    # Раздяет DataFrame на два, учитывая количество строк
    half_rows = len(df) // 2
    df_x = df.iloc[:half_rows, 0:1]  # Взять первую половину столбцов
    df_y = df.iloc[half_rows:, 1:]  # Взять вторую половину столбцов

    return df_x, df_y
#Сохранение
def save_to_csv(df, output_csv_file):
    df.to_csv(output_csv_file, sep=';', index=False)
#Запуск
def process_csv_files():
    try:
        input_csv_files = find_csv_files()

        # Создаю папку для файлов
        output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '1 Задание')
        os.makedirs(output_folder, exist_ok=True)

        # Перебераю все найденные .csv файлы
        for input_csv_file in input_csv_files:
            df_x, df_y = split_csv_file(input_csv_file)

            # Указываю путь для сохранения файлов
            file_name = os.path.basename(input_csv_file)
            output_x_csv_file = os.path.join(output_folder, f'X_{file_name}')
            output_y_csv_file = os.path.join(output_folder, f'Y_{file_name}')

            save_to_csv(df_x, output_x_csv_file)
            save_to_csv(df_y, output_y_csv_file)

        print(f'Файлы X.csv и Y.csv созданы успешно')
    except FileNotFoundError as e:
        print(e)

def main():
    process_csv_files()

if __name__ == "__main__":
    main()