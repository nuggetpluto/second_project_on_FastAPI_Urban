from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, update, delete
from typing import Annotated

# Импортируем локальные модули и схемы
from app.backend.db_depends import get_db
from app.schemas import CreateTask, UpdateTask
from app.models import Task, User

# Создание маршрутизатора
router = APIRouter()


# Функция 1: Получение всех задач
@router.get("/")
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    return tasks


# Функция 2: Получение задачи по ID
@router.get("/{task_id}")
async def task_by_id(task_id: int, db: Annotated[Session, Depends(get_db)]):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task:
        return task
    else:
        raise HTTPException(status_code=404, detail="Task was not found")


# Функция 3: Создание новой задачи
@router.post("/create")
async def create_task(new_task: CreateTask, user_id: int, db: Annotated[Session, Depends(get_db)]):
    # Поиск пользователя по ID
    user = db.scalar(select(User).where(User.id == user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User was not found")

    # Создание задачи и привязка к пользователю
    stmt = insert(Task).values(
        title=new_task.title,
        content=new_task.content,
        priority=new_task.priority,
        user_id=user_id,  # Связывание задачи с пользователем
        slug=new_task.title.lower().replace(" ", "-")  # Генерация slug на основе названия задачи
    )
    db.execute(stmt)
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


# Функция 4: Обновление задачи
@router.put("/update/{task_id}")
async def update_task(task_id: int, update_data: UpdateTask, db: Annotated[Session, Depends(get_db)]):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task:
        stmt = update(Task).where(Task.id == task_id).values(
            title=update_data.title,
            content=update_data.content,
            priority=update_data.priority
        )
        db.execute(stmt)
        db.commit()
        return {'status_code': status.HTTP_200_OK, 'transaction': 'Task update is successful!'}
    else:
        raise HTTPException(status_code=404, detail="Task was not found")


# Функция 5: Удаление задачи
@router.delete("/delete/{task_id}")
async def delete_task(task_id: int, db: Annotated[Session, Depends(get_db)]):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task:
        stmt = delete(Task).where(Task.id == task_id)
        db.execute(stmt)
        db.commit()
        return {'status_code': status.HTTP_200_OK, 'transaction': 'Task deletion is successful!'}
    else:
        raise HTTPException(status_code=404, detail="Task was not found")
