FROM python:3.13-slim

WORKDIR /app/movie_service

COPY requirements.txt requirements.txt

RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

RUN pip install -r requirements.txt \
    && rm -rf /root/.cache/pip

COPY . .

WORKDIR /app

CMD ["uvicorn", "movie_service.app.main:app", "--host", "0.0.0.0"]