import pytest
import random
import string
from api_client import ApiClient
from test_data import generate_random_string, generate_unique_courier_data

@pytest.fixture
def unique_courier():
    data = generate_unique_courier_data()
    login, password, first_name = data["login"], data["password"], data["first_name"]
    
    # Создаем
    response = ApiClient.create_courier(login, password, first_name)
    assert response.status_code == 201
    
    courier_data = {"login": login, "password": password, "first_name": first_name}
    yield courier_data
    
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
