import allure
from helpers.api_client import StellarBurgersAPI
from helpers.api_data import (
    HTTP_OK,
    HTTP_UNAUTHORIZED,
    ERROR_INCORRECT_CREDENTIALS,
    KEY_SUCCESS,
    KEY_ACCESS_TOKEN,
    KEY_REFRESH_TOKEN,
    KEY_USER,
    KEY_EMAIL,
    KEY_NAME,
    KEY_MESSAGE,
)


@allure.feature("Логин пользователя")
class TestLoginUser:
    @allure.story("Успешный логин")
    @allure.title("Тест успешного входа под существующим пользователем")
    def test_login_existing_user_success(self, created_user):
        """Проверка успешного входа под существующим пользователем"""
        api_client = StellarBurgersAPI()

        response = api_client.login_user(
            email=created_user["email"],
            password=created_user["password"],
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
        assert (
            KEY_ACCESS_TOKEN in response_data
        ), f"В ответе должен быть {KEY_ACCESS_TOKEN}"
        assert (
            KEY_REFRESH_TOKEN in response_data
        ), f"В ответе должен быть {KEY_REFRESH_TOKEN}"
        assert KEY_USER in response_data, f"В ответе должен быть объект {KEY_USER}"

        # Проверяем данные пользователя
        user_data = response_data[KEY_USER]
        assert user_data.get(KEY_EMAIL) == created_user["email"]
        assert user_data.get(KEY_NAME) == created_user["name"]

    @allure.story("Логин с неверными данными")
    @allure.title("Тест входа с неверным email")
    def test_login_with_invalid_email(self, created_user):
        """Проверка невозможности входа с неверным email"""
        api_client = StellarBurgersAPI()

        response = api_client.login_user(
            email="invalid_email@test.com",
            password=created_user["password"],
        )

        # Проверяем код ответа
        assert (
            response.status_code == HTTP_UNAUTHORIZED
        ), f"Ожидался код {HTTP_UNAUTHORIZED}, получен {response.status_code}"

        # Проверяем тело ответа
        response_data = response.json()
        assert (
            response_data.get(KEY_SUCCESS) is False
        ), f"Поле {KEY_SUCCESS} должно быть False"
        assert (
            response_data.get(KEY_MESSAGE) == ERROR_INCORRECT_CREDENTIALS
        ), f"Ожидалось сообщение '{ERROR_INCORRECT_CREDENTIALS}', получено {response_data.get(KEY_MESSAGE)}"

    @allure.story("Логин с неверными данными")
    @allure.title("Тест входа с неверным паролем")
    def test_login_with_invalid_password(self, created_user):
        """Проверка невозможности входа с неверным паролем"""
        api_client = StellarBurgersAPI()

        response = api_client.login_user(
            email=created_user["email"],
            password="invalid_password123",
        )

        # Проверяем код ответа
        assert (
            response.status_code == HTTP_UNAUTHORIZED
        ), f"Ожидался код {HTTP_UNAUTHORIZED}, получен {response.status_code}"

        # Проверяем тело ответа
        response_data = response.json()
        assert (
            response_data.get(KEY_SUCCESS) is False
        ), f"Поле {KEY_SUCCESS} должно быть False"
        assert (
            response_data.get(KEY_MESSAGE) == ERROR_INCORRECT_CREDENTIALS
        ), f"Ожидалось сообщение '{ERROR_INCORRECT_CREDENTIALS}', получено {response_data.get(KEY_MESSAGE)}"

    @allure.story("Логин с неверными данными")
    @allure.title("Тест входа с неверным email и паролем")
    def test_login_with_invalid_credentials(self, user_credentials):
        """Проверка невозможности входа с полностью неверными данными"""
        api_client = StellarBurgersAPI()

        response = api_client.login_user(
            email=user_credentials["email"],
            password=user_credentials["password"],
        )

        # Проверяем код ответа
        assert (
            response.status_code == HTTP_UNAUTHORIZED
        ), f"Ожидался код {HTTP_UNAUTHORIZED}, получен {response.status_code}"

        # Проверяем тело ответа
        response_data = response.json()
        assert (
            response_data.get(KEY_SUCCESS) is False
        ), f"Поле {KEY_SUCCESS} должно быть False"
        assert (
            response_data.get(KEY_MESSAGE) == ERROR_INCORRECT_CREDENTIALS
        ), f"Ожидалось сообщение '{ERROR_INCORRECT_CREDENTIALS}', получено {response_data.get(KEY_MESSAGE)}"
