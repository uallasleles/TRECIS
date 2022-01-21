import os
import requests
from requests.exceptions import HTTPError
from requests.exceptions import ConnectionError
 
 
def internet_connection_test(url):
    """
    Verifique a conectividade com a Internet
    """
 
    try:        
        response = requests.get(url, headers={'Accept': 'application/json; charset=utf8'})
        response.raise_for_status()

        # response.status_code
        # response.headers['content-type']
        # response.encoding
        # response.text
        # response.json()        
        
    except HTTPError as http_err:
        print(f'Ocorreu um erro HTTP: {http_err}')  # Python 3.6
        return False
    except Exception as err:
        print(f'Ocorreu outro erro: {err}')  # Python 3.6
        return False
    else:        
        return True