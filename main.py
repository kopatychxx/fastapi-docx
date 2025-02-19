from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from docx import Document
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Показываем форму
@app.get("/", response_class=HTMLResponse)
async def show_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

# Генерация одного DOCX
@app.post("/generate-docx/")
async def generate_docx(
    client_name: str = Form(...),
    street_address: str = Form(...),
    city_postal_code: str = Form(...),
    client_email: str = Form(...),
    accident_date: str = Form(...),
    current_date: str = Form(...),
    file_number: str = Form(...)
):
    template_path = "template.docx"  # Путь к шаблону
    output_filename = f"generated_{file_number}.docx"

    if not os.path.exists(template_path):
        return {"error": "Файл шаблона не найден"}

    doc = Document(template_path)

    replacements = {
        "{{ClientName}}": client_name,
        "{{StreetAddress}}": street_address,
        "{{CityPostalCode}}": city_postal_code,
        "{{ClientEmail}}": client_email,
        "{{AccidentDate}}": accident_date,
        "{{CurrentDate}}": current_date,
        "{{FileNumber}}": file_number
    }

    # Заменяем переменные в тексте
    for para in doc.paragraphs:
        for key, value in replacements.items():
            if key in para.text:
                para.text = para.text.replace(key, value)

    # Заменяем переменные в таблицах (если есть)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for key, value in replacements.items():
                    if key in cell.text:
                        cell.text = cell.text.replace(key, value)

    # Сохраняем новый файл
    doc.save(output_filename)

    return FileResponse(output_filename, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", filename=output_filename)
