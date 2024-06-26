# DOCKERFILE


FROM python:3.10-slim

RUN apt-get update && apt-get -y upgrade  && apt-get install -y gcc
WORKDIR /app

COPY ./requirements.txt .

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . .