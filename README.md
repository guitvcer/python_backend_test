# Python Backend Тестовое задание

## Клонирование
    git clone https://github.com/guitvcer/python_backend_test.git
    cd python_backend_test

## Запуск
    poetry install
    poetry run python manage.py makemigrations airflow
    poetry run python manage.py migrate
    poetry run python manage.py update_currencies & poetry run python manage.py runserver &

## Запуск через docker-compose
### Не запускается manage.py update_currencies
    docker-compose up
