import allure
import pytest
import random
import string
import requests
from api_client import ApiClient

class TestCreateCourier:

    @staticmethod
    def generate_unique_data():
        # Генерируем случайную строку из 8 букв
        rand_str = ''.join(random.choices(string.ascii_lowercase, k=8))
        return {
            "login": f"test_login_{rand_str}",
            "password": f"test_pass_{rand_str}",
            "first_name": f"Test Name {rand_str}"
        }

    @allure.title("Успешное создание курьера")
    @allure.description("Проверка, что курьера можно создать: код 201 и ответ {\"ok\": true}")
    def test_create_courier_success(self):
        data = self.generate_unique_data()
        
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
        data = self.generate_unique_data()

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
        assert response_duplicate.json()["message"] == "Этот логин уже используется"

    @allure.title("Ошибка при отсутствии поля login")
    @allure.description("Проверка, что при отсутствии login возвращается 400")
    def test_create_courier_missing_login(self):
        # Берём гарантированно уникальный логин через генератор
        data = self.generate_unique_data()
        
        payload = {
            "password": data["password"],
            "firstName": data["first_name"]
            # login НЕ добавляем
        }
        
        response = requests.post(
            "https://qa-scooter.praktikum-services.ru/api/v1/courier", 
            json=payload
        )
        
        assert response.status_code == 400
        assert response.json() == {"code": 400,
                                   "message": "Недостаточно данных для создания учетной записи"}

    @allure.title("Ошибка при отсутствии поля password")
    @allure.description("Проверка, что при отсутствии password возвращается 400")
    def test_create_courier_missing_password(self):
        # Берём гарантированно уникальный логин через генератор
        data = self.generate_unique_data()
        
        payload = {
            "login": data["login"],
            "firstName": data["first_name"]
            # password НЕ добавляем
        }
        
        response = requests.post(
            "https://qa-scooter.praktikum-services.ru/api/v1/courier", 
            json=payload
        )
        
        assert response.status_code == 400
        assert response.json() == {"code": 400,
                                   "message": "Недостаточно данных для создания учетной записи"}
