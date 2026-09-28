import allure
import pytest
from api_client import ApiClient

class TestCreateOrder:

    @allure.title("Создание заказа с разными вариантами цветов")
    @allure.description("Проверка создания заказа: код 201 и наличие track в ответе; проверка разных вариантов цветов")
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    def test_create_order_with_colors(self, color):
        payload = {
            "firstName": "Иван",
            "lastName": "Иванов",
            "address": "Москва, Мира 62",
            "metroStation": 4,
            "phone": "+79990000000",
            "rentTime": 1,
            "deliveryDate": "2026-09-25",
            "comment": "Test comment",
            "color": color
        }

        response = ApiClient.create_order(payload)
        assert response.status_code == 201
        assert "track" in response.json()