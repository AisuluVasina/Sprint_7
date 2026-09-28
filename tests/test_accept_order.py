import allure
import pytest
from api_client import ApiClient

class TestAcceptOrder:

    @allure.title("Успешное принятие заказа")
    @allure.description("Проверка, что заказ можно принять: код 200 и ответ {\"ok\": true}")
    def test_accept_order_success(self, unique_courier, created_order):
        login = unique_courier["login"]
        password = unique_courier["password"]
        track = created_order

        # Получаем ID курьера
        login_resp = ApiClient.login_courier(login, password)
        assert login_resp.status_code == 200
        courier_id = login_resp.json().get("id")

        # Принимаем заказ
        response = ApiClient.accept_order(track, courier_id)
        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.title("Ошибка при отсутствии ID курьера или заказа")
    @allure.description("Проверка, что при отсутствии ID курьера или заказа возвращается ошибка: код 400 и сообщение")
    @pytest.mark.parametrize("courier_id, order_id", [
        (None, 123),
        (123, None),
        (None, None)
    ])
    def test_accept_order_missing_params(self, courier_id, order_id):
        if courier_id is None or order_id is None:
            # Если один из параметров None, API может вернуть 400 или 500 в зависимости от реализации
            # В данном случае ожидаем 400, но если API возвращает 500, нужно уточнить требования
            response = ApiClient.accept_order(order_id or 0, courier_id or 0)
            assert response.status_code == 400
            assert response.json()["message"] == "Недостаточно данных для поиска"
        else:
            response = ApiClient.accept_order(order_id, courier_id)
            assert response.status_code == 400
            assert response.json()["message"] == "Недостаточно данных для поиска"