FROM python:3-buster

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /app

COPY . .
