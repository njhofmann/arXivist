FROM python:3.8.3-slim-buster
COPY src /src/
#RUN apt-get update && apt-get install -y iputils-ping && apt-get -y install netcat && apt-get -y install curl
COPY init.sql .
COPY .env .
COPY run.sh run.sh
RUN chmod 744 run.sh
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
