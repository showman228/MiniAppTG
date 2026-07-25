from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from server.app.config import settings

from server.app.routers.category import router as category_router
from server.app.routers.product import router as product_router
from server.app.routers.cart import router as cart_router
from server.app.routers.order import router as order_router
from server.app.routers.demo_auth.views import router as demo_auth_router

from .database import init_db

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount("/static", StaticFiles(directory=settings.static_dir), name="static")

app.include_router(category_router)
app.include_router(product_router)
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(demo_auth_router)


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
