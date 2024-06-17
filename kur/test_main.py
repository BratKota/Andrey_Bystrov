import requests

def login(username, password):
    url = 'http://127.0.0.1:5000/login'
    data = {'username': username, 'password': password}
    return requests.post(url, data=data, allow_redirects=False)

def select_film(film_id):
    url = 'http://127.0.0.1:5000/reviews'
    data = {'film_id': film_id}
    return requests.post(url, data=data)

def test_login_success(start_server):
    response_success = login('Andrey', '1234')
    assert response_success.status_code == 302
    assert response_success.headers['Location'] == '/index'
    print("Успех: Вход прошел успешно с правильными данными")

def test_login_fail(start_server):
    response_fail = login('Andrey123', '1234')
    assert response_fail.headers.get('Location') is None
    print("Успех: Ошибка при заходе на страницу с неверными данными")

def test_select_titanic_movie(start_server):
    response_titanic = select_film('2213')
    assert response_titanic.status_code == 200
    assert '<title>Отзывы о фильме Титаник</title>' in response_titanic.text
    print("Успех: Выбор фильма 'Титаник' обработан корректно")

def test_select_invalid_movie(start_server):
    response_invalid = select_film('999999999999999999999999999999999999999')
    assert 'Фильм не найден' in response_invalid.text
    print("Успех: Обработка неверного film_id выполнена корректно")

def test_not_found_url(start_server):
    url = 'http://127.0.0.1:5000/nosrt'
    response = requests.get(url)
    assert response.status_code == 404
    assert response.json() == {
        "message": "Запрошенный URL-адрес не был найден на сервере.",
        "status": "error"
    }
    print("Успех: Обработка несуществующего URL выполнена корректно")
