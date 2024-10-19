# app/models/task_r.py

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from models.user import User
from sqlalchemy.schema import CreateTable
from sqlalchemy.orm import relationship
from backend.db import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    priority = Column(Integer)
    completed = Column(Boolean)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)  # Добавлен индекс и nullable=False
    slug = Column(String, unique=True)

    user = relationship("User", back_populates="tasks")


# Печать SQL-запроса
print(CreateTable(Task.__table__))
