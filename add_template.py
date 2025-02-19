import os
import asyncio
from database import SessionLocal, TemplateFile
from sqlalchemy.future import select

# Асинхронная функция добавления шаблона в базу данных
async def add_template_to_db(filename: str, content: bytes):
    async with SessionLocal() as db:
        # Проверка на наличие существующего файла в базе данных
        result = await db.execute(select(TemplateFile).filter_by(filename=filename))
        existing_template = result.scalar_one_or_none()

        if existing_template:
            # Обновляем содержимое существующего шаблона
            existing_template.content = content
            await db.commit()
            await db.refresh(existing_template)
            print(f"Template {filename} updated in the database!")
        else:
            # Создаем новый шаблон
            new_template = TemplateFile(filename=filename, content=content)
            db.add(new_template)
            await db.commit()
            await db.refresh(new_template)
            print(f"Template {filename} added to the database!")

# Функция для добавления всех шаблонов
async def add_templates():
    template_directory = "./templates_docx"  # Папка с шаблонами
    filenames = [
        "01_New_Client_Initial_Letter.docx",
        "02_Conduct_letter_Sec_B.docx",
        "03_Conduct_letter_Def_insurer.docx",
        "04_SOPB_request.docx",
        "05_Accident_Collision_Centre.docx",
        "06_Chart_request_GP.docx",
        "07_CRA_request.docx",
        "08_Employment_file_request.docx",
        "10_Letter_to_AHS.docx"
    ]

    for filename in filenames:
        file_path = os.path.join(template_directory, filename)
        if os.path.exists(file_path):
            print(f"Processing {filename}...")
            with open(file_path, "rb") as f:
                content = f.read()
            await add_template_to_db(filename, content)
        else:
            print(f"File {filename} not found!")

# Запуск асинхронной функции
if __name__ == "__main__":
    asyncio.run(add_templates())
