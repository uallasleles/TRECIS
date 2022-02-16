#!/bin/bash

docker-compose stop && \
docker-compose down && \
docker system prune -a && \
docker volume rm $(docker volume ls -q) && \
sudo rm -rf ~/Source/TRECIS/data/mongodbdata/*