# app/models/task.py

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.backend.db import Base
from app.models.user import User
from sqlalchemy.schema import CreateTable


class Task(Base):
    __tablename__ = 'tasks'
    __table_args__ = {'extend_existing': True}  # Указываем, что можно "расширить" уже существующую таблицу

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    priority = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    slug = Column(String, unique=True, index=True)

    # Связь с пользователем
    user = relationship("Task", back_populates="tasks")


# Печать SQL-запроса
print(CreateTable(Task.__table__))
