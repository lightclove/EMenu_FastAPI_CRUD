# app/main.py

from fastapi import FastAPI
from app.routers.food import food_router

app = FastAPI()

# Подключение маршрутов к приложению FastAPI
app.include_router(food_router, prefix="/api", tags=["food"])

@app.get("/")
def read_root():
    """
    Корневой маршрут для проверки состояния сервера.
    """
    return {"message": "Electronic restarant Menu API"}
