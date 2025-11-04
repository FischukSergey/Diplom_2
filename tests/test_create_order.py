import allure
from helpers.api_client import StellarBurgersAPI
from helpers.api_data import (
    HTTP_OK,
    HTTP_BAD_REQUEST,
    HTTP_INTERNAL_ERROR,
    ERROR_INGREDIENTS_REQUIRED,
    KEY_SUCCESS,
    KEY_ORDER,
    KEY_NUMBER,
    KEY_MESSAGE,
)


@allure.feature("Создание заказа")
class TestCreateOrder:
    @allure.story("Создание заказа с авторизацией")
    @allure.title("Тест создания заказа с авторизацией и ингредиентами")
    def test_create_order_with_auth_and_ingredients(
        self, created_user, ingredients_list
    ):
        """Проверка успешного создания заказа с авторизацией и ингредиентами"""
        api_client = StellarBurgersAPI()

        # Берем первые 3 ингредиента для заказа
        selected_ingredients = ingredients_list[:3]

        response = api_client.create_order(
            ingredients=selected_ingredients,
            access_token=created_user["access_token"],
        )

        # Проверяем код ответа
        assert (
            response.status_code == HTTP_OK
        ), f"Ожидался код {HTTP_OK}, получен {response.status_code}"

        # Проверяем тело ответа
        response_data = response.json()
        assert (
            response_data.get(KEY_SUCCESS) is True
        ), f"Поле {KEY_SUCCESS} должно быть True"
        assert KEY_ORDER in response_data, f"В ответе должен быть объект {KEY_ORDER}"

        # Проверяем данные заказа
        order_data = response_data[KEY_ORDER]
        assert KEY_NUMBER in order_data, f"В заказе должен быть номер заказа"
        assert isinstance(
            order_data[KEY_NUMBER], int
        ), "Номер заказа должен быть числом"

    @allure.story("Создание заказа без авторизации")
    @allure.title("Тест создания заказа без авторизации, но с ингредиентами")
    def test_create_order_without_auth_and_with_ingredients(self, ingredients_list):
        """Проверка создания заказа без авторизации, но с ингредиентами"""
        api_client = StellarBurgersAPI()

        # Берем первые 3 ингредиента для заказа
        selected_ingredients = ingredients_list[:3]

        response = api_client.create_order(
            ingredients=selected_ingredients,
            access_token=None,
        )

        # Проверяем код ответа
        assert (
            response.status_code == HTTP_OK
        ), f"Ожидался код {HTTP_OK}, получен {response.status_code}"

        # Проверяем тело ответа
        response_data = response.json()
        assert (
            response_data.get(KEY_SUCCESS) is True
        ), f"Поле {KEY_SUCCESS} должно быть True"
        assert KEY_ORDER in response_data, f"В ответе должен быть объект {KEY_ORDER}"

        # Проверяем данные заказа
        order_data = response_data[KEY_ORDER]
        assert KEY_NUMBER in order_data, f"В заказе должен быть номер заказа"

    @allure.story("Создание заказа без ингредиентов")
    @allure.title("Тест создания заказа с авторизацией, но без ингредиентов")
    def test_create_order_with_auth_without_ingredients(self, created_user):
        """Проверка невозможности создания заказа без ингредиентов с авторизацией"""
        api_client = StellarBurgersAPI()

        response = api_client.create_order(
            ingredients=[],
            access_token=created_user["access_token"],
        )

        # Проверяем код ответа
        assert (
            response.status_code == HTTP_BAD_REQUEST
        ), f"Ожидался код {HTTP_BAD_REQUEST}, получен {response.status_code}"

        # Проверяем тело ответа
        response_data = response.json()
        assert (
            response_data.get(KEY_SUCCESS) is False
        ), f"Поле {KEY_SUCCESS} должно быть False"
        assert (
            response_data.get(KEY_MESSAGE) == ERROR_INGREDIENTS_REQUIRED
        ), f"Ожидалось сообщение '{ERROR_INGREDIENTS_REQUIRED}', получено {response_data.get(KEY_MESSAGE)}"

    @allure.story("Создание заказа без ингредиентов")
    @allure.title("Тест создания заказа без авторизации и без ингредиентов")
    def test_create_order_without_auth_without_ingredients(self):
        """Проверка невозможности создания заказа без авторизации и без ингредиентов"""
        api_client = StellarBurgersAPI()

        response = api_client.create_order(
            ingredients=[],
            access_token=None,
        )

        # Проверяем код ответа
        assert (
            response.status_code == HTTP_BAD_REQUEST
        ), f"Ожидался код {HTTP_BAD_REQUEST}, получен {response.status_code}"

        # Проверяем тело ответа
        response_data = response.json()
        assert (
            response_data.get(KEY_SUCCESS) is False
        ), f"Поле {KEY_SUCCESS} должно быть False"
        assert (
            response_data.get(KEY_MESSAGE) == ERROR_INGREDIENTS_REQUIRED
        ), f"Ожидалось сообщение '{ERROR_INGREDIENTS_REQUIRED}', получено {response_data.get(KEY_MESSAGE)}"

    @allure.story("Создание заказа с неверными данными")
    @allure.title("Тест создания заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_ingredients_hash(self, created_user):
        """Проверка обработки запроса с неверным хешем ингредиентов"""
        api_client = StellarBurgersAPI()

        # Используем невалидные хеши ингредиентов
        invalid_ingredients = ["invalid_hash_123", "invalid_hash_456"]

        response = api_client.create_order(
            ingredients=invalid_ingredients,
            access_token=created_user["access_token"],
        )

        # Проверяем код ответа
        assert (
            response.status_code == HTTP_INTERNAL_ERROR
        ), f"Ожидался код {HTTP_INTERNAL_ERROR}, получен {response.status_code}"
