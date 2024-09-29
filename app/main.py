from fastapi import FastAPI
from app.backend.db import engine, Base
from app.routers import task, user

# Создание приложения FastAPI
app = FastAPI()

# Подключение маршрутов
app.include_router(task.router)
app.include_router(user.router)

# Базовый маршрут
@app.get("/")
async def root():
    return {"message": "Welcome to Taskmanager"}


# Создание таблиц
Base.metadata.create_all(bind=engine)
