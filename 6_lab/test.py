import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.metrics import mean_absolute_error
import numpy as np
from xgboost import XGBRegressor
import os
from catboost import CatBoostRegressor
#Обучение модели
def train_and_evaluate_model(model, model_params, X_train, y_train, X_test, y_test, result_file):
    # Инициализация модели с указанными параметрами
    model = model(**model_params)
    # Обучение модели
    model.fit(X_train, y_train)
    # Получение строкового представления модели с её параметрами
    model_description = str(model)
    # Получение параметров модели
    model_params = model.get_params()
    # Предсказание на тестовых данных
    predictions = model.predict(X_test)
    # Оценка качества модели
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)
    mape = np.mean(np.abs((y_test - predictions) / y_test)) * 100
    pearson_corr = np.corrcoef(y_test, predictions)[0, 1]

     # Вывод результатов на консоль
    print("\nМодель: {}\n".format(model_description))
    print("Параметры модели:")
    for param, value in model_params.items():
        print("{}: {}".format(param, value))
    print("Средняя абсолютная ошибка (MAE) на тестовых данных: {}".format(mae))
    print("Средняя абсолютная процентная ошибка (MAPE) на тестовых данных: {}".format(mape))
    print("Коэффициент корреляции Пирсона на тестовых данных: {}".format(pearson_corr))
    print("Среднеквадратичная ошибка на тестовых данных: {}".format(mse))
    print("Коэффициент детерминации (R^2) на тестовых данных: {}".format(r2))

    # Запись результатов в файл
    with open(result_file, 'a') as file:
        file.write("\nМодель: {}\n".format(model_description))
        file.write("Параметры модели:\n")
        for param, value in model_params.items():
            file.write("{}: {}\n".format(param, value))
        file.write("\nСредняя абсолютная ошибка (MAE) на тестовых данных: {}\n".format(mae))
        file.write("Средняя абсолютная процентная ошибка (MAPE) на тестовых данных: {}\n".format(mape))
        file.write("Коэффициент корреляции Пирсона на тестовых данных: {}\n".format(pearson_corr))
        file.write("Среднеквадратичная ошибка на тестовых данных: {}\n".format(mse))
        file.write("Коэффициент детерминации (R^2) на тестовых данных: {}\n".format(r2))
# Путь к файлу для записи результатов
result_file = "results.txt"

# Загрузка данных из CSV файла с явным указанием разделителя
data = pd.read_csv('dataset.csv', delimiter=';')

# Преобразование столбца 'Date' в формат даты
data['Date'] = pd.to_datetime(data['Date'], format='%d.%m.%Y')

# Удаление строк с некорректными значениями или пустыми строками
data.dropna(inplace=True)
data = data[data['Value'].apply(lambda x: str(x).replace('.', '').isdigit())]

# Перемешивание данных
data = data.sample(frac=1, random_state=42).reset_index(drop=True)

# Посмотрим на структуру данных после изменений
print(data.head())

# Определение границы разделения данных (80% данных для обучения, 20% для прогноза)
split_date = int(len(data) * 0.8)

# Разделение данных
train_data = data.iloc[:split_date]
test_data = data.iloc[split_date:]
print("\n"+"Размеры обучающего и тестового наборов данных:")
print("Обучающий набор данных:", train_data.shape)
print("Тестовый набор данных:", test_data.shape)

# Сохранение обучающего и тестового наборов данных в файлы CSV
train_data.to_csv('train_data.csv', index=False)
test_data.to_csv('test_data.csv', index=False)

# Загрузка обучающих и тестовых данных
train_data = pd.read_csv('train_data.csv')
test_data = pd.read_csv('test_data.csv')

# Преобразование даты в числовой формат (может потребоваться для модели линейной регрессии)
train_data['Date'] = pd.to_numeric(pd.to_datetime(train_data['Date']))
test_data['Date'] = pd.to_numeric(pd.to_datetime(test_data['Date']))

# Подготовка данных для обучения модели
X_train = train_data[['Date']]  # используем только дату как признак
y_train = train_data['Value']  # значения курса рубля

X_test = test_data[['Date']]  # используем только дату как признак
y_test = test_data['Value']  # значения курса рубля

#1 Линейная регрессия 
model_lin= {
    'fit_intercept': True,
    'copy_X': True,
    'n_jobs': None,
    'positive': True
}
#2 Линейная регрессия с другими параметрами 
model_lin_2= {
    'fit_intercept': True,
    'copy_X': False,
    'n_jobs': None,
    'positive': False
}
#Запуск линейной регресии
train_and_evaluate_model(LinearRegression, model_lin, X_train, y_train, X_test, y_test, "results.txt")
train_and_evaluate_model(LinearRegression, model_lin_2, X_train, y_train, X_test, y_test, "results.txt")

#3 CatBoostRegressor
iterations = 1000   # Количество итераций обучения
learning_rate = 0.1 # Скорость обучения
depth = 6 # Глубина деревьев
loss_function = 'RMSE' # Функция потерь (корень из среднеквадратичной ошибки)
random_seed = 42 # Зафиксированный seed для воспроизводимости результатов
verbose = False  # Параметр, определяющий вывод информации о процессе обучения
#Запуск CatBoostRegressor
train_and_evaluate_model(CatBoostRegressor, {"iterations": iterations, "learning_rate": learning_rate, "depth": depth, "loss_function": loss_function, "random_seed": random_seed, "verbose": verbose}, X_train, y_train, X_test, y_test, "results.txt")

#4 CatBoostRegressor с другими параметрами
iterations = 1500   # Количество итераций обучения
learning_rate = 0.05 # Скорость обучения
depth = 8 # Глубина деревьев
loss_function = 'MAE' # Функция потерь (корень из среднеквадратичной ошибки)
random_seed = 42 # Зафиксированный seed для воспроизводимости результатов
verbose = False  # Параметр, определяющий вывод информации о процессе обучения
#Запуск CatBoostRegressor
train_and_evaluate_model(CatBoostRegressor, {"iterations": iterations, "learning_rate": learning_rate, "depth": depth, "loss_function": loss_function, "random_seed": random_seed, "verbose": verbose}, X_train, y_train, X_test, y_test, "results.txt")

#5 XGBoostRegressor
params_xgb = {
    'n_estimators': 1000,   # Количество деревьев в ансамбле
    'learning_rate': 0.1,   # Скорость обучения
    'max_depth': 6,         # Максимальная глубина деревьев
    'objective': 'reg:squarederror',  # Функция потерь (в данном случае - среднеквадратичная ошибка)
    'random_state': 42      # Зафиксированный seed для воспроизводимости результатов
}
#Запуск XGBoostRegressor
train_and_evaluate_model(XGBRegressor, params_xgb, X_train, y_train, X_test, y_test, "results.txt")

#5 XGBoostRegressor с другими параметрами
# Новые параметры для XGBoostRegressor
params_xgb = {
    'objective': 'reg:squarederror',  # Функция потерь для регрессии
    'eval_metric': 'rmse',             # Метрика оценки модели
    'max_depth': 8,                    # Максимальная глубина дерева
    'learning_rate': 0.05,             # Скорость обучения
    'n_estimators': 500,               # Количество деревьев
    'subsample': 0.8,                  # Доля подвыборки для обучения каждого дерева
    'colsample_bytree': 0.8,           # Доля признаков для обучения каждого дерева
    'random_state': 42                 # Зафиксированный seed для воспроизводимости результатов
}

#Запуск XGBoostRegressor
train_and_evaluate_model(XGBRegressor, params_xgb, X_train, y_train, X_test, y_test, "results.txt")
print("Готово")