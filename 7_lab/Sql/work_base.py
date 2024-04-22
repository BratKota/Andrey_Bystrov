import sqlite3
import os

def execute_sql_from_file(cursor, filename):
    with open(filename, 'r') as f:
        sql_commands = f.read()
        cursor.executescript(sql_commands)

# Проверяем наличие файла new_base.db
if not os.path.exists('new_base.db'):
    # Если файл не существует, создаем соединение с новой базой данных SQLite с именем new_base.db
    conn = sqlite3.connect('new_base.db')

    # Создаем курсор для выполнения SQL-запросов
    cursor = conn.cursor()

    # Выполняем SQL-запросы из файла schema.sql для создания базы данных
    execute_sql_from_file(cursor, 'schema.sql')

    # Закрываем соединение с базой данных
    print("База созданна")
    conn.close()

# Устанавливаем соединение с базой данных SQLite с именем new_base.db
conn = sqlite3.connect('new_base.db')

# Создаем курсор для выполнения SQL-запросов
cursor = conn.cursor()

# Добавим  SQL-запросы 
sql_queries = """
-- Чтение данных:Список городов
SELECT * FROM City;

--Чтение данных с условием:Список игроков из Австралии
SELECT *FROM Player JOIN Country ON Player.Country_Name = Country.Country_Id WHERE Country.Country_Name = 'Australia';

--Чтение определенных столбцов:Список игроков и их id страны
SELECT Player_Name, Country_Name FROM Player;

--Изменение данных:Поменяли название города
UPDATE City SET City_Name = 'Los Angeles' WHERE City_Id = 1;

--Добавление данных:Добавили город
INSERT INTO City (City_Name, Country_Id) VALUES ('Moskow', '2');

--Удаление данных:Удалили Москву
DELETE FROM City WHERE City_Name = 'Moskow';


--Использование подзапроса:Команды из ЮАР
SELECT * FROM City WHERE Country_id IN (SELECT Country_id FROM Country WHERE Country_Name = 'South Africa');

--Использование оператора LIKE:Поиск городов,начинающие на R
SELECT * FROM City WHERE City_name LIKE 'R%';

--Использование агрегатной функции для вычисления среднего значения:Среднее количество ударов
SELECT AVG(Striker) FROM Ball_by_Ball;

--Использование сортировки:Матчи где разница очков была от 5 до 10 в порядке убывания
SELECT * FROM Match WHERE Win_Margin BETWEEN 5 AND 10 ORDER BY Win_Margin DESC;
"""





# Сохраняем SQL-запросы в файл test-queries.sql
with open('test-queries.sql', 'w') as f:
    f.write(sql_queries)

# Закрываем соединение с базой данных
conn.close()
print('Готово')