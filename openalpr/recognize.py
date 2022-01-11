# test_camera.py
#
# Open an RTSP stream and feed image frames to 'openalpr'
# for real-time license plate recognition.
# https://gist.github.com/jkjung-avt/790a1410b91c170187f8dbdb8cc698c8

import sys, os
import cv2
from openalpr import Alpr
from def_api import Api
from def_salva import Salva
import requests
from pprint import pprint
import base64

# See https://docs.rekor.ai/rekor-scout/scout-agent/nvidia-gpu-acceleration
# GPU processing must use a single Alpr object and single thread per GPU.
# CPU processing may use multiple threads, with one Alpr object/thread per CPU core.
USE_GPU = False 
GPU_BATCH_SIZE = 10
GPU_ID = 0

TRACK_VEHICLES_WITHOUT_PLATES = True

OPENALPR_CONFIG         = '/etc/openalpr/openalpr.conf'
RUNTIME_DATA_PATH       = '/usr/share/openalpr/runtime_data'
ALPR_COUNTRY            = 'br'

RTSP_SOURCE             = os.environ.get('RTSP_SOURCE')
TEST_VIDEO_FILE_PATH    = '/var/lib/openalpr/videoclips/cars.mp4'
WINDOW_NAME             = 'openalpr'
FRAME_SKIP              = 15

def open_cam_rtsp(uri, width=1280, height=720, latency=2000):
    gst_str = ('rtspsrc location={} latency={} ! '
               'rtph264depay ! h264parse ! omxh264dec ! nvvidconv ! '
               'video/x-raw, width=(int){}, height=(int){}, format=(string)BGRx ! '
               'videoconvert ! appsink max-buffers=5').format(uri, latency, width, height)
    return cv2.VideoCapture(RTSP_SOURCE)
    # return cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)

enable_GPU = False

def main():
    
    # api = Api(options.camera_name)
    api = Api('camera_name_test')
    # gps = Gps()
    
    # Initialize instances
    alpr = Alpr(ALPR_COUNTRY, OPENALPR_CONFIG, RUNTIME_DATA_PATH)
    if not alpr.is_loaded():
        print('Error loading OpenALPR')
        sys.exit(1)

    alpr.set_top_n(3) # Configuração dos Top N Candidatos Retornados
    #alpr.set_default_region('new')

    cap = open_cam_rtsp(RTSP_SOURCE)
    
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
        img64 = base64.b64encode(frame).decode('utf-8')

            #TODO pegar threshold de confiança de arquivo de configuração
            # if confidence > 80 and len(plate) == 7:
            #     save = Salva(plate)
            #     img_name = save.SalvaFullImage(frame)
            #     crop_placa = frame[coord_ini_y:coord_fim_y, coord_ini_x:coord_fim_x]
            #     save.SalvaCropImage(crop_placa)
            #     gps_lat = None
            #     gps_log = None
            #     gps_qual = None

            #     # ENVIAR PARA A API
            #     api.send(
            #         plate,
            #         confidence,
            #         '{},{}'.format(coord_ini_x, coord_ini_y), 
            #         '{},{}'.format(coord_fim_x, coord_fim_y),
            #         gps_lat, 
            #         gps_log,
            #         gps_qual, 
            #         img_name,
            #     )

                # res = requests.post('http://webserver:80/plate', json={"plate": results})

                # if res.ok:
                #     print(res.json())

        for i, plate in enumerate(results['results']):
            
            # PEGA DOIS VALORES PARA VALIDAÇÃO
            best_candidate = plate['candidates'][0]
            placa = best_candidate['plate'].upper()
            
            # VALIDA
            if best_candidate['confidence'] > 80 and len(placa) == 7:
                
                # ENVIA PARA A API
                res = requests.post('http://webserver:80/plate', json={"plate": results})
                if res.ok:
                    print(res.json())

        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()
    cap.release()
    alpr.unload()

if __name__ == "__main__":
    main()