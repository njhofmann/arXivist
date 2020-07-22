FROM python:3.8.3-slim-buster
COPY src /src/
COPY schema.sql .
COPY .env .
COPY requirements.txt .
RUN mkdir --mode=777 /pdfs
RUN pip install --no-cache-dir -r requirements.txt