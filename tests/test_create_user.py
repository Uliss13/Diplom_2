import pytest
import allure
import data
from api_client import register_user
from helpers import generate_user_payload

@allure.feature("Пользователи")
@allure.story("Создание пользователя")
class TestCreateUser:

    @allure.title("Успешное создание уникального пользователя")
    def test_create_unique_user(self, user_payload):
        with allure.step("Отправка запроса на создание"):
            response = register_user(user_payload)
            
        with allure.step("Проверка ответа"):
            assert response.status_code == data.USER_CREATE_SUCCESS_STATUS
            assert response.json()["success"] is True
            assert "accessToken" in response.json()

    @allure.title("Ошибка при создании уже зарегистрированного пользователя")
    def test_create_duplicate_user(self, user_payload):
        with allure.step("Создание первого пользователя"):
            register_user(user_payload)
            
        with allure.step("Попытка создать дубликат"):
            response = register_user(user_payload)
            
        with allure.step("Проверка ответа"):
            assert response.status_code == data.USER_CREATE_DUPLICATE_STATUS
            assert response.json()["message"] == data.USER_CREATE_DUPLICATE_MSG

    @allure.title("Ошибка при создании без обязательного поля: {missing_field}")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field(self, missing_field):
        with allure.step(f"Формирование payload без поля '{missing_field}'"):
            payload = generate_user_payload()
            payload.pop(missing_field)
            
        with allure.step("Отправка запроса"):
            response = register_user(payload)
            
        with allure.step("Проверка ответа"):
            assert response.status_code == data.USER_CREATE_MISSING_FIELD_STATUS
            assert response.json()["message"] == data.USER_CREATE_MISSING_FIELD_MSG