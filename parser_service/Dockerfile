# Устанавливаем базовый образ Python
FROM python:3.11

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /fastapi_app

# Копируем файлы проекта в рабочую директорию контейнера
COPY . .

# Устанавливаем зависимости FastAPI
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт 8000 для доступа
EXPOSE 8000

# Команда для запуска FastAPI сервера
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
