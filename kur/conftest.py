import subprocess
import time
import os
import pytest

@pytest.fixture(scope="module")
def start_server():
    # Устанавливаем переменную окружения для режима тестирования
    os.environ['FLASK_ENV'] = 'testing'
    # Запускаем сервер с помощью subprocess
    process = subprocess.Popen(['python', 'main.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Ждем некоторое время, чтобы сервер успел запуститься
    time.sleep(3)
    print("Успех: Система запустилась")
