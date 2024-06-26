# DOCKERFILE


FROM python:3.12-slim

RUN apt-get update && apt-get -y upgrade
WORKDIR /app

COPY ./requirements.txt .

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . .