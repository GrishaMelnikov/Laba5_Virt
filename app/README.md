# My App

Минимальное FastAPI-приложение для лабораторной работы по CI/CD.

## Быстрый запуск

```bash
pip install -r requirements.txt
uvicorn src.main:app --reload
```

## Запуск тестов

```bash
pytest tests/
```

## Docker

```bash
docker build -t my-app .
docker run -p 8000:8000 my-app
```

## Эндпоинты

- `GET /` — приветственное сообщение
- `POST /users/` — создать пользователя
- `GET /users/{id}` — получить пользователя
- `PUT /users/{id}` — обновить пользователя
- `DELETE /users/{id}` — удалить пользователя