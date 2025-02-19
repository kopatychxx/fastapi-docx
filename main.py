from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import SessionLocal, Template
from docx import Document
import os
import zipfile

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Получаем шаблоны из базы данных
async def get_templates():
    async with SessionLocal() as session:
        result = await session.execute(select(Template))
        return result.scalars().all()

# Форма для ввода данных
@app.get("/", response_class=HTMLResponse)
async def show_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

# Генерация DOCX
@app.post("/generate-docx/")
async def generate_docx(
    client_name: str = Form(...),
    street_address: str = Form(...),
    city_postal_code: str = Form(...),
    client_email: str = Form(...),
    accident_date: str = Form(...),
    current_date: str = Form(...),
    file_number: str = Form(...),
):
    templates_data = await get_templates()

    replacements = {
        "{{ClientName}}": client_name,
        "{{StreetAddress}}": street_address,
        "{{CityPostalCode}}": city_postal_code,
        "{{ClientEmail}}": client_email,
        "{{AccidentDate}}": accident_date,
        "{{CurrentDate}}": current_date,
        "{{FileNumber}}": file_number
    }

    output_dir = f"generated/{file_number}"
    os.makedirs(output_dir, exist_ok=True)

    files_to_zip = []

    for template_data in templates_data:
        template_path = os.path.join(output_dir, template_data.filename)
        with open(template_path, "wb") as file:
            file.write(template_data.content)

        doc = Document(template_path)

        for para in doc.paragraphs:
            for key, value in replacements.items():
                if key in para.text:
                    para.text = para.text.replace(key, value)

        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for key, value in replacements.items():
                        if key in cell.text:
                            cell.text = cell.text.replace(key, value)

        output_filename = os.path.join(output_dir, f"generated_{template_data.filename}")
        doc.save(output_filename)
        files_to_zip.append(output_filename)

    zip_filename = f"{file_number}_documents.zip"
    zip_path = os.path.join("generated", zip_filename)

    with zipfile.ZipFile(zip_path, "w") as zipf:
        for file in files_to_zip:
            zipf.write(file, os.path.basename(file))

    return FileResponse(zip_path, media_type="application/zip", filename=zip_filename)

# Запуск FastAPI на Railway
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)