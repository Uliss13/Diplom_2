import allure
import requests
from urls import REGISTER_URL, LOGIN_URL, ORDERS_URL, INGREDIENTS_URL, USER_URL

@allure.step("Создание пользователя")
def register_user(payload):
    return requests.post(REGISTER_URL, json=payload)

@allure.step("Авторизация пользователя")
def login_user(payload):
    return requests.post(LOGIN_URL, json=payload)

@allure.step("Получение списка ингредиентов")
def get_ingredients():
    return requests.get(INGREDIENTS_URL)

@allure.step("Создание заказа")
def create_order(payload, token=None):
    headers = {}
    if token:
        headers["Authorization"] = token
    return requests.post(ORDERS_URL, json=payload, headers=headers)

@allure.step("Удаление пользователя")
def delete_user(token):
    return requests.delete(USER_URL, headers={"Authorization": token})