# Bookstore API

FastAPI-приложение платформы объявлений о продаже книг.

## Стек
- **FastAPI** — веб-фреймворк
- **SQLAlchemy 2.0** (async) — ORM
- **PostgreSQL** — база данных
- **Pydantic v2** — валидация данных
- **pytest + pytest-asyncio** — тесты
- **python-jose** — JWT авторизация
- **passlib + bcrypt** — хэширование паролей

## Установка и запуск

### 1. Клонирование и настройка окружения

```bash
git clone <your-repo>
cd bookstore
cp .env_example .env
# отредактируйте .env под ваши параметры подключения
```

### 2. Запуск БД через Docker

```bash
docker-compose up -d
```

Или, если Postgres установлен локально — создайте вручную две БД: `bookstore` и `bookstore_test`.

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Запуск приложения

```bash
uvicorn src.main:app --reload
```

Приложение доступно на `http://localhost:8000`  
Документация Swagger: `http://localhost:8000/docs`

### 5. Запуск тестов

```bash
pytest src/tests/ -v
```

## API Endpoints

### Продавцы (Sellers)

| Метод | URL | Описание | Auth |
|-------|-----|----------|------|
| POST | `/api/v1/seller/` | Регистрация продавца | — |
| GET | `/api/v1/seller/` | Список всех продавцов | — |
| GET | `/api/v1/seller/{id}` | Данные продавца + его книги | JWT |
| PUT | `/api/v1/seller/{id}` | Обновление данных продавца | — |
| DELETE | `/api/v1/seller/{id}` | Удаление продавца (и его книг) | — |

### Книги (Books)

| Метод | URL | Описание | Auth |
|-------|-----|----------|------|
| POST | `/api/v1/books/` | Добавить книгу | JWT |
| GET | `/api/v1/books/` | Список всех книг | — |
| GET | `/api/v1/books/{id}` | Данные о книге | — |
| PUT | `/api/v1/books/{id}` | Обновить книгу | JWT |
| DELETE | `/api/v1/books/{id}` | Удалить книгу | — |

### Авторизация (JWT)

| Метод | URL | Описание |
|-------|-----|----------|
| POST | `/api/v1/token` | Получить JWT токен |

**Получение токена:**
```json
POST /api/v1/token
{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

**Использование токена:**
```
Authorization: Bearer <token>
```

## Структура проекта

```
src/
├── configurations/   # Настройки, подключение к БД
├── models/          # SQLAlchemy ORM модели
├── routers/         # FastAPI роутеры (эндпоинты)
├── schemas/         # Pydantic схемы
├── services/        # Бизнес-логика
├── tests/           # Тесты pytest
└── main.py          # Точка входа
```
