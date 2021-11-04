FROM python:3.10.0-bullseye

WORKDIR /app

EXPOSE 9000

COPY . .

RUN pip install -U pip
RUN pip install poetry
RUN poetry install
RUN poetry run python manage.py makemigrations airflow
RUN poetry run python manage.py migrate