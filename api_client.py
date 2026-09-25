import requests

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"

class ApiClient:
    @staticmethod
    # Создание курьера
    def create_courier(login, password, first_name):
        payload = {"login": login, "password": password, "firstName": first_name}
        return requests.post(f"{BASE_URL}/courier", json=payload)

    @staticmethod
    # Логин (авторизация) курьера
    def login_courier(login, password):
        payload = {"login": login, "password": password}
        return requests.post(f"{BASE_URL}/courier/login", json=payload)

    @staticmethod
    # Удаление курьера
    def delete_courier(courier_id):
        if not courier_id:
            # Для случая, когда ID не передан, отправляем запрос без ID в пути
            # Но API, скорее всего, ожидает ID в пути, поэтому такой запрос вернёт 404
            return requests.delete(f"{BASE_URL}/courier")
        return requests.delete(f"{BASE_URL}/courier/{courier_id}")

    @staticmethod
    # Cоздание заказа
    def create_order(payload):
        return requests.post(f"{BASE_URL}/orders", json=payload)

    @staticmethod
    # Список заказов
    def get_orders_list(params=None):
        return requests.get(f"{BASE_URL}/orders", params=params)

    @staticmethod
    # Принять заказ
    def accept_order(order_id, courier_id):
        params = {"t": track_number}
        return requests.get(f"{BASE_URL}/orders/track", params=params)

    @staticmethod
    # Получить заказ по его номеру
    def get_order_by_track(track_number):
        return requests.get(f"{BASE_URL}/orders/track", params={"t": track_number})

    @staticmethod
    def cancel_order(track_number):
        return requests.put(f"{BASE_URL}/orders/cancel", json={"track": track_number})