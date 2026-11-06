import allure
import data
from api_client import create_order

@allure.feature("Заказы")
@allure.story("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_auth_with_ingredients(self, registered_user, valid_ingredients):
        with allure.step("Формирование payload"):
            payload = {"ingredients": valid_ingredients}
            
        with allure.step("Отправка запроса с токеном"):
            response = create_order(payload, token=registered_user["token"])
            
        with allure.step("Проверка ответа"):
            assert response.status_code == data.ORDER_CREATE_SUCCESS_STATUS
            assert response.json()["success"] is True
            assert "number" in response.json()["order"]

    @allure.title("Создание заказа без авторизации")
    def test_create_order_no_auth(self, valid_ingredients):
        with allure.step("Формирование payload"):
            payload = {"ingredients": valid_ingredients}
            
        with allure.step("Отправка запроса без токена"):
            response = create_order(payload, token=None)
            
        with allure.step("Проверка ответа"):
            assert response.status_code == data.ORDER_CREATE_NO_AUTH_STATUS
            assert response.json()["success"] is True
            assert "order" in response.json()

    @allure.title("Ошибка при создании заказа без ингредиентов")
    def test_create_order_no_ingredients(self, registered_user):
        with allure.step("Формирование payload с пустым списком"):
            payload = {"ingredients": []}
            
        with allure.step("Отправка запроса"):
            response = create_order(payload, token=registered_user["token"])
            
        with allure.step("Проверка ответа"):
            assert response.status_code == data.ORDER_CREATE_NO_INGREDIENTS_STATUS
            assert response.json()["message"] == data.ORDER_CREATE_NO_INGREDIENTS_MSG

    @allure.title("Ошибка при создании заказа с неверным хешем")
    def test_create_order_invalid_hash(self, registered_user):
        with allure.step("Формирование payload с невалидным хешем"):
            payload = {"ingredients": ["invalid_hash_123"]}
            
        with allure.step("Отправка запроса"):
            response = create_order(payload, token=registered_user["token"])
            
        with allure.step("Проверка ответа"):
            assert response.status_code == data.ORDER_CREATE_INVALID_HASH_STATUS