import requests
import allure
from helpers.urls import (
    USER_REGISTER_URL,
    USER_LOGIN_URL,
    USER_DELETE_URL,
    INGREDIENTS_URL,
    ORDERS_URL,
)


class StellarBurgersAPI:
    """Класс для работы с API Stellar Burgers"""

    @allure.step("Создание пользователя с email {email}")
    def create_user(self, email=None, password=None, name=None):
        """Создать пользователя"""
        url = USER_REGISTER_URL
        payload = {}

        if email is not None:
            payload["email"] = email
        if password is not None:
            payload["password"] = password
        if name is not None:
            payload["name"] = name

        response = requests.post(url, json=payload)
        return response

    @allure.step("Логин пользователя с email {email}")
    def login_user(self, email=None, password=None):
        """Авторизовать пользователя"""
        url = USER_LOGIN_URL
        payload = {}

        if email is not None:
            payload["email"] = email
        if password is not None:
            payload["password"] = password

        response = requests.post(url, json=payload)
        return response

    @allure.step("Удаление пользователя")
    def delete_user(self, access_token):
        """Удалить пользователя (требуется токен авторизации)"""
        url = USER_DELETE_URL
        headers = {"Authorization": access_token}
        response = requests.delete(url, headers=headers)
        return response

    @allure.step("Получение списка ингредиентов")
    def get_ingredients(self):
        """Получить список доступных ингредиентов"""
        url = INGREDIENTS_URL
        response = requests.get(url)
        return response

    @allure.step("Создание заказа")
    def create_order(self, ingredients=None, access_token=None):
        """Создать заказ"""
        url = ORDERS_URL
        payload = {}

        if ingredients is not None:
            payload["ingredients"] = ingredients

        headers = {}
        if access_token is not None:
            headers["Authorization"] = access_token

        response = requests.post(url, json=payload, headers=headers)
        return response
