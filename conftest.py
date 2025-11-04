import logging
import pytest
from helpers.api_client import StellarBurgersAPI
from helpers.data_generator import generate_user_data
from helpers.api_data import HTTP_OK, KEY_ACCESS_TOKEN, KEY_DATA

# Настройка логирования
logger = logging.getLogger(__name__)


@pytest.fixture
def user_credentials():
    """Фикстура для генерации данных пользователя"""
    return generate_user_data()


@pytest.fixture
def user_cleanup_list():
    """Фикстура для автоматического удаления пользователей после теста"""
    users_to_cleanup = []

    # Передаём список в тест - тесты будут добавлять туда данные пользователей
    yield users_to_cleanup

    # После теста удаляем всех пользователей из списка
    api_client = StellarBurgersAPI()
    for user_data in users_to_cleanup:
        try:
            # Логинимся, чтобы получить токен
            login_response = api_client.login_user(
                user_data["email"], user_data["password"]
            )
            if login_response.status_code == HTTP_OK:
                access_token = login_response.json().get(KEY_ACCESS_TOKEN)
                if access_token:
                    api_client.delete_user(access_token)
        except Exception as e:
            # Логируем ошибки при cleanup, но не роняем тест
            logger.warning(
                f"Не удалось удалить пользователя {user_data.get('email')}: {e}"
            )


@pytest.fixture
def created_user(user_credentials, user_cleanup_list):
    """Фикстура для создания пользователя с последующим удалением"""
    api_client = StellarBurgersAPI()

    # Создаём пользователя
    response = api_client.create_user(
        email=user_credentials["email"],
        password=user_credentials["password"],
        name=user_credentials["name"],
    )

    # Проверяем успешность создания (pre-condition)
    if response.status_code != HTTP_OK:
        pytest.fail(
            f"Не удалось создать пользователя в pre-condition. "
            f"Код: {response.status_code}, Ответ: {response.text}"
        )

    # Регистрируем пользователя для удаления после теста
    user_cleanup_list.append(user_credentials)

    # Получаем токен из ответа
    response_data = response.json()
    access_token = response_data.get(KEY_ACCESS_TOKEN)

    if not access_token:
        pytest.fail(f"Не получен accessToken в pre-condition. Ответ: {response_data}")

    # Передаём данные пользователя в тест
    yield {
        "email": user_credentials["email"],
        "password": user_credentials["password"],
        "name": user_credentials["name"],
        "access_token": access_token,
    }


@pytest.fixture
def ingredients_list():
    """Фикстура для получения списка доступных ингредиентов"""
    api_client = StellarBurgersAPI()
    response = api_client.get_ingredients()

    # Проверяем успешность получения ингредиентов (pre-condition)
    if response.status_code != HTTP_OK:
        pytest.fail(
            f"Не удалось получить список ингредиентов в pre-condition. "
            f"Код: {response.status_code}, Ответ: {response.text}"
        )

    ingredients_data = response.json().get(KEY_DATA, [])

    if not ingredients_data:
        pytest.fail("Список ингредиентов пуст в pre-condition")

    # Возвращаем список ID ингредиентов
    return [ingredient["_id"] for ingredient in ingredients_data]
