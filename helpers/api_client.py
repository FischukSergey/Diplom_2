import requests
import allure
from helpers.urls import (
    BASE_URL,
    USER_REGISTER,
    USER_LOGIN,
    USER_DELETE,
    INGREDIENTS,
    ORDERS,
)


class StellarBurgersAPI:
    """Класс для работы с API Stellar Burgers"""

    def __init__(self):
        self.base_url = BASE_URL

    @allure.step("Создание пользователя с email {email}")
    def create_user(self, email=None, password=None, name=None):
        """Создать пользователя"""
        url = f"{self.base_url}{USER_REGISTER}"
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
        url = f"{self.base_url}{USER_LOGIN}"
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
        url = f"{self.base_url}{USER_DELETE}"
        headers = {"Authorization": access_token}
        response = requests.delete(url, headers=headers)
        return response

    @allure.step("Получение списка ингредиентов")
    def get_ingredients(self):
        """Получить список доступных ингредиентов"""
        url = f"{self.base_url}{INGREDIENTS}"
        response = requests.get(url)
        return response

    @allure.step("Создание заказа")
    def create_order(self, ingredients=None, access_token=None):
        """Создать заказ"""
        url = f"{self.base_url}{ORDERS}"
        payload = {}

        if ingredients is not None:
            payload["ingredients"] = ingredients

        headers = {}
        if access_token is not None:
            headers["Authorization"] = access_token

        response = requests.post(url, json=payload, headers=headers)
        return response
