"""URL-адреса для API Stellar Burgers"""

# Базовый URL API (можно менять для переключения между стендами)
BASE_URL = "https://stellarburgers.education-services.ru"

# Полные URL для работы с пользователями
USER_REGISTER_URL = f"{BASE_URL}/api/auth/register"
USER_LOGIN_URL = f"{BASE_URL}/api/auth/login"
USER_DELETE_URL = f"{BASE_URL}/api/auth/user"

# Полные URL для работы с ингредиентами и заказами
INGREDIENTS_URL = f"{BASE_URL}/api/ingredients"
ORDERS_URL = f"{BASE_URL}/api/orders"
