import asyncio
from database import engine, Base

async def init_db():
    # Создание таблиц
    async with engine.begin() as conn:
        # Вместо run_sync используйте этот подход для асинхронной работы
        await conn.run_sync(Base.metadata.create_all)

# Запуск функции инициализации
if __name__ == "__main__":
    asyncio.run(init_db())