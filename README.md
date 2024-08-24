## Инструкция по развёртыванию проекта

* клонировать проект на компьютер `git clone https://github.com/foxygen-d/cat_charity_fund.git`
* создание виртуального окружения `python3 -m venv venv`
* запуск виртуального окружения `py venv/Scripts(bin)/activate`
* установить зависимости из файла requirements.txt `pip install -r requirements.txt`
* запуск сервера `uvicorn main:app`
* запуск сервера с автоматическим рестартом `uvicorn main:app --reload`
* инициализируем Alembic в проекте `alembic init --template async alembic`
* создание файла миграции `alembic revision --autogenerate -m "migration name"`
* применение миграций `alembic upgrade head`
* отмена миграций `alembic downgrade`
* запуск тестов `pytest`


## Системные требования

* Python > 3.6
* FastAPI > 0.7.0
* Works on Linux, Windows, macOS