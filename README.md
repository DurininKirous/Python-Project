# Observability-ready FastAPI Service

Этот проект демонстрирует, как построить сервис на FastAPI c хранением данных в PostgreSQL и мониторингом через Prometheus

## Возможности

- **CRUD API** для сущности `service_checks`, которая хранит статус произвольных проверок.
- **PostgreSQL** в качестве хранилища, асинхронные сессии `sqlalchemy.ext.asyncio` и драйвер `asyncpg`.
- **Prometheus** scrape endpoint `/metrics`, созданный через `prometheus-fastapi-instrumentator`.
- **Тесты** на `pytest` + встроенный `TestClient` для проверки основных сценариев API.

## Быстрый старт

1. Установите Docker и Docker Compose.
2. Соберите и запустите окружение:
   ```bash
   docker compose up --build
   ```
3. Сервис будет доступен на `http://localhost:8000`, документация Swagger — `http://localhost:8000/docs`.
4. Метрики Prometheus доступны на `http://localhost:8000/metrics`.
5. Веб-интерфейс Prometheus — `http://localhost:9090`.

## Локальная разработка без Docker

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
export DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/app"
uvicorn app.main:app --reload
```

Запустите PostgreSQL отдельно (например, через Docker), либо измените `DATABASE_URL` на совместимый драйвер (например, `sqlite+aiosqlite:///./dev.db`).

## Структура проекта

```
app/
  api/v1/routes.py  # эндпоинты CRUD
  config.py         # pydantic-настройки
  crud.py           # функции работы с БД
  database.py       # фабрики engine/session
  main.py           # создание FastAPI приложения
  models.py         # SQLAlchemy модели
  schemas.py        # Pydantic-схемы
```

## Тесты

```bash
pytest
```

Тесты используют временную SQLite-базу, поэтому не требуют дополнительной подготовки.

## Метрики Prometheus

`prometheus-fastapi-instrumentator` автоматически регистрирует ряд метрик:

- Время ответа (`http_response_duration_seconds`).
- Количество запросов (`http_requests_total`).
- Размер ответа (`http_response_size_bytes`).

Можно расширить метрики, добавив кастомный middleware или отдельные gauge/counter.

## Дальнейшее развитие

- Добавить Alembic для миграций.
- Вынести метрики БД (pg_stat_activity) через экспортёры.
- Подключить Grafana и собрать дашборд.
