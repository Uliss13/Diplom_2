import pytest
import allure
from api_client import register_user, get_ingredients, delete_user
from helpers import generate_user_payload

@pytest.fixture
def user_payload():
    return generate_user_payload()

@pytest.fixture
def created_user(user_payload):
    with allure.step("Подготовка: создание пользователя"):
        response = register_user(user_payload)
        assert response.status_code == 200, f"Не удалось создать пользователя: {response.text}"
        token = response.json().get("accessToken")

    yield {"payload": user_payload, "token": token}
    
    with allure.step("Очистка: удаление пользователя"):
        if token:
            delete_user(token)

@pytest.fixture
def valid_ingredients():
    with allure.step("Подготовка: получение валидных ID ингредиентов"):
        response = get_ingredients()
        assert response.status_code == 200, "Не удалось получить ингредиенты"
        data = response.json()["data"]
        # Берем первые два ингредиента для теста
        return [data[0]["_id"], data[1]["_id"]]