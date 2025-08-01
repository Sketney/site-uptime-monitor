FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

# обновляем pip, чтобы избежать ошибок
RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
