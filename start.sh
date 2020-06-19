#!/bin/sh
docker-compose up --build -d
docker exec -it $(docker-compose ps -q app) python -m src.arxivist prod
