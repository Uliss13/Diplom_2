import allure
import data
from api_client import register_user, login_user

@allure.feature("Пользователи")
@allure.story("Логин пользователя")
class TestLoginUser:

    @allure.title("Успешный вход под существующим пользователем")
    def test_login_success(self, user_payload):
        with allure.step("Регистрация пользователя"):
            register_user(user_payload)
            
        with allure.step("Отправка запроса на логин"):
            response = login_user(user_payload)
            
        with allure.step("Проверка ответа"):
            assert response.status_code == data.USER_LOGIN_SUCCESS_STATUS
            assert response.json()["success"] is True
            assert "accessToken" in response.json()

    @allure.title("Ошибка при входе с неверным логином и паролем")
    def test_login_invalid_credentials(self):
        with allure.step("Формирование неверных данных"):
            payload = {"email": "wrong@yandex.ru", "password": "wrong_pass"}
            
        with allure.step("Отправка запроса"):
            response = login_user(payload)
            
        with allure.step("Проверка ответа"):
            assert response.status_code == data.USER_LOGIN_FAIL_STATUS
            assert response.json()["message"] == data.USER_LOGIN_FAIL_MSG