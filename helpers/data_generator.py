import random
import string


def generate_random_string(length):
    """Генерирует случайную строку из букв нижнего регистра заданной длины"""
    letters = string.ascii_lowercase
    random_string = "".join(random.choice(letters) for _ in range(length))
    return random_string


def generate_random_email():
    """Генерирует случайный email"""
    username = generate_random_string(10)
    domain = generate_random_string(5)
    return f"{username}@{domain}.com"


def generate_user_data():
    """Генерирует полные данные пользователя"""
    return {
        "email": generate_random_email(),
        "password": generate_random_string(10),
        "name": generate_random_string(8),
    }
