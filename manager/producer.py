#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import json
import asyncio
import aiostalk

async def queue_producer(body):
    """Produtor de Fila Beanstalk
    O produtor de fila recebe registros do banco de dados (brutos ou customizados), 
    os formata como JSON, e os insere como jobs numa fila beanstalk.

    Args:
        body ([type: json]): registros do banco de dados formatados como JSON.
    
    Author: Uallas Leles Pereira
    """    
    
    async with aiostalk.Client(('127.0.0.1', 11300), use='mongo') as client:
        await asyncio.sleep(0.01)
        await client.put(json.dumps(body))