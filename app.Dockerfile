FROM python:3.8.3-slim-buster
COPY src /src/
COPY init.sql .
COPY .env .
COPY run.sh run.sh
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt