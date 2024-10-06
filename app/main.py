from fastapi import FastAPI
from app.backend.db import engine, Base
from app.routers import task, user

app = FastAPI()

# Подключение маршрутов
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(task.router, prefix="/tasks", tags=["Tasks"])  # Подключаем маршруты задач


@app.get("/")
async def root():
    return {"message": "Welcome to Taskmanager"}


# Создание таблиц
Base.metadata.create_all(bind=engine)
