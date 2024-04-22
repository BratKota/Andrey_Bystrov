import sqlite3
import pandas as pd

# Устанавливаем соединение с базой данных SQLite с именем new_base.db
conn = sqlite3.connect('new_base.db')

# Функция для выполнения SQL-запросов из файла и сохранения результатов в DataFrame
def execute_sql_from_file_to_dataframe(conn, filename):
    cursor = conn.cursor()
    with open(filename, 'r') as f:
        sql_commands = f.read()
        for sql_command in sql_commands.split(';'):
            sql_command = sql_command.strip()
            if sql_command:
                if '--' in sql_command:
                    print("\nЗапрос:", sql_command.split('--')[1].strip().split('\n')[0])
                else:
                    print("Запрос:")
                cursor.execute(sql_command)
                data = cursor.fetchall()
                if data:
                    df = pd.DataFrame(data, columns=[x[0] for x in cursor.description])
                    print(df)
                else:
                    print("Сделано")
                print()

# Выполняем SQL-запросы из файла test-queries.sql
execute_sql_from_file_to_dataframe(conn, 'test-queries.sql')

# Закрываем соединение с базой данных
conn.close()
