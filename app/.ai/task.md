Создай минимальное FastAPI-приложение для лабораторной работы по CI/CD.

## Структура проекта

my-app/
├── .github/
│   └── workflows/
│       ├── tests.yml
│       └── build-and-delivery.yml
├── src/
│   ├── __init__.py
│   ├── main.py
│   └── routers/
│       ├── __init__.py
│       └── user.py
├── tests/
│   ├── __init__.py
│   └── test_user.py
├── requirements.txt
├── Dockerfile
└── README.md

## Требования к коду

### src/main.py
- FastAPI-приложение
- Подключить роутер user с префиксом /users
- GET / → {"message": "Hello, World!"}

### src/routers/user.py
- APIRouter
- Pydantic-модель User: name (str), email (str)
- Хранилище в памяти: users_db (dict), next_id (int)
- GET /users/{user_id} → 200 или 404
- POST /users → 201
- PUT /users/{user_id} → 200 или 404
- DELETE /users/{user_id} → 204 или 404

### tests/test_user.py
- TestClient из fastapi.testclient
- test_get_existed_user — создать, получить, проверить
- test_get_not_existed_user — 404
- test_create_user — 201
- test_update_user — 200
- test_delete_user — 204
- test_root — GET /

### requirements.txt
fastapi
uvicorn
pytest
httpx

### Dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

### .github/workflows/tests.yml
name: Test Python App
on:
  push:
    branches: [ 'dev', 'main' ]
jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - Checkout (actions/checkout@v4)
      - Setup Python 3.12 (actions/setup-python@v5)
      - Install Dependencies (pip, requirements.txt, pytest, httpx)
      - Run Tests (pytest tests/)

### .github/workflows/build-and-delivery.yml
name: Build and Delivery
on:
  workflow_run:
    workflows: ["Test Python App"]
    types: [completed]
    branches: [ 'main' ]
jobs:
  cd:
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    steps:
      - Checkout (actions/checkout@v4)
      - Login to Docker Hub (docker/login-action@v3)
        username: ${{ vars.DOCKERHUB_USERNAME }}
        password: ${{ secrets.DOCKERHUB_TOKEN }}
      - Build and Push (docker/build-push-action@v6)
        push: true
        tags: ${{ vars.DOCKERHUB_USERNAME }}/my-app:latest

### README.md
Краткое описание, команды запуска, тестов, Docker.

## Важно
- Все __init__.py — пустые
- Код должен работать без ошибок
- Тесты должны проходить
- Никаких лишних зависимостей