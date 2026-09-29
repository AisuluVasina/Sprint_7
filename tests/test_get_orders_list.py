import allure
from api_client import ApiClient

class TestGetOrdersList:

    @allure.title("Получение списка заказов")
    @allure.description("Проверка, что в теле ответа возвращается список заказов: код 200 и наличие ключа 'orders'")
    def test_get_orders_list(self):
        response = ApiClient.get_orders_list()
        assert response.status_code == 200
        assert "orders" in response.json()