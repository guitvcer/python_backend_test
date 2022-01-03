FROM python:3.10.0-bullseye

WORKDIR /app

EXPOSE 9000

RUN pip install -U pip
RUN pip install poetry

COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

COPY . .

RUN python manage.py migrate
