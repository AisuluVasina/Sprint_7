import allure
import pytest
from api_client import ApiClient
from test_data import MSG_ACCOUNT_NOT_FOUND, MSG_MISSING_DATA_LOGIN

class TestLoginCourier:

    @allure.title("Успешная авторизация курьера")
    @allure.description("Проверка, что курьер может авторизоваться: код 200 и в ответе есть ID")
    def test_login_courier_success(self, unique_courier):
        login = unique_courier["login"]
        password = unique_courier["password"]

        response = ApiClient.login_courier(login, password)
        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title("Ошибка при неверном пароле")
    @allure.description("Проверка, что при неверном пароле возвращается ошибка: код 404 и сообщение")
    def test_login_courier_wrong_password(self, unique_courier):
        login = unique_courier["login"]
        wrong_password = "wrong_password"

        response = ApiClient.login_courier(login, wrong_password)
        assert response.status_code == 404
        assert response.json()["message"] == MSG_ACCOUNT_NOT_FOUND

    @allure.title("Ошибка при отсутствии обязательных полей")
    @allure.description("Проверка, что при отсутствии одного из обязательных полей возвращается ошибка: код 400 и сообщение")
    @pytest.mark.parametrize("payload", [
        {"login": "test"},
        {"password": "test"},
        {}
    ])
    def test_login_courier_missing_field(self, payload):
        response = ApiClient.login_courier(payload.get("login", ""), payload.get("password", ""))
        assert response.status_code == 400
        assert response.json()["message"] == MSG_MISSING_DATA_LOGIN