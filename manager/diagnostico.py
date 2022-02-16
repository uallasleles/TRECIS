#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import greenstalk
from pprint import pprint

from database import get_db

db = get_db
HOST_NAMES = ['openalpr', '127.0.0.1']
PORT = 11300
# TUBE_NAME = 'alpr' # alpr

def tubes_list(client):
    # Para diagnóstico, imprima uma lista de todos os tubos disponíveis no Beanstalk.
    return client.tubes()

def items_number(client, TUBE_NAME):
    # Para diagnóstico, imprima o número de itens na fila alprd atual.
    try:
        pprint(client.stats_tube(TUBE_NAME))
    except client.CommandFailed:
        print("Tubo não existe")

def main():
    for HOST_NAME in HOST_NAMES:
        with greenstalk.Client((HOST_NAME, PORT)) as client:
            print("LISTA DE TUBOS: {}".format(tubes_list(client)))
            for TUBE_NAME in tubes_list(client):
                client.use(TUBE_NAME)

                items_number(client, TUBE_NAME)

if __name__=='__main__':
    main()