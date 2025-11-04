## Задание : API-тесты

Автотесты для API Stellar Burgers (https://stellarburgers.education-services.ru/)

### Установка

1. Клонировать репозиторий
2. Создать виртуальное окружение:
```bash
python3 -m venv venv
source venv/bin/activate  # для macOS/Linux
```

3. Установить зависимости:
```bash
pip3 install -r requirements.txt
```

### Запуск тестов

Запуск всех тестов:
```bash
pytest tests/
```

Запуск с генерацией Allure отчета:
```bash
pytest tests/ --alluredir=allure-results
allure generate allure-results -o allure-report --clean
allure open allure-report
```

### Структура проекта

```
Diplom_2/
├── helpers/          # Вспомогательные модули
│   ├── api_client.py    # API клиент для Stellar Burgers
│   └── data_generator.py # Генераторы тестовых данных
├── tests/           # Тесты
│   ├── test_create_user.py  # Тесты создания пользователя
│   ├── test_login_user.py   # Тесты логина
│   └── test_create_order.py # Тесты создания заказа
├── conftest.py      # Фикстуры pytest
└── requirements.txt # Зависимости
```
