import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Функция для фильтрации по отклонению от среднего значения
def filter_by_deviation(dataframe, deviation_threshold):
    filtered_df = dataframe[dataframe['mean_deviation'] >= deviation_threshold]
    print("\nОтфильтрованный DataFrame по значение отклонения от среднего значения курса :")
    print(filtered_df)
# Функция для фильтрации по датам
def filter_by_date(dataframe, start_date, end_date):
    # Преобразование столбца 'date' в формат datetime с заданным форматом
    dataframe['date'] = pd.to_datetime(dataframe['date'], format='%d.%m.%Y', errors='coerce')
    # Преобразование начальной и конечной даты в формат datetime
    start_date = pd.to_datetime(start_date, format='%d.%m.%Y')
    end_date = pd.to_datetime(end_date, format='%d.%m.%Y')
    # Фильтрация по датам
    filtered_df = dataframe[(dataframe['date'] >= start_date) & (dataframe['date'] <= end_date)]
    print("\nОтфильтрованный DataFrame по датам:")
    print(filtered_df)
# Функция для отрисовки по месяцу
def plot_currency_stats_for_month(dataframe, target_month_year):
    # Преобразование столбца 'date' в формат datetime
    dataframe['date'] = pd.to_datetime(dataframe['date'], format='%d.%m.%Y', errors='coerce')
    # Фильтрация данных по указанному месяцу и году
    target_month = pd.to_datetime(target_month_year, format='%Y.%m', errors='coerce')
    filtered_data = dataframe[(dataframe['date'].dt.month == target_month.month) & (dataframe['date'].dt.year == target_month.year)]
    # Построение графика изменения курса за месяц
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='date', y='value', data=filtered_data, marker='o', label='Курс')
    # Добавление горизонтальных линий для среднего значения и медианы
    plt.axhline(y=filtered_data['value'].mean(), color='red', linestyle='dashed', label='Среднее значение')
    plt.axhline(y=filtered_data['value'].median(), color='green', linestyle='dashed', label='Медиана')
    plt.title(f'График изменения курса за {target_month_year}')
    plt.xlabel('Дата')
    plt.ylabel('Курс')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()
# Проверка на ошибки
def error(dataframe):
    df=dataframe
    df = pd.read_csv(df, sep=';')
    # Именование колонок
    df.columns = [col.lower().replace(' ', '_') for col in df.columns]
    print(df)
    # Преобразование столбца 'date' в формат datetime с заданным форматом
    df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y', errors='coerce')
    # Преобразование столбца 'Value' в числовой тип
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    # Замена невалидных значений на np.nan
    df['value'] = df['value'].replace('невалидное значение', np.nan)
    print("\nКоличество невалидных значений в каждой колонке:")
    print(df.isnull().sum())
    print("\nПроцент невалидных значений в каждой колонке:")
    print(df.isnull().mean())
    # Или удаление строк с невалидными значениями
    df = df[df['value'].notna()]

    # Проверка на наличие невалидных значений в колонках
    print("\nКоличество невалидных значений в каждой колонке,после удаления:")
    print(df.isnull().sum())
    print("\nПроцент невалидных значений в каждой колонке,после удаления:")
    print(df.isnull().mean())
    return df
# Отклонения
def deviation(dataframe):
    print("\nОтклонения:")
    # Добавление столбцов с отклонением от медианы и среднего значения курса
    dataframe['median_deviation'] = dataframe['value'].median() - dataframe['value']
    dataframe['mean_deviation'] = dataframe['value'].mean() - dataframe['value']
    dataframe['calculated_column'] = dataframe['median_deviation'] + dataframe['mean_deviation']
    # Вывод обновленного DataFrame
    print(dataframe)
# Cтатистическая информация
def statistics(dataframe):
    # Вычисление статистической информации
    stat_info = dataframe[['value', 'median_deviation', 'mean_deviation', 'calculated_column']].describe()
    # Вывод статистической информации
    print("\nСтатистическая информация:")
    print(stat_info)
    # Построение графика boxplot
    plt.figure(figsize=(10, 6))
    dataframe[['value', 'median_deviation', 'mean_deviation', 'calculated_column']].boxplot()
    plt.title("Boxplot для курса и отклонений")
    plt.show()
# Сортировка по месяцам
def group_month(dataframe):
    # Преобразование столбца 'date' в формат datetime с заданным форматом
    dataframe['date'] = pd.to_datetime(dataframe['date'], format='%d.%m.%Y', errors='coerce')
    # Группировка по месяцу с вычислением среднего значения курса
    monthly_avg = dataframe.groupby(dataframe['date'].dt.to_period("M")).agg({'value': 'mean'}).reset_index()
    # Вывод среднего значения курса по месяцам
    print("\nСреднее значение курса по месяцам:")
    print(monthly_avg)
    # Построение графика среднего значения курса по месяцам
    plt.figure(figsize=(10, 6))
    plt.plot(monthly_avg['date'].astype(str), monthly_avg['value'], marker='o')
    plt.title("Среднее значение курса по месяцам")
    plt.xlabel("Месяц")
    plt.ylabel("Среднее значение курса")
    plt.xticks(rotation=45)  # Поворот подписей по оси X для лучшей читаемости
    plt.tight_layout()
    plt.show()
def all_period(dataframe):
    # Сортировка DataFrame по дате
    df = dataframe.sort_values(by='date')
    # Установка стиля seaborn
    sns.set(style="whitegrid")
    # Построение графика с использованием seaborn
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='date', y='value', data=df, marker='o', label='Курс')
    plt.title('График изменения курса за весь период')
    plt.xlabel('Дата')
    plt.ylabel('Курс')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()
def main():
    # Имя  CSV-файла
    file_name = 'dataset.csv'
    # Обработка ошибок и подготовка данных
    df = error(file_name)
    # Вычисление отклонений и статистики
    deviation(df)
    statistics(df)
    # Использование функции для фильтрации по отклонению
    deviation_threshold = 488  # Задаю значение отклонения, с которым мы хотим фильтровать
    filter_by_deviation(df, deviation_threshold)
    # Использование функции для фильтрации по датам
    start_date = '26.08.2022'  # Задаю начальную дату
    end_date = '12.11.2022'    # Задаю конечную дату
    filter_by_date(df, start_date, end_date)
    # Группировка по месяцам
    group_month(df)
    # Построение графика для всего периода
    all_period(df)
    #функция для отрисовки по месяцу
    target_month_year = '2022.02'  #месяц с годом
    plot_currency_stats_for_month(df, target_month_year)
# Вызов функции main
if __name__ == "__main__":
    main()
