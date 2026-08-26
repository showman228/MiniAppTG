# MiniAPPTG — мини-магазин на FastAPI + React

Пет-проект: витрина интернет-магазина, задуманная как Telegram Mini App. Пишется для того, чтобы разобраться с асинхронным FastAPI, SQLAlchemy 2.0, миграциями Alembic и React — поэтому код намеренно простой, без лишних абстракций.

Что уже работает: каталог с категориями, карточка товара, корзина, регистрация и вход, история заказов, админка на sqladmin.

**Стек:** Python 3.13 · FastAPI · SQLAlchemy 2.0 (async) · PostgreSQL 16 · Alembic · React 19 · Vite · axios

---

## Запуск

Нужен только Docker. Всё поднимается тремя контейнерами: база, бэкенд, фронт.

```bash
cp .env.example .env   # если .env ещё нет — заполни POSTGRES_* и SECRET_KEY
docker compose up -d --build
```

| Что | Адрес |
|---|---|
| Витрина (React) | http://localhost:5173 |
| API | http://localhost:8000 |
| Swagger | http://localhost:8000/docs |
| Админка | http://localhost:8000/admin |
| PostgreSQL | localhost:5432 |

Оба сервиса запускаются с hot-reload: и `uvicorn --reload`, и Vite видят правки в файлах на хосте — пересобирать контейнеры для изменений в коде не нужно.

Полезные команды:

```bash
docker compose logs -f frontend      # логи Vite
docker compose logs -f app           # логи FastAPI
docker compose down                  # остановить
docker compose down -v               # остановить и стереть базу
```

После правки `frontend/package.json` образ нужно пересобрать вместе с анонимным томом, иначе внутри останется старый набор пакетов:

```bash
docker compose build frontend && docker compose up -d --force-recreate -V frontend
```

### Переменные окружения

`.env` в корне репозитория, читается и бэкендом (`server/app/config.py`), и docker-compose:

| Переменная | Назначение |
|---|---|
| `POSTGRES_USER` / `POSTGRES_PASSWORD` / `POSTGRES_DB` | доступ к базе |
| `POSTGRES_HOST` | `db` для докера, `localhost` при локальном запуске |
| `POSTGRES_PORT` | обычно `5432` |
| `SECRET_KEY` | подпись сессионной куки админки |
| `DEBUG` | `True` включает вывод SQL-запросов |

### Миграции

```bash
docker compose exec app alembic upgrade head
docker compose exec app alembic revision --autogenerate -m "описание"
```

---

## Структура

```
.
├── server/                     бэкенд
├── frontend/                   фронтенд
├── alembic/                    миграции
├── docker-compose.yml          db + app + frontend
├── pyproject.toml              зависимости Python (poetry)
├── AGENTS.md                   правила для ИИ-агентов
└── Todo.txt                    роадмап проекта
```

### `server/` — FastAPI

```
server/
├── Dockerfile
├── static/images/              фотографии товаров (отдаются как /static/images/*)
└── app/
    ├── main.py                 приложение, CORS, StaticFiles, подключение роутеров
    ├── config.py               настройки из .env через pydantic-settings
    ├── database.py             async engine, сессии, Base
    ├── routers/                HTTP-эндпоинты
    │   ├── category.py         GET /category/
    │   ├── product.py          GET /products/, /products/category/{id}, /products/{id}
    │   ├── cart.py             POST /cart/add|details|remove, PUT /cart/update
    │   ├── order.py            /order/* — требуют авторизации
    │   └── user.py             POST /users/register, GET /users/me
    ├── schemas/                Pydantic-модели запросов и ответов
    ├── models/                 таблицы SQLAlchemy (+ models/admin — вьюхи sqladmin)
    ├── crud/                   запросы к базе
    ├── services/               бизнес-логика поверх crud
    ├── core/                   auth.py (HTTP Basic), admin_auth.py, security.py (bcrypt)
    └── middlewares/            замер времени обработки запроса
```

Слои идут сверху вниз: `routers` → `services` → `crud` → `models`. Роутер разбирает HTTP, сервис знает правила, crud ходит в базу.

**Корзина не хранится на сервере.** Клиент держит словарь `{product_id: quantity}` у себя и отправляет его целиком в каждом запросе, а в ответ получает пересчитанный состав с ценами и суммой. Таблицы корзины в базе нет.

**Авторизация — HTTP Basic.** Логин идёт по `username` (не по email), пароль хешируется bcrypt. Отдельного эндпоинта логина нет: клиент отправляет заголовок `Authorization: Basic ...` на `GET /users/me` и по ответу понимает, верны ли данные.

### `frontend/` — React + Vite

```
frontend/
├── Dockerfile
├── vite.config.js              dev-сервер и прокси на бэкенд
├── index.html
└── src/
    ├── main.jsx                точка входа, провайдеры, импорт стилей
    ├── App.jsx                 маршруты
    ├── api/
    │   ├── client.js           axios: подстановка Basic-заголовка, обработка 401
    │   └── categories.js · products.js · cart.js · users.js · orders.js
    ├── context/
    │   ├── AuthContext.jsx     текущий пользователь, вход, регистрация, выход
    │   └── CartContext.jsx     корзина: localStorage + синхронизация с сервером
    ├── hooks/useFetch.js       загрузка данных с состояниями loading / error
    ├── components/             Header, CategoryChips, ProductCard, CartRow, AuthForms, Notice
    ├── views/                  HomePage, ProductPage, CartPage, ProfilePage
    ├── utils/format.js         цены, даты, склонение «товар / товара / товаров»
    └── styles/                 base · layout · catalog · forms
```

Страницы: `/` — витрина, `/product/:id` — карточка товара, `/cart` — корзина, `/profile` — профиль и история заказов.

**Запросы идут через прокси Vite, а не напрямую на `:8000`.** Всё, что начинается с `/api`, уходит на бэкенд с отрезанным префиксом; `/static` проксируется как есть, поэтому пути к картинкам из базы работают без склейки. Адрес бэкенда задаётся переменной `API_TARGET` — её читает сам Vite внутри docker-сети, в браузер она не попадает.

Префикс `/api` нужен, чтобы развести адреса: `/cart` — это одновременно маршрут страницы и префикс роутера на бэкенде.

**Корзина живёт в localStorage**, но состав и суммы всегда берутся из ответа сервера — после каждого изменения словарь пересобирается из того, что вернул бэкенд. Если товар удалили из базы, он просто исчезнет из корзины.

---

## Локальный запуск без Docker

Если нужно погонять бэкенд напрямую:

```bash
poetry install
POSTGRES_HOST=localhost poetry run uvicorn server.app.main:app --reload
cd frontend && npm install && npm run dev
```

Учти: `static_dir` в настройках — путь относительно рабочей директории, поэтому картинки товаров найдутся только при запуске из `server/`. В Docker этой проблемы нет — там каталог смонтирован в `/app/static`.

Форматирование Python — black: `poetry run black server/`
