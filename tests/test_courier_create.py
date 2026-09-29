import allure
import pytest
from api_client import ApiClient
from test_data import generate_unique_courier_data, MSG_DUPLICATE_LOGIN, MSG_MISSING_DATA_CREATE

class TestCreateCourier:

    @allure.title("Успешное создание курьера")
    @allure.description("Проверка, что курьера можно создать: код 201 и ответ {\"ok\": true}")
    def test_create_courier_success(self):
        data = generate_unique_courier_data()
        
        response = ApiClient.create_courier(
            data["login"], 
            data["password"], 
            data["first_name"]
        )
        assert response.status_code == 201
        assert response.json() == {"ok": True}

    @allure.title("Ошибка при создании курьера с дублирующимся логином")
    @allure.description("Проверка, что нельзя создать курьера с уже существующим логином: код 409 и сообщение об ошибке")
    def test_create_courier_duplicate_login(self):
        data = generate_unique_courier_data()

        # 1. Создаём курьера (должно быть 201)
        response = ApiClient.create_courier(
            data["login"], 
            data["password"], 
            data["first_name"]
        )
        assert response.status_code == 201

        # 2. Пробуем создать повторно с тем же логином (должно быть 409)
        response_duplicate = ApiClient.create_courier(
            data["login"], 
            data["password"], 
            data["first_name"]
        )
        assert response_duplicate.status_code == 409
        assert response_duplicate.json()["message"] == MSG_DUPLICATE_LOGIN

    @allure.title("Ошибка при отсутствии поля login")
    @allure.description("Проверка, что при отсутствии login возвращается 400")
    def test_create_courier_missing_login(self):
        # Берём гарантированно уникальный логин через генератор
        data = generate_unique_courier_data()
        
        payload = {
            "password": data["password"],
            "firstName": data["first_name"]
            # login НЕ добавляем
        }

        response = ApiClient.create_order(payload)  
        # Исправление:
        response = ApiClient.create_courier(
            login="",
            password=data["password"],
            first_name=data["first_name"]
        )
        
        assert response.status_code == 400
        assert response.json()["message"] == MSG_MISSING_DATA_CREATE

    @allure.title("Ошибка при отсутствии поля password")
    @allure.description("Проверка, что при отсутствии password возвращается 400")
    def test_create_courier_missing_password(self):
        # Берём гарантированно уникальный логин через генератор
        data = generate_unique_courier_data()
        
        payload = {
            "login": data["login"],
            "firstName": data["first_name"]
            # password НЕ добавляем
        }

        response = ApiClient.create_courier(
            login=data["login"],
            password="",
            first_name=data["first_name"]
        )
        
        assert response.status_code == 400
        assert response.json()["message"] == MSG_MISSING_DATA_CREATE
