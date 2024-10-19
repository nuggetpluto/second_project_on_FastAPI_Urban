from fastapi import FastAPI
from backend.db import engine, Base
from routers import task_r, user_r

app = FastAPI()

# Подключение маршрутов
app.include_router(user_r.router, prefix="/users", tags=["Users"])
app.include_router(task_r.router, prefix="/tasks", tags=["Tasks"])  # Подключаем маршруты задач


@app.get("/")
async def root():
    return {"message": "Welcome to Taskmanager"}


# Создание таблиц
Base.metadata.create_all(bind=engine)
