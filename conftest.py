import pytest
import random
import string
from api_client import ApiClient

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

@pytest.fixture
def unique_courier():
    #Создает курьера перед тестом, удаляет после.
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    
    # Создаем
    response = ApiClient.create_courier(login, password, first_name)
    assert response.status_code == 201
    
    courier_data = {"login": login, "password": password, "first_name": first_name}
    yield courier_data
    
    # Удаляем (если нужно, иногда тесты сами проверяют удаление, но для чистоты можно удалить)
    # Примечание: если тест проверяет удаление, эту строку нужно убрать или сделать условной
    login_resp = ApiClient.login_courier(login, password)
    if login_resp.status_code == 200:
        courier_id = login_resp.json().get("id")
        ApiClient.delete_courier(courier_id)

@pytest.fixture
def created_order():
    """Создает заказ перед тестом."""
    payload = {
        "firstName": "Иван",
        "lastName": "Иванов",
        "address": "Москва, Мира 62",
        "metroStation": 4,
        "phone": "+79990000000",
        "rentTime": 1,
        "deliveryDate": "2026-09-25",
        "comment": "Test comment"
    }
    response = ApiClient.create_order(payload)
    assert response.status_code == 201
    track = response.json().get("track")
    yield track
    # Очистка заказа не предусмотрена API явно, оставляем как есть или игнорируем в рамках спринта