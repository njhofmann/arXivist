#!/bin/sh
docker-compose up --build -d
docker exec -it $(docker-compose ps -q app) /bin/bash run.sh