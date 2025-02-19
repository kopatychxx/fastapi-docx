import asyncio
from database import SessionLocal, engine, Base, Template
import os

TEMPLATES_DIR = "templates_docx"  # Папка с шаблонами

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as session:
        for filename in os.listdir(TEMPLATES_DIR):
            filepath = os.path.join(TEMPLATES_DIR, filename)
            with open(filepath, "rb") as file:
                content = file.read()

            template = Template(filename=filename, content=content)
            session.add(template)

        await session.commit()

asyncio.run(init_db())
