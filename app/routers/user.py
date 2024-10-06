from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, update, delete
from typing import Annotated
from slugify import slugify

# Импортируем локальные модули
from app.backend.db import SessionLocal
from app.schemas import CreateUser, UpdateUser
from app.models import User, Task

# Создание маршрутизатора
router = APIRouter()


# Функция для подключения к БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Функция 1: Получение всех пользователей
@router.get("/")
async def all_users(db: Annotated[Session, Depends(get_db)]):
    # Получение всех пользователей из базы данных
    users = db.scalars(select(User)).all()
    return users


# Функция 2: Получение пользователя по ID
@router.get("/{user_id}")
async def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    # Поиск пользователя в базе данных по ID
    user = db.scalar(select(User).where(User.id == user_id))
    if user:
        return user
    else:
        # Если пользователь не найден, возвращаем ошибку 404
        raise HTTPException(status_code=404, detail="User was not found")


# Функция 3: Создание нового пользователя
@router.post("/create")
async def create_user(new_user: CreateUser, db: Annotated[Session, Depends(get_db)]):
    # Генерация slug из username
    slug = slugify(new_user.username)
    # Вставка нового пользователя в таблицу
    stmt = insert(User).values(
        username=new_user.username,
        firstname=new_user.firstname,
        lastname=new_user.lastname,
        age=new_user.age,
        slug=slug
    )
    db.execute(stmt)
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


# Функция 4: Обновление пользователя
@router.put("/update/{user_id}")
async def update_user(user_id: int, update_data: UpdateUser, db: Annotated[Session, Depends(get_db)]):
    # Проверяем, существует ли пользователь с данным user_id
    user = db.scalar(select(User).where(User.id == user_id))
    if user:
        # Обновление данных пользователя
        stmt = update(User).where(User.id == user_id).values(
            firstname=update_data.firstname,
            lastname=update_data.lastname,
            age=update_data.age
        )
        db.execute(stmt)
        db.commit()
        return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}
    else:
        raise HTTPException(status_code=404, detail="User was not found")


@router.delete("/delete/{user_id}")
async def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.scalar(select(User).where(User.id == user_id))
    if user:
        # Удаление всех задач пользователя перед удалением самого пользователя
        db.execute(delete(Task).where(Task.user_id == user_id))
        # Удаление пользователя
        db.execute(delete(User).where(User.id == user_id))
        db.commit()
        return {'status_code': status.HTTP_200_OK, 'transaction': 'User and related tasks are deleted successfully!'}
    else:
        raise HTTPException(status_code=404, detail="User was not found")


# Новый маршрут для получения задач пользователя по ID
@router.get("/{user_id}/tasks")
async def tasks_by_user_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.scalar(select(User).where(User.id == user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User was not found")

    tasks = db.scalars(select(Task).where(Task.user_id == user_id)).all()
    return tasks
