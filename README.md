# ylab_hw_2023
Домашнее задание #1 от YLAB "Проект на FastAPI с использованием PostgreSQL. Реализовать
REST API по работе с меню ресторана, все CRUD операции".

****Инструкция по запуску:****

Установить зависимости из requirements.txt

Произвести миграцию БД:
- **alembic upgrade head**

Для запуска:
- запустить файл **main.py** 

    ИЛИ

- Через терминал **uvicorn main:app --reload**


**Затем можно запускать тесты в Postman**


Данные для БД:

POSTGRES_DB = "ylab_hw"

POSTGRES_USER = "postgres"

POSTGRES_PASSWORD = "root"
