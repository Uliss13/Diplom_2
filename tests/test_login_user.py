import allure
import data
from api_client import login_user

@allure.feature("Пользователи")
@allure.story("Логин пользователя")
class TestLoginUser:

    @allure.title("Успешный вход под существующим пользователем")
    def test_login_success(self, registered_user):
        with allure.step("Отправка запроса на логин"):
            response = login_user(registered_user["payload"])
            
        with allure.step("Проверка ответа"):
            assert response.status_code == data.USER_LOGIN_SUCCESS_STATUS
            assert response.json()["success"] is True
            assert "accessToken" in response.json()

    @allure.title("Ошибка при входе с неверным логином")
    def test_login_wrong_login(self, registered_user):
        with allure.step("Формирование неверного логина"):
            payload = registered_user["payload"].copy()
            payload["email"] = "wrong_login@yandex.ru"
            
        with allure.step("Отправка запроса"):
            response = login_user(payload)
            
        with allure.step("Проверка ответа"):
            assert response.status_code == data.USER_LOGIN_FAIL_STATUS
            assert response.json()["message"] == data.USER_LOGIN_FAIL_MSG

    @allure.title("Ошибка при входе с неверным паролем")
    def test_login_wrong_password(self, registered_user):
        with allure.step("Формирование неверного пароля"):
            payload = registered_user["payload"].copy()
            payload["password"] = "wrong_password"
            
        with allure.step("Отправка запроса"):
            response = login_user(payload)
            
        with allure.step("Проверка ответа"):
            assert response.status_code == data.USER_LOGIN_FAIL_STATUS
            assert response.json()["message"] == data.USER_LOGIN_FAIL_MSG