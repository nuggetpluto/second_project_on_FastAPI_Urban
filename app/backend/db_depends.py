from .db import SessionLocal

# Асинхронная функция подключения к БД
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
