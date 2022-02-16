import cv2
import datetime
import logging
import sys
import os

# path_base = "{}/trecis/webapp/images".format(os.environ['HOME'])
path_base = "/var/lib/openalpr/plateimages"

class Salva(object):
    nome_file = ""

    def __init__(self, placa):
        self.__placa = placa
        self.nome_file = nome(self.__placa)

    def SalvaFullImage(self, imagem):
        try:
            if self.__placa and imagem.any():
                newimage = cv2.resize(imagem, (640, 360))
                path_img = ("{}/full_image/{}.jpg".format(path_base, self.nome_file))
                if not cv2.imwrite(path_img, newimage, [int(cv2.IMWRITE_JPEG_QUALITY), 45]):
                    raise Exception("Could not write image")
                return self.nome_file

        except OSError as err:
            logging.exception("message")
            return None

        except:
            logging.exception("message")
            return None

    def SalvaCropImage(self, imagemCrop):
        try:
            if self.__placa and imagemCrop.any():
                path_img = ("{}/crop_image/{}.jpg".format(path_base, self.nome_file))
                if not cv2.imwrite(path_img, imagemCrop, [int(cv2.IMWRITE_JPEG_QUALITY), 70]):
                    raise Exception("Could not write image")
                return self.nome_file
        except OSError as err:
            logging.exception("message")
            return None
        except:
            logging.exception("message")
            return None


def nome(placa):    
    timestr = datetime.datetime.now().strftime('%Y%m%d-%H%M%S.%f')[:-3]
    return "{}_{}".format(timestr, placa)

