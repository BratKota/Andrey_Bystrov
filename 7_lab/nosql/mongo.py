import os
import pymongo
import json

# Получение текущего рабочего каталога
current_dir = os.path.dirname(os.path.abspath(__file__))

# Путь к JSON файлу
json_file = os.path.join(current_dir, "aircraft.json")

# Подключение к MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")  # Замените на ваш адрес MongoDB

# Создание новой базы данных
new_db_name = "test"
new_db = client[new_db_name]

# Создание коллекции
collection_name = "test"
collection = new_db[collection_name]

# Чтение данных из JSON файла
with open(json_file) as f:
    data = json.load(f)

# Вставка данных в коллекцию, сохраняя названия ключей
collection.insert_one(data)




