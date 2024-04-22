import os
import pymongo
import random
import json
# Подключение к MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")  # Подставьте свой адрес MongoDB
db = client["test"]  
collection = db['test']

# Извлечение списка всех пилотов
pilots = collection.find_one({})['pilot']
# Вывод списка всех пилотов
print("Вывод списка всех пилотов:")
for pilot in pilots:
    print(f"Name: {pilot['Name']}, Age: {pilot['Age']}")

# Вывод пилотов определенного возраста
age_threshold = 27
print(f"\nПилоты страше 27:")
older_pilots = collection.find({"pilot.Age": {"$gt": age_threshold}})
for pilot in older_pilots:
    for p in pilot['pilot']:
        if p['Age'] > age_threshold:
            print(f"Name: {p['Name']}, Age: {p['Age']}")

# Получение информации о конкретном пилоте по его ID
pilot_id = 2  
specific_pilot = collection.find_one({"pilot.Pilot_Id": pilot_id})
if specific_pilot:
    for pilot in specific_pilot['pilot']:
        if pilot['Pilot_Id'] == pilot_id:
            print(f"\nИнформация о пилоте с ID {pilot_id}:")
            print(f"Name: {pilot['Name']}, Age: {pilot['Age']}")
else:
    print(f"\nПилот с ID {pilot_id} не найден.")

# Обновление информации о пилоте
pilot_id_to_update = 3  # ID пилота, информацию о котором мы хотим обновить
new_age = random.randint(20, 60)    # Новый возраст для пилота

# Находим пилота по его ID и обновляем информацию о возрасте
update_result = collection.update_one({"pilot.Pilot_Id": pilot_id_to_update}, {"$set": {"pilot.$.Age": new_age}})

# Проверяем, было ли успешно обновление
if update_result.modified_count > 0:
    print(f"\nИнформация о пилоте с ID {pilot_id_to_update} успешно обновлена.")
else:
    print(f"\nИнформация о пилоте с ID {pilot_id_to_update} не была обновлена. Возможно, пилот с таким ID не найден или уже был обновлен.")

# Вывод обновленной информации о пилоте
updated_pilot = collection.find_one({"pilot.Pilot_Id": pilot_id_to_update})
if updated_pilot:
    for pilot in updated_pilot['pilot']:
        if pilot['Pilot_Id'] == pilot_id_to_update:
            print(f"\nИнформация о пилоте после обновления:")
            print(f"Pilot ID: {pilot['Pilot_Id']}, Name: {pilot['Name']}, New Age: {pilot['Age']}")
else:
    print(f"\nПилот с ID {pilot_id_to_update} не найден.")



# Добавление нового пилота
new_pilot = {
    "Pilot_Id": 13,
    "Name": "John Doe",
    "Age": 35
}

# Попытка добавления пилота
insert_result = collection.update_one({}, {"$push": {"pilot": new_pilot}})

# Проверяем, было ли успешно добавление
if insert_result.modified_count > 0:
    print("\nНовый пилот успешно добавлен.")
else:
    print("\nНе удалось добавить нового пилота.")

# Вывод обновленного списка пилотов после добавления
updated_pilots_list = collection.find_one({})['pilot']
print("\nОбновленный список пилотов:")
for pilot in updated_pilots_list:
    print(f"Name: {pilot['Name']}, Age: {pilot['Age']}")


# Удаление определенного пилота по его ID
pilot_id_to_delete = 13  # ID пилота, которого мы хотим удалить

# Попытка удаления пилота
delete_result = collection.update_one({}, {"$pull": {"pilot": {"Pilot_Id": pilot_id_to_delete}}})

# Проверяем, было ли успешно удаление
if delete_result.modified_count > 0:
    print(f"\nПилот с ID {pilot_id_to_delete} успешно удален.")
else:
    print(f"\nПилот с ID {pilot_id_to_delete} не был найден или уже удален.")

# Вывод обновленного списка пилотов после удаления
updated_pilots_list = collection.find_one({})['pilot']
print("\nОбновленный список пилотов:")
for pilot in updated_pilots_list:
    print(f"Name: {pilot['Name']}, Age: {pilot['Age']}")

# Запрос с агрегированием для подсчета общего количества пилотов
aggregation_query = [
    {"$unwind": "$pilot"},  # Развернуть массив pilot в отдельные документы
    {"$group": {"_id": None, "Total_Pilots": {"$sum": 1}}}  # Подсчитать общее количество пилотов
]
print("\n")
# Выполнение запроса
aggregation_result = collection.aggregate(aggregation_query)

# Вывод результатов агрегирования
for result in aggregation_result:
    print(f"Общее количество пилотов: {result['Total_Pilots']}")

print("\n")
# Запрос с агрегированием для получения списка стран, в которых проходили матчи
aggregation_query = [
    {"$match": {"match.Country": {"$ne": None}}}, 
    {"$group": {"_id": "$match.Country"}} 
]
aggregation_result = collection.aggregate(aggregation_query)
unique_countries = [result['_id'] for result in aggregation_result]
print("Список стран, в которых проходили матчи:")
for country in unique_countries:
    print(country)
print("\n")
# Map Function
map_function = """
function () {
    this.pilot.forEach(function(pilot) {
        emit("average_age", {age: pilot.Age, count: 1});
    });
}
"""

# Reduce Function
reduce_function = """
function (key, values) {
    var total_age = 0;
    var total_count = 0;
    values.forEach(function(value) {
        total_age += value.age;
        total_count += value.count;
    });
    return {age_sum: total_age, count: total_count};
}
"""

# Финальная функция
finalize_function = """
function (key, reducedValue) {
    return reducedValue.age_sum / reducedValue.count;
}
"""

# Выполнение операции Map-Reduce
result = db.command({
    "mapReduce": "test",
    "map": map_function,
    "reduce": reduce_function,
    "out": "average_age_result",
    "finalize": finalize_function
})

# Получение результата
for doc in db.average_age_result.find():
    print("Средний возраст пилотов:", doc['value'])
print("\n Количесво пилотов по их возрастам")
# Map Function
map_function = """
function () {
    this.pilot.forEach(function(pilot) {
        emit(pilot.Age, 1);
    });
}
"""

# Reduce Function
reduce_function = """
function (key, values) {
    var total = 0;
    values.forEach(function(value) {
        total += value;
    });
    return total;
}
"""

# Выполнение операции Map-Reduce
result = db.command({
    "mapReduce": "test",
    "map": map_function,
    "reduce": reduce_function,
    "out": "pilots_count_by_age"
})

# Получение результата
pilots_count = {}
for doc in db.pilots_count_by_age.find():
    pilots_count[doc['_id']] = doc['value']

# Вывод результата
for age, count in sorted(pilots_count.items()):
    print(f"Возраст: {age}, Количество пилотов: {count}")
# Закрываем соединение с MongoDB
client.close()
