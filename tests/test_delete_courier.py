import allure
import pytest
from api_client import ApiClient
from test_data import MSG_COURIER_DELETE, MSG_COURIER_NOT_FOUND

class TestDeleteCourier:

    @allure.title("Успешное удаление курьера")
    @allure.description("Проверка, что курьера можно удалить: код 200 и ответ {\"ok\": true}")
    def test_delete_courier_success(self, unique_courier):
        login = unique_courier["login"]
        password = unique_courier["password"]

        # Логинимся, чтобы получить ID
        login_resp = ApiClient.login_courier(login, password)
        assert login_resp.status_code == 200
        courier_id = login_resp.json().get("id")

        # Удаляем
        response = ApiClient.delete_courier(courier_id)
        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.title("Ошибка при удалении курьера без ID")
    @allure.description("Проверка, что при отсутствии ID возвращается ошибка: код 400 и сообщение")
    def test_delete_courier_without_id(self):
        response = ApiClient.delete_courier("")
        assert response.status_code == 400
        assert response.json()["message"] == MSG_COURIER_DELETE

    @allure.title("Ошибка при удалении несуществующего курьера")
    @allure.description("Проверка, что при удалении несуществующего курьера возвращается ошибка: код 400 и сообщение")
    def test_delete_courier_nonexistent(self):
        response = ApiClient.delete_courier("999999999")
        assert response.status_code == 404
        assert response.json()["message"] == MSG_COURIER_NOT_FOUND