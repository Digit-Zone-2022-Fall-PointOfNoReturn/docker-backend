FROM python:3-alpine

COPY . /django

WORKDIR /django

RUN pip install -r requirements.txt

ENTRYPOINT sh scripts/init.sh && uvicorn config.asgi:application --host 0.0.0.0 --port 8000
