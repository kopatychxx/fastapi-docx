from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, LargeBinary
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
class Template(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True)
    content = Column(LargeBinary)  # Храним DOCX как BLOB
