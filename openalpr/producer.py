import greenstalk
import json


def queue_producer(body):
    """Produtor de Fila Beanstalk
    O produtor de fila recebe os resultados da leitura do `recognize_ndarray()` (brutos ou customizados), 
    os formata como JSON, e os insere como jobs numa fila beanstalk.

    Args:
        body ([type: json]): dados de retorno do `recognize_ndarray()` formatados como JSON.
    
    Author: Uallas Leles Pereira
    """    
    
    with greenstalk.Client(('127.0.0.1', 11300), use='alpr', watch='alpr') as client:
        client.put(json.dumps(body))
    
    return print("{}".format(body['img_name']))