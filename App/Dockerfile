# Устанавливаем базовый образ Python
FROM python:3.11

RUN mkdir /django_app

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /django_app

# Копируем файлы проекта в рабочую директорию контейнера
COPY . .

# Устанавливаем зависимости Django
RUN pip install -r requirements.txt

# Открываем порт 8000 для доступа
EXPOSE 8000

# Команда для запуска сервера разработки Django
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
