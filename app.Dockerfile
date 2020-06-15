FROM python:3.8.3-slim-buster
COPY src /src/
COPY database/db.env /database/
COPY database/db_init.py /database/db_init.py
COPY run.sh run.sh
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt