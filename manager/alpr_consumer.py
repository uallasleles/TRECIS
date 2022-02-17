#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import greenstalk
import aiostalk
import asyncio
import json
from database import get_db
from logging import exception

db = get_db()
TUBE_NAME='alpr'

async def add_document(data):
    # await asyncio.sleep(0.1)
    db.plate.insert_one(data)

async def queue_consumer():
    """Consumidor de Fila Beanstalk
    O Consumidor de Fila escuta uma fila beanstalk em um determinado tubo, obtem um job desta fila e executa um processo. 
    Após a execução do processo o job é removido da fila e uma nova escuta é realizada.

    Author: Uallas Leles Pereira
    """    
    async with aiostalk.Client(('openalpr', 11300), use=TUBE_NAME, watch=TUBE_NAME) as client:
        while True:
            # Espere um segundo para conseguir um job. Se houver um job, processe-o e exclua-o da fila.
            # Se não, volte a aguardar.
            # await asyncio.sleep(0.1)
            job = await client.reserve()

            if job is None:
                print("Sem placas disponíveis no momento, aguardando...")
            else:
                print("Encontrou uma placa!")
                results = json.loads(job.body)
                print(results)

                print("Job ID: {} Plate: {}".format(job.id, results['plate'].upper()))
                await asyncio.sleep(0.01)
                await add_document(results)
                
                # FUTURAMENTE PRETENDO FAZER ESSA VERIFICAÇÃO
                # if 'data_type' not in plate_data:
                #     print("Isso não deveria estar aqui... todos os dados do OpenALPR devem ter um data_type")
                # elif plate_data['data_type'] == 'alpr_results':
                #     print("Este é um resultado de placa")
                # elif plate_data['data_type'] == 'alpr_group':
                #     print("Este é um resultado do grupo")
                # elif plate_data['data_type'] == 'heartbeat':
                #     print("Este é um heartbeat")  
                # app.add_document(plate_data)

                await asyncio.sleep(0.01)
                await client.delete(job)

if __name__ == "__main__":
    asyncio.run(queue_consumer())