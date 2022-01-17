import os
import base64
from datetime import datetime
from logging import exception
from time import time, sleep
from send2api import Api
from bson import json_util
from bson.objectid import ObjectId
import json
import database_connection
import internet_connection

db = database_connection.get_db()

def del_doc(doc_id, file_name):
    
    try:
        filter = {'_id': ObjectId(doc_id)}
        db.plate.delete_one(filter=filter)
    except Exception as e:
        exception(e)

    try:
        print("Removendo arquivo de imagem do disco local ...")

        path_base = "/var/lib/openalpr/plateimages"            
        full_img_dir = ("{}/full_image".format(path_base))
        crop_img_dir = ("{}/crop_image".format(path_base))

        if os.path.isfile(os.path.join(full_img_dir, file_name)):
            os.remove(os.path.join(full_img_dir, file_name))
            os.remove(os.path.join(crop_img_dir, file_name))

    except Exception as e:
        exception(e)

def send(doc):    
    api = Api(doc['plate']['cam_name'])
    
    try:    
        status = api.send(
            doc['plate']['plate'],
            doc['plate']['confidence'],
            doc['plate']['coordinates'][0],
            doc['plate']['coordinates'][1],
            doc['plate']['gps_lat'],
            doc['plate']['gps_log'],
            doc['plate']['gps_qual'],
            doc['plate']['img_name']
            )
    except:
        exception("message")        
    finally:
        return status

def cleansing():    
    projection = {
        '_id': True, 
        'plate.plate': True, 
        'plate.confidence': True, 
        'plate.coordinates.x': True, 
        'plate.coordinates.y': True, 
        'plate.gps_lat': True, 
        'plate.gps_log': True, 
        'plate.gps_qual': True, 
        'plate.img_name': True,        
        'plate.cam_name': True
        }
    
    try:
        print(f"{datetime.now()} - Buscando novo reconhecimento de placa...")
        rs = db.plate.find({}, projection=projection)
    except Exception as e:
        exception(e)
    
    for i in rs:
        code = None
        doc_id = i['_id']
        file_name = '{}.jpg'.format(i['plate']['img_name'])
        
        if internet_connection.internet_connection_test() == True:
            try:
                print(f"{datetime.now()} - Enviando dados da placa para a API...")
                code = send(i)
            except Exception as e:
                exception(e)
            finally: 
                if code == 200:
                    print(f"{datetime.now()} - Deletando registro do banco de dados...")
                    del_doc(doc_id, file_name)
            sleep(1)

if __name__ == "__main__":    
    cleansing()

