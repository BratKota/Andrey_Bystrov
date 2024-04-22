import sqlite3

# Устанавливаем соединение с базой данных SQLite
conn = sqlite3.connect('database.sqlite')

# Создаем курсор для выполнения SQL-запросов
cursor = conn.cursor()

#1задание Выполняем запрос к таблице "Team" и извлекаем данные
cursor.execute("SELECT * FROM Team")
city_data = cursor.fetchall()
#2 поулчаем скелет базы данных
schema = "\n".join(conn.iterdump())
# Выводим данные
for row in city_data:
    print(row)

# Закрываем соединение с базой данных

conn.close()

#2 задание. Сохраняем скелет базы данных в файл schema.sql в текущей директории
with open('schema.sql', 'w') as f:
    f.write(schema)