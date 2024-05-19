
## Выпускная квалификационная работа.

# Описание проекта

* Django: основное веб-приложение, работающее на порту 8000.
* FastAPI: микросервис для парсинга данных, работающий на порту 8001.
* PostgreSQL: база данных, используемая Django приложением.
* InfluxDB: база данных для временных рядов, используемая для хранения данных от FastAPI микросервиса.

**Технологии:**
Python • Django • FastAPI • PostgreSQL • InfluxDB • Docker • Html • CSS • Javascript

# Инструкция по запуску приложения

## Подготовка окружения

1. Установите Docker и Docker Compose, если они еще не установлены.

## Запуск приложения через docker-compose

1. Склонируйте репозиторий:
   `git clone git@github.com:oliver2214/petro-tracker.git`

2. Перейдите в каталог с проектом:
   `cd petro-tracker`

3. Запустите приложение с помощью Docker Compose:
   `docker compose up`

   *Если с первого раза не получится повторите команду*

4. Django приложение будет доступно по адресу [localhost:8000](http://localhost:8000).

5. API парсера будет доступен по адресу [localhost:8001/docs](http://localhost:8001/docs).
