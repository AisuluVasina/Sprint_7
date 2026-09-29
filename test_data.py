import random
import string

def generate_random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def generate_unique_courier_data():
    rand_str = ''.join(random.choices(string.ascii_lowercase, k=8))
    return {
        "login": f"test_login_{rand_str}",
        "password": f"test_pass_{rand_str}",
        "first_name": f"Test Name {rand_str}"
    }

# Сообщения об ошибках
MSG_DUPLICATE_LOGIN = "Этот логин уже используется"
MSG_MISSING_DATA_CREATE = "Недостаточно данных для создания учетной записи"
MSG_MISSING_DATA_ACCEPT = "Недостаточно данных для поиска"
MSG_MISSING_DATA_LOGIN = "Недостаточно данных для входа"
MSG_COURIER_NOT_FOUND = "Курьера с таким id нет"
MSG_COURIER_DELETE = "Недостаточно данных для удаления курьера"
MSG_ACCOUNT_NOT_FOUND = "Учетная запись не найдена"