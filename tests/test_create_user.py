import allure
from helpers.api_client import StellarBurgersAPI
from helpers.api_data import (
    HTTP_OK,
    HTTP_FORBIDDEN,
    ERROR_USER_ALREADY_EXISTS,
    ERROR_REQUIRED_FIELDS,
    KEY_SUCCESS,
    KEY_ACCESS_TOKEN,
    KEY_REFRESH_TOKEN,
    KEY_USER,
    KEY_EMAIL,
    KEY_NAME,
    KEY_MESSAGE,
)


@allure.feature("Создание пользователя")
class TestCreateUser:
    @allure.story("Успешное создание пользователя")
    @allure.title("Тест успешного создания уникального пользователя")
    def test_create_unique_user_success(self, user_credentials, user_cleanup_list):
        """Проверка успешного создания уникального пользователя"""
        api_client = StellarBurgersAPI()

        # Регистрируем пользователя для автоматического удаления после теста
        user_cleanup_list.append(user_credentials)

        response = api_client.create_user(
            email=user_credentials["email"],
            password=user_credentials["password"],
            name=user_credentials["name"],
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
        assert user_data.get(KEY_EMAIL) == user_credentials["email"]
        assert user_data.get(KEY_NAME) == user_credentials["name"]

    @allure.story("Создание дубликата пользователя")
    @allure.title("Тест создания уже зарегистрированного пользователя")
    def test_create_duplicate_user_error(self, created_user):
        """Проверка невозможности создания пользователя, который уже зарегистрирован"""
        api_client = StellarBurgersAPI()

        # Пытаемся создать второго пользователя с теми же данными
        response = api_client.create_user(
            email=created_user["email"],
            password=created_user["password"],
            name=created_user["name"],
        )

        # Проверяем код ответа
        assert (
            response.status_code == HTTP_FORBIDDEN
        ), f"Ожидался код {HTTP_FORBIDDEN}, получен {response.status_code}"

        # Проверяем тело ответа
        response_data = response.json()
        assert (
            response_data.get(KEY_SUCCESS) is False
        ), f"Поле {KEY_SUCCESS} должно быть False"
        assert (
            response_data.get(KEY_MESSAGE) == ERROR_USER_ALREADY_EXISTS
        ), f"Ожидалось сообщение '{ERROR_USER_ALREADY_EXISTS}', получено {response_data.get(KEY_MESSAGE)}"

    @allure.story("Создание пользователя без обязательных полей")
    @allure.title("Тест создания пользователя без email")
    def test_create_user_without_email(self, user_credentials):
        """Проверка невозможности создания пользователя без email"""
        api_client = StellarBurgersAPI()

        response = api_client.create_user(
            email=None,
            password=user_credentials["password"],
            name=user_credentials["name"],
        )

        # Проверяем код ответа
        assert (
            response.status_code == HTTP_FORBIDDEN
        ), f"Ожидался код {HTTP_FORBIDDEN}, получен {response.status_code}"

        # Проверяем тело ответа
        response_data = response.json()
        assert (
            response_data.get(KEY_SUCCESS) is False
        ), f"Поле {KEY_SUCCESS} должно быть False"
        assert (
            response_data.get(KEY_MESSAGE) == ERROR_REQUIRED_FIELDS
        ), f"Ожидалось сообщение '{ERROR_REQUIRED_FIELDS}', получено {response_data.get(KEY_MESSAGE)}"

    @allure.story("Создание пользователя без обязательных полей")
    @allure.title("Тест создания пользователя без password")
    def test_create_user_without_password(self, user_credentials):
        """Проверка невозможности создания пользователя без password"""
        api_client = StellarBurgersAPI()

        response = api_client.create_user(
            email=user_credentials["email"],
            password=None,
            name=user_credentials["name"],
        )

        # Проверяем код ответа
        assert (
            response.status_code == HTTP_FORBIDDEN
        ), f"Ожидался код {HTTP_FORBIDDEN}, получен {response.status_code}"

        # Проверяем тело ответа
        response_data = response.json()
        assert (
            response_data.get(KEY_SUCCESS) is False
        ), f"Поле {KEY_SUCCESS} должно быть False"
        assert (
            response_data.get(KEY_MESSAGE) == ERROR_REQUIRED_FIELDS
        ), f"Ожидалось сообщение '{ERROR_REQUIRED_FIELDS}', получено {response_data.get(KEY_MESSAGE)}"

    @allure.story("Создание пользователя без обязательных полей")
    @allure.title("Тест создания пользователя без name")
    def test_create_user_without_name(self, user_credentials):
        """Проверка невозможности создания пользователя без name"""
        api_client = StellarBurgersAPI()

        response = api_client.create_user(
            email=user_credentials["email"],
            password=user_credentials["password"],
            name=None,
        )

        # Проверяем код ответа
        assert (
            response.status_code == HTTP_FORBIDDEN
        ), f"Ожидался код {HTTP_FORBIDDEN}, получен {response.status_code}"

        # Проверяем тело ответа
        response_data = response.json()
        assert (
            response_data.get(KEY_SUCCESS) is False
        ), f"Поле {KEY_SUCCESS} должно быть False"
        assert (
            response_data.get(KEY_MESSAGE) == ERROR_REQUIRED_FIELDS
        ), f"Ожидалось сообщение '{ERROR_REQUIRED_FIELDS}', получено {response_data.get(KEY_MESSAGE)}"
