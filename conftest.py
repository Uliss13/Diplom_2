import pytest
import allure
from api_client import register_user, login_user, delete_user, get_ingredients
from helpers import generate_user_payload

@pytest.fixture
def registered_user():
    payload = generate_user_payload()
    
    with allure.step("Подготовка: создание пользователя"):
        response = register_user(payload)
        token = response.json().get("accessToken")

    yield {"payload": payload, "token": token}
    
    with allure.step("Очистка: удаление пользователя"):
        if token:
            delete_user(token)

@pytest.fixture
def cleanup_user():
    created_users = []
    
    def _add(login_data):
        created_users.append(login_data)
        
    yield _add
    
    with allure.step("Очистка: удаление созданных пользователей"):
        for user_data in created_users:
            login_resp = login_user(user_data)
            if login_resp.status_code == 200:
                token = login_resp.json().get("accessToken")
                if token:
                    delete_user(token)

@pytest.fixture
def valid_ingredients():
    with allure.step("Подготовка: получение валидных ID ингредиентов"):
        response = get_ingredients()
        data = response.json()["data"]
        return [data[0]["_id"], data[1]["_id"]]