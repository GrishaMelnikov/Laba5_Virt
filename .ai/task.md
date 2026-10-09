Лабораторная работа №5. Методология CI/CD.

## Что уже есть
- Репозиторий на GitHub.
- FastAPI-приложение (src/main.py, src/routers/user.py).
- requirements.txt.
- Dockerfile.
- Папка tests с __init__.py (тесты не написаны).

## Что нужно сделать

### 1. Написать тесты (tests/test_user.py)
Использовать TestClient из fastapi.testclient.
Тесты:
- test_get_existed_user — создать пользователя, получить его, проверить 200 и данные.
- test_get_not_existed_user — проверить 404.
- test_create_user — проверить 201.
- test_update_user — проверить 200.
- test_delete_user — проверить 204.
- test_root — проверить GET / (200 и {"message": "Hello, World!"}).

### 2. Создать пайплайн тестов (.github/workflows/tests.yml)
- Имя: Test Python App.
- Триггер: push в ветки dev и main.
- Одно задание ci на ubuntu-latest.
- Шаги:
  - Checkout (actions/checkout@v4).
  - Setup Python 3.12 (actions/setup-python@v5).
  - Установка зависимостей (pip, requirements.txt, pytest, httpx).
  - Запуск тестов (pytest tests/).

### 3. Создать пайплайн сборки и доставки (.github/workflows/build-and-delivery.yml)
- Имя: Build and Delivery.
- Триггер: workflow_run после Test Python App в ветке main, тип completed.
- Одно задание cd на ubuntu-latest.
- Условие: if github.event.workflow_run.conclusion == 'success'.
- Шаги:
  - Checkout (actions/checkout@v4).
  - Логин в Docker Hub (docker/login-action@v3) с username: ${{ vars.DOCKERHUB_USERNAME }}, password: ${{ secrets.DOCKERHUB_TOKEN }}.
  - Сборка и пуш образа (docker/build-push-action@v6) с push: true, tags: ${{ vars.DOCKERHUB_USERNAME }}/my-app:latest.

### 4. Настроить переменные GitHub Actions
- Variable: DOCKERHUB_USERNAME (логин Docker Hub).
- Secret: DOCKERHUB_TOKEN (пароль Docker Hub).

### 5. Проверить
- Запушить в dev.
- Убедиться, что тесты прошли в Actions.
- Слить dev в main.
- Убедиться, что Build and Delivery прошёл.
- Проверить, что образ появился на Docker Hub.