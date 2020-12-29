FROM python:3.9-slim-buster
RUN apt-get update && apt-get install -y gcc python3-dev && pip install --upgrade pip

COPY requirements-dev.txt /requirements-dev.txt
RUN pip install -r /requirements-dev.txt

COPY ./app /app
WORKDIR /app

ENTRYPOINT ["python", "tftp_server.py"]