#!/bin/sh

LOG_FILE="output.log"

# load env file
set -o allexport
source ./.env
set +o allexport

if [ $# -gt 1 ]; then
    echo "require zero or one arguments"
    exit 1
fi

if [ $# -eq 1 ]; then
  if [ $1 = "update" ]; then
    echo "rebuilding arXivist"
    docker-compose down
    docker-compose up --build -d --force --quiet > $LOG_FILE
  else
    echo "invalid single parameter"
    exit 1
  fi
elif [ $# -eq 0 ]; then
  echo "starting arXivist"
  docker-compose start > $LOG_FILE
fi

# clear if production mode
if [ $PROGRAM_MODE = prod ]; then
  reset
fi

echo "entering arXivist"
docker exec -it $(docker-compose ps -q app) python -m src.arxivist $PROGRAM_MODE

echo "exiting arXivist"
docker-compose stop >> $LOG_FILE &

# clear if production mode
if [ $PROGRAM_MODE = prod ]; then
  reset
fi