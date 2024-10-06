# app/models/task.py

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.backend.db import Base
from app.models.user import User
from sqlalchemy.schema import CreateTable

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.backend.db import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    priority = Column(Integer)
    completed = Column(Boolean)
    user_id = Column(Integer, ForeignKey("users.id"))
    slug = Column(String, unique=True)

    # Обратная связь на пользователя
    user = relationship("User", back_populates="tasks")


# Печать SQL-запроса
print(CreateTable(Task.__table__))
