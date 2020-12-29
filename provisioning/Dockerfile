FROM python:3.9-slim-buster
RUN apt-get update && apt-get install -y gcc python3-dev iputils-ping && pip install --upgrade pip

WORKDIR /usr/src

COPY requirements-dev.txt .
RUN pip install -r requirements-dev.txt

COPY ./app ./app

WORKDIR /usr/src/app

ENTRYPOINT ["python", "tftp_server.py"]