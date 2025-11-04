"""Константы для работы с API: коды ответов, сообщения, структуры данных"""

# HTTP коды ответов
HTTP_OK = 200
HTTP_FORBIDDEN = 403
HTTP_UNAUTHORIZED = 401
HTTP_BAD_REQUEST = 400
HTTP_INTERNAL_ERROR = 500

# Сообщения об ошибках при создании пользователя
ERROR_USER_ALREADY_EXISTS = "User already exists"
ERROR_REQUIRED_FIELDS = "Email, password and name are required fields"

# Сообщения об ошибках при логине
ERROR_INCORRECT_CREDENTIALS = "email or password are incorrect"

# Сообщения об ошибках при создании заказа
ERROR_INGREDIENTS_REQUIRED = "Ingredient ids must be provided"

# Ключи в ответах API
KEY_SUCCESS = "success"
KEY_ACCESS_TOKEN = "accessToken"
KEY_REFRESH_TOKEN = "refreshToken"
KEY_USER = "user"
KEY_EMAIL = "email"
KEY_NAME = "name"
KEY_MESSAGE = "message"
KEY_ORDER = "order"
KEY_NUMBER = "number"
KEY_DATA = "data"
