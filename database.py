from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Integer, String, Column, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
import os

# Получаем строку подключения из переменной окружения
DATABASE_URL = os.getenv("DATABASE_URL")

# Если DATABASE_URL не определён, выбрасывается ошибка
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL is not set in the environment variables.")

# Создаём асинхронное подключение к базе данных
engine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
Base = declarative_base()

# Модель для хранения шаблонов
class TemplateFile(Base):
    __tablename__ = "templates_file"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True)
    content = Column(LargeBinary)  # Храним DOCX как BLOB

# Функция для получения сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Функция для инициализации базы данных (создание таблиц)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)