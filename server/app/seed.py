"""Заполнение БД тестовыми данными.

Запуск (локально):
    python -m server.app.seed

Запуск в Docker:
    docker compose exec app python -m server.app.seed

Зайти в pgAdmin:
docker-compose --profile dev up -d
"""
import asyncio

from sqlalchemy import select

from server.app.database import SessionLocal, engine
from server.app.models import Category, Product, User, Order
from server.app.database import Base


CATEGORIES = [
    {"name": "Электроника", "slug": "electronics"},
    {"name": "Одежда", "slug": "clothing"},
    {"name": "Книги", "slug": "books"},
    {"name": "Дом и сад", "slug": "home"},
]

PRODUCTS = [
    # Электроника
    {"name": "Смартфон Galaxy X", "description": "Флагманский смартфон 2026 года, 256GB, AMOLED.", "price": 79990, "category": "electronics", "image_url": "/static/images/phone.jpg"},
    {"name": "Беспроводные наушники AirPro", "description": "Активное шумоподавление, 30 часов работы.", "price": 14990, "category": "electronics", "image_url": "/static/images/headphones.jpg"},
    {"name": "Ноутбук UltraBook 14", "description": "Лёгкий ноутбук для работы, 16GB RAM, 1TB SSD.", "price": 109990, "category": "electronics", "image_url": "/static/images/laptop.jpg"},
    # Одежда
    {"name": "Футболка Basic White", "description": "Хлопковая футболка унисекс, 100% хлопок.", "price": 1490, "category": "clothing", "image_url": "/static/images/tshirt.jpg"},
    {"name": "Джинсы Slim Fit", "description": "Классические джинсы, синий деним.", "price": 4990, "category": "clothing", "image_url": "/static/images/jeans.jpg"},
    {"name": "Куртка зимняя", "description": "Тёплая куртка с капюшоном, до -25°C.", "price": 12990, "category": "clothing", "image_url": "/static/images/jacket.jpg"},
    # Книги
    {"name": "Чистый код", "description": "Роберт Мартин — классика программирования.", "price": 1290, "category": "books", "image_url": "/static/images/clean_code.jpg"},
    {"name": "Алгоритмы. Построение и анализ", "description": "Кормен и др. — фундаментальный учебник.", "price": 2490, "category": "books", "image_url": "/static/images/clrs.jpg"},
    # Дом и сад
    {"name": "Кофеварка EspressoPro", "description": "Капельная кофеварка на 12 чашек.", "price": 6990, "category": "home", "image_url": "/static/images/coffee.jpg"},
    {"name": "Набор посуды Premium", "description": "12 предметов из нержавеющей стали.", "price": 8990, "category": "home", "image_url": "/static/images/dishes.jpg"},
]

USERS = [
    {"telegram_id": 100000001, "username": "alice", "firstname": "Алиса"},
    {"telegram_id": 100000002, "username": "bob", "firstname": "Боб"},
    {"telegram_id": 100000003, "username": "charlie", "firstname": "Чарли"},
]


async def seed() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as db:
        # --- categories ---
        existing = (await db.execute(select(Category.slug))).scalars().all()
        existing_slugs = set(existing)
        for c in CATEGORIES:
            if c["slug"] not in existing_slugs:
                db.add(Category(**c))
        await db.commit()

        cats = (await db.execute(select(Category))).scalars().all()
        slug_to_id = {c.slug: c.id for c in cats}

        # --- products ---
        existing_names = set((await db.execute(select(Product.name))).scalars().all())
        for p in PRODUCTS:
            if p["name"] in existing_names:
                continue
            db.add(Product(
                name=p["name"],
                description=p["description"],
                price=p["price"],
                category_id=slug_to_id[p["category"]],
                image_url=p["image_url"],
            ))
        await db.commit()

        # --- users ---
        existing_tg = set((await db.execute(select(User.telegram_id))).scalars().all())
        for u in USERS:
            if u["telegram_id"] not in existing_tg:
                db.add(User(**u))
        await db.commit()

        # --- orders (по одному заказу на пользователя) ---
        users = (await db.execute(select(User))).scalars().all()
        products = (await db.execute(select(Product))).scalars().all()
        existing_orders = (await db.execute(select(Order.user_id, Order.product_id))).all()
        existing_pairs = {(uid, pid) for uid, pid in existing_orders}

        if products and users:
            for i, user in enumerate(users):
                product = products[i % len(products)]
                if (user.id, product.id) in existing_pairs:
                    continue
                qty = (i % 3) + 1
                db.add(Order(
                    user_id=user.id,
                    product_id=product.id,
                    quantity=qty,
                    price=product.price,
                    total_price=product.price * qty,
                ))
            await db.commit()

        print(
            f"Seed done: {len(CATEGORIES)} categories, "
            f"{len(PRODUCTS)} products, {len(USERS)} users, "
            f"{len(users)} demo orders."
        )


if __name__ == "__main__":
    asyncio.run(seed())
