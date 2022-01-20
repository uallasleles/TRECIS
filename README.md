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


Limpa a tela no Windows, Mac, Unix
```python
print(chr(27) + "[2J")
```

`chr(27)`é o mesmo `\x1b` que o caractere de controle ASCII “Escape”
.

chr(27) + "[2J"é o mesmo que a string '\x1b[2J'que é uma sequência de escape ANSI
para limpar a janela do terminal.

Isso significa que seu terminal, ou console, se entender
as sequências de escape ANSI (nem todos os terminais o fazem), detectará quando você imprimir essa
string mágica e limpará a janela.

Se você estiver usando o IDLE ou outro IDE, provavelmente não funcionará. Mas se
você estiver usando o terminal ou console do seu sistema operacional,
provavelmente limpará a tela.

Este não é um recurso do Python, depende inteiramente do terminal ou
console em que você está executando. Se o terminal suportar códigos de escape ANSI,
ele limpará a tela, caso contrário, provavelmente imprimirá apenas um espaço
e, em seguida, [2J.

cores ANSI (Python)