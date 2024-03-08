FROM python:3.11

# Установка утилиты wait-for-it
RUN apt-get update && apt-get install -y wait-for-it

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["wait-for-it", "db:5432", "--", "alembic", "upgrade", "head", "&&", "gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]

#CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
