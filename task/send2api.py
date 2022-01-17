import requests
import datetime
import json
import base64
import os
import os.path
import sys
import logging


class Api(object):

    def __init__(self, camera_id):
        self.__camera_id = camera_id

    def send(self, placa, acuracia, coord_inicio, coord_final, gps_lat, gps_log, gps_qual, file_name):
        try:
            self.__placa        = placa
            self.__gps_lat      = gps_lat
            self.__gps_log      = gps_log
            self.__gps_qual     = gps_qual
            self.__acuracia     = acuracia
            self.__coord_i      = coord_inicio
            self.__coord_f      = coord_final
            self.__file_name    = '{}.jpg'.format(file_name)

            headers = {'Content-type': 'application/json'}

            url_endpoint = os.environ['URL_ENDPOINT']        

            # // versão 2
            full_img64 = ""
            crop_img64 = ""
            
            # TODO buscar image_path do arquivo de configuração

            # path_base = "{}/data/openalpr/plateimages".format(os.environ['HOME'])
            path_base = "/var/lib/openalpr/plateimages"            
            
            # LÊ IMAGEM ORIGINAL DO DISCO E CONVERTE PARA BASE64
            full_img_dir = ("{}/full_image".format(path_base))
            if os.path.isfile(os.path.join(full_img_dir, self.__file_name)):
                imgfull = open(os.path.join(full_img_dir, self.__file_name), 'rb').read()
                full_img64 = base64.b64encode(imgfull).decode('utf-8')

            # LÊ IMAGEM THUMB DO DISCO E CONVERTE PARA BASE64
            crop_img_dir = ("{}/crop_image".format(path_base))
            if os.path.isfile(os.path.join(crop_img_dir, self.__file_name)):
                imgcrop = open(os.path.join(crop_img_dir, self.__file_name), 'rb').read()
                crop_img64 = base64.b64encode(imgcrop).decode('utf-8')

            data = {
                'camera_id': self.__camera_id,
                'placa': self.__placa,
                'data':  datetime.datetime.now(),
                'acuracia': self.__acuracia,
                'fileName': self.__file_name,
                'gps': {
                    "latitude": self.__gps_lat,
                    "logitude": self.__gps_log,
                    "quality": self.__gps_qual
                },
                'coordenadasXY': {
                    'coord_inicial': self.__coord_i,
                    'coord_final': self.__coord_f
                },
                'img64':{
                    'full_img64': full_img64,
                    'crop_img64': crop_img64,
                },
            }

            r = requests.post(
                url_endpoint, 
                data=json.dumps(data, default = myconverter), 
                headers=headers
                )
            print(json.dumps(data, default = myconverter))

            print(r.status_code, r.reason, r.content)
            return r.status_code
            # print(r.text)

        except OSError as err:
            logging.exception("message")
            # erro.grava("OS error: {0}".format(err))
            # print("OS error: {0}".format(err))

        except:
            logging.exception("message")
            # print("Erro: ", sys.exc_info()[0])
            # erro.grava("Erro: {0}".format(sys.exc_info()[0]))

def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()