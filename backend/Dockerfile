FROM python:3.9-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  && apt-get -y install curl netcat gcc iputils-ping \
  && apt-get clean

COPY . .

RUN pip install -r requirements.txt