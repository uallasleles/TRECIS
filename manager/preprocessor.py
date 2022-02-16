#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import os
from datetime import datetime
from logging import exception
from sender import Api
from bson.objectid import ObjectId
from  database import get_db
import producer
import asyncio
import base64

db = get_db()

async def del_doc(doc_id, file_name):
    
    try:
        filter = {'_id': ObjectId(doc_id)}
        await db.plate.delete_one(filter=filter)
    except Exception as e:
        exception(e)

    try: 
        path_base = os.environ['ALPR_PATH_IMG'] 
        full_img_dir = ("{}/full_image".format(path_base))
        crop_img_dir = ("{}/crop_image".format(path_base))

        if os.path.isfile(os.path.join(full_img_dir, file_name)):
            await os.remove(os.path.join(full_img_dir, file_name))
            await os.remove(os.path.join(crop_img_dir, file_name))

    except Exception as e:
        exception(e)

def send(doc):
    status = 0
    api = Api(doc['plate']['cam_name'])
    
    try:    
        status = api.send(
            doc['plate']['plate'],
            doc['plate']['datetime'],
            doc['plate']['confidence'],
            doc['plate']['coordinates'][0],
            doc['plate']['coordinates'][1],
            doc['plate']['img_name']
            )
    except:
        exception("message")        
    finally:
        return status

async def get_img64(img_name):
    # LÊ IMAGEM ORIGINAL DO DISCO E CONVERTE PARA BASE64
    pathbase = os.environ['ALPR_PATH_IMG']
    dirlist = ['full_image', 'crop_image']
    img = []
    await asyncio.sleep(0.01)
    for dir in dirlist:
        img_dir = ("{}/{}".format(pathbase, dir))
        filepath = os.path.join(img_dir, img_name)
        if os.path.isfile(filepath):
            await asyncio.sleep(0.01)
            with open(filepath, 'rb') as f:
                img.append(base64.b64encode(f.read()).decode('utf-8'))
    return img

def get_data():
    projection = {
        '_id': True, 
        'plate': True, 
        'epoch_time': True,
        'confidence': True, 
        'coordinates.x': True, 
        'coordinates.y': True, 
        'img_name': True,        
        'cam_name': True
        }

    # print(f"{datetime.now()} - Consultando registros no banco de dados...")
    try:
        collection = db.plate.find({}, projection=projection)
        # print(f"{len(list(collection))} documentos consultados.")
    except Exception as e:
        exception(e)

    return collection

async def preprocessor():
    # await asyncio.sleep(0.1)
    collection = get_data()

    for doc in collection:
        img = []
        file_name = '{}.jpg'.format(doc['img_name'])
        await asyncio.sleep(0.01)
        img = await get_img64(file_name)

        # code = None
        # doc_id = doc['_id']
        # Converte de epoch time para datetime com milisegundos, (ms pois este epoch time possui 13 dígitos)
        doc['datetime'] = datetime.fromtimestamp( doc['epoch_time'] / 1000 ).isoformat(sep=' ', timespec='milliseconds')
            

        try:
            print(f"{datetime.now()} - Enviando dados da {file_name} para a API...")

            data = {
                'camera_id': doc['cam_name'],
                'placa': doc['plate'], 
                'data': doc['datetime'],
                'acuracia': doc['confidence'], 
                'fileName': doc['img_name'],
                'coordenadasXY': {
                    'coord_inicial': doc['coordinates'][0],
                    'coord_final': doc['coordinates'][1]
                    },
                'img64':{
                    'full_img64': img[0],
                    'crop_img64': img[1]
                    }
                }

            await asyncio.sleep(0.01)
            await producer.queue_producer(data)

        except Exception as e:
            exception(e)

        # finally: 
        #     if code == 200:
        #         print(f"{datetime.now()} - Deletando ID: {doc_id} / Placa: {doc['plate']} do banco de dados...")
        #         await del_doc(doc_id, file_name)

if __name__ == "__main__":
    asyncio.run(preprocessor())
