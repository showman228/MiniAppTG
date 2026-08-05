from fastapi import FastAPI
from sqladmin import Admin
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from server.app.config import settings
from server.app.middlewares.process_time import ProcessTimeMiddleware
from server.app.core.admin_auth import AdminAuth

from server.app.models.admin.users import UsersAdmin
from server.app.models.admin.categories import CategoriesAdmin
from server.app.models.admin.products import ProductsAdmin
from server.app.models.admin.orders import OrdersAdmin

from server.app.routers.category import router as category_router
from server.app.routers.product import router as product_router
from server.app.routers.cart import router as cart_router
from server.app.routers.order import router as order_router
from server.app.routers.user import router as user_router

from .database import init_db, engine

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    docs_url="/docs",
    redoc_url="/redoc"
)

admin = Admin(app, engine, authentication_backend=AdminAuth(secret_key=settings.SECRET_KEY))

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.add_middleware(ProcessTimeMiddleware)

app.mount("/static", StaticFiles(directory=settings.static_dir), name="static")

app.include_router(category_router)
app.include_router(product_router)
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(user_router)

admin.add_view(UsersAdmin)
admin.add_view(CategoriesAdmin)
admin.add_view(ProductsAdmin)
admin.add_view(OrdersAdmin)


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/")
async def root():
    return {
        "message": "Welcome to MiniAPPTG",
        "docs": "/api/docs"
    }


@app.get("/health")
async def health():
    return {"status": "200_OK"}
