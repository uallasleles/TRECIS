#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os
import requests
import cv2
from openalpr import Alpr
from logging import exception
from def_salva import Salva

from argparse import ArgumentParser


parser = ArgumentParser(description='T-Recis programa OCR da WMB')

parser.add_argument("-c", "--country", 
                    dest="country", action="store", 
                    default="br", help="License plate Country" )

parser.add_argument("--config", 
                    dest="config", action="store", 
                    default="/etc/openalpr/openalpr.conf", help="Path to openalpr.conf config file" )

parser.add_argument("--runtime_data", 
                    dest="runtime_data", action="store", 
                    default="/usr/share/openalpr/runtime_data", help="Path to OpenALPR runtime_data directory" )

parser.add_argument("-d", type=int,
                    dest="device_id", action="store", 
                    default="0", required=False, help="[int] Device Id" )

parser.add_argument("-f", type=int,
                    dest="frame_skip", action="store", 
                    default="5", required=False, help="[int] Qtd. fps a processar.Ex:5 processa até 5fps depois skip - DISABLED" )

parser.add_argument("-n", type=int, 
                    dest="top_n", action="store", 
                    default="1", required=False, help="[int] Qtd. de placas retornadas por imagem" )

parser.add_argument("-t", type=int,
                    dest="threads", action="store", 
                    default="1", required = False, help="[int] Nº de threads para processar" )

parser.add_argument("--no-gpu",
                    dest="gpu", action="store_false", 
                    default=False, required=False, help="[flag] Se chamada não roda por GPU e sim por CPU" )

options = parser.parse_args()

FRAME_SKIP = options.frame_skip

# See https://docs.rekor.ai/rekor-scout/scout-agent/nvidia-gpu-acceleration
# GPU processing must use a single Alpr object and single thread per GPU.
# CPU processing may use multiple threads, with one Alpr object/thread per CPU core.
GPU_BATCH_SIZE = 10
GPU_ID = 0

TRACK_VEHICLES_WITHOUT_PLATES = True

RTSP_SOURCE             = os.environ.get('RTSP_SOURCE')
WINDOW_NAME             = 'openalpr'
FRAME_SKIP              = 15


enable_GPU = False

def main():
    print(chr(27) + "[2J") # Limpa a tela no Windows, Mac, Unix
    if(options.gpu):
        print('Executando com\033[92m NVIDIA CUDA\033[0m desabilitando uso de CPU')
        
    alpr = Alpr(options.country, options.config, options.runtime_data)

    if not alpr.is_loaded():
        print('Erro ao carregar OpenALPR')
        sys.exit(1)

    alpr.set_top_n(options.top_n)
    alpr.set_default_region(options.country) #TODO VERIFICAR DEFAULT REGION
    alpr.use_gpu = options.gpu
    alpr.gpu_id = 0
    alpr.motion_detection = 1
    alpr.analysis_threads = options.threads

    cap = cv2.VideoCapture(RTSP_SOURCE)
    if not cap.isOpened():
        alpr.unload()
        sys.exit('Falhou ao abrir o video!')
    
    # cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_AUTOSIZE)
    # cv2.setWindowTitle(WINDOW_NAME, 'OpenALPR video test')

    _frame_number = 5
    while True:
        ret_val, frame = cap.read()
        if not ret_val:
            print('VideoCapture.read() failed. Exiting...')
            break

        _frame_number += 1
        if _frame_number % FRAME_SKIP != 0:
            continue
        # cv2.imshow(WINDOW_NAME, frame)

        results = alpr.recognize_ndarray(frame)
        for i, rs in enumerate(results['results']):
            epoch_time  = results['epoch_time']
            plate       = rs['plate'].upper()
            confidence  = rs['confidence']            

            # TODO sugestão, criar opção em Parser para threshold de confiança
            if confidence > 80 and len(plate) == 7:
                                
                coord_ini_x = 1919 if rs['coordinates'][0]['x'] > 1920 else rs['coordinates'][0]['x']
                coord_ini_y = rs['coordinates'][0]['y']
                coord_fim_x = 1919 if rs['coordinates'][2]['x'] > 1920 else rs['coordinates'][2]['x']
                coord_fim_y = rs['coordinates'][2]['y']
                
                save = Salva(plate)
                img_name = save.SalvaFullImage(frame)
                crop_placa = frame[coord_ini_y:coord_fim_y, coord_ini_x:coord_fim_x]
                save.SalvaCropImage(crop_placa)
                
                # cam_name = options.camera_name
                cam_name = os.environ.get('CAM_NAME')

                # ADD FIELDS IN RESULTS
                rs['cam_name'] = cam_name
                rs['img_name'] = img_name
                rs['epoch_time'] = epoch_time
                
                # ENVIA PARA O BANCO
                res = requests.post('http://webserver:80/plate', json={"plate": rs})
                if res.ok:
                    print(res.json())

        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()
    cap.release()
    alpr.unload()

if __name__ == "__main__":
    main()