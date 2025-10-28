import pytest
from helpers.api_client import StellarBurgersAPI
from helpers.data_generator import generate_user_data
from helpers.api_data import HTTP_OK, KEY_ACCESS_TOKEN, KEY_DATA


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
        except Exception:
            # Игнорируем ошибки при cleanup (пользователь может не существовать)
            pass


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

    # Проверяем успешность создания
    assert (
        response.status_code == HTTP_OK
    ), f"Не удалось создать пользователя: {response.text}"

    # Регистрируем пользователя для удаления после теста
    user_cleanup_list.append(user_credentials)

    # Получаем токен из ответа
    response_data = response.json()
    access_token = response_data.get(KEY_ACCESS_TOKEN)

    # Передаём данные пользователя в тест
    yield {
        "email": user_credentials["email"],
        "password": user_credentials["password"],
        "name": user_credentials["name"],
        "access_token": access_token,
    }


@pytest.fixture
def user_with_token(created_user):
    """Фикстура для авторизованного пользователя с токеном"""
    # created_user уже содержит токен и все данные
    return created_user


@pytest.fixture
def ingredients_list():
    """Фикстура для получения списка доступных ингредиентов"""
    api_client = StellarBurgersAPI()
    response = api_client.get_ingredients()

    assert response.status_code == HTTP_OK, "Не удалось получить список ингредиентов"

    ingredients_data = response.json().get(KEY_DATA, [])

    # Возвращаем список ID ингредиентов
    return [ingredient["_id"] for ingredient in ingredients_data]
