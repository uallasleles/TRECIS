## COI - TRECIS
### Python/Flask/ALPR application with Mongo database

Project structure:
```
.
├── docker-compose.yaml
├── flask
│   ├── Dockerfile
│   ├── requirements.txt
│   └── api.py
└── openalpr
│   ├── Dockerfile
│   ├── requirements.txt
    └── recognize.py

```

[_docker-compose.yaml_](docker-compose.yaml)
```
services:
  api:
    build: api
  alpr:
    build: openalpr
    ports:
      - 11300:11300
      - 8355:8355
      - 554:554
  mongo:
    image: mongo
    ports:
      - "27017:27017"
```

## Setup

```
> docker-compose up --detach --build 
> docker exec -it mongodb bash
$ root:/# mongo -u coi -p 1234

> use carsdb
> db.createUser({user: 'alpruser', pwd: '1234', roles: [{role: 'readWrite', db: 'carsdb'}]})
> exit

$ mongo -u alpruser -p 1234 --authenticationDatabase carsdb

> exit

$ exit

docker exec -it alpr bash
python home/recognize.py
```

```
docker-compose build --pull
docker-compose push docker-compose up -d --build
docker exec -i CONTAINER_ID /bin/bash -c "export VAR1=VAL1"
```
