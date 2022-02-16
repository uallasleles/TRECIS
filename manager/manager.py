#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import asyncio
from pprint import pprint
import aiohttp
import time
import json
import async_timeout
import greenstalk
import aiostalk
import os
from contextlib import asynccontextmanager

HOST_NAME='127.0.0.1'
PORT=11300
TUBE_NAME='mongo'
TASK_POOL_SIZE=100

# url                 = 'https://webhook.site'
# url_API             = 'https://webhook.site'
# url_Login           = '/c678c35d-9b08-4fff-8a76-016bb3667d80'
# url_SavePlate       = '/c678c35d-9b08-4fff-8a76-016bb3667d80'

url                 = 'https://api.coi.coi-desenvolvimento.com.br'
url_API             = 'https://api.coi.coi-desenvolvimento.com.br'
url_Login           = '/api/Account/Login'
url_SavePlate       = '/api/TRecis/SavePlate?savePhotoDebug=false'
url_GetAllPlate     = '/api/TRecis/GetAllPlate'
url_EraseAllPlate   = '/api/TRecis/EraseAllPlate'

token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InRlc3QifQ.pyNsXX_vNsUvdt6xu13F1Gs1zGELT4Va8a38eG5svBA'

headers = {
    'Accept': '*/*',
    'Content-Type': 'application/json-patch+json',
    'Authorization': f'Bearer {token}'
}

headers2 = {
  'Content-Type': 'application/json',
  'Authorization': f'Bearer {token}',
  'Cookie': '.AspNetCore.Identity.Application=CfDJ8DvckMT-FexCoYaxsNEGCJsnMuL33cMxsJaQltCGE8_hhCBOPmq-zhXZJMdz1oUeqKs1NQ1rLVFtABT66y9A_EwvB3i68xybZaqIbWo_N8OQrfbtWF5S0_K1TbUsTL99-2BtWHZdqNcinCbtgX29jhq2-ieAPBgA3XVqmNtJ_E4ZZvu6ahvuIW9zBlJc4qj_v89N7ViN6hR-hDrnPvb51axvWEgC9_w70wHc5S5t40K7zh-iWAuXhZgmNovKGtgOxGZgaVQJOKI4Qm2SPXT8Lu2S4FFWZB9rju_lEFQFCkxwLv6K9bnXyAM9sVBRacQFWkB9KiFYh96-ZCSbgQyxUkL90gHpcmbFDaFol6Xvw22QnUc5jC-6xoUzRzKq3Ul_ZaMxrtKWMnCt-Q47y48-6Ez--9bBoz_RmXcMWsZ0n3IBrw5mYm9ltPMvVDUGUTCzDpqd5kt3xPj6E8DoR2LKaIqi53vpugwjXK3zKZh_RoXk2Hp4ZW4geRbdjonjf5qs4Cjju4hg2q0uIpD_05x6A7IjxySyTgmtwh996ZI5bt1eNftnjEEXyuf7sQDINaM-SNnYzIuFKpjyWXkEm-vtzvTt-pIvZh34iZhrv_2No-Wbzt3U1ooXQeHdwn-yv9rEGo6c79KjWz_P2p7RM9v5x2qqy5DO4O3yQNGDkyw_V5aX3nMUn93bRCy0nEtG3XEjxYg06pYK3ogRiSTwF_4uIRa_ljbdGfRnIriwOuE_-lzb'
}

data = """{
    "email": "996655@atibaia.sp.gov.br",
    "password": "1234567890"
    }"""

async def send(url, session, headers=headers2, json=json):
    async with session.post(url=url, headers=headers, json=json) as resp:
        resp.raise_for_status()
        return resp.content
    
# Asynchronous Generator Expressions
async def one_at_a_time():
    async with aiostalk.Client((HOST_NAME, PORT), use=TUBE_NAME, watch=TUBE_NAME) as client:
        for _ in range(TASK_POOL_SIZE):
            # await asyncio.sleep(1)
            job = await client.reserve()
            # await asyncio.sleep(0.1)
            await client.delete(job)
            yield job

async def ship(session, url_SavePlate, headers):
    data = [json.loads(job.body) async for job in one_at_a_time()]
    tasks = [asyncio.create_task(send(session=session, url=url_SavePlate, headers=headers, json=json)) for json in data]
    await asyncio.sleep(0.01)
    results = await asyncio.gather(*tasks)
    print(results.text)

async def fetch(session, url_Login, headers, data):
    # async with async_timeout.timeout(10):
    async with session.post(url=url_Login, headers=headers, data=data) as response:
        response.raise_for_status()
        return await response.text

async def main():
    async with aiohttp.ClientSession(base_url=url_API) as session:

        result_fetch = await fetch(session, url_Login, headers, data)
        print(result_fetch)

        result_ship = await ship(session, url_SavePlate, headers)
        print(result_ship)
    
if __name__=='__main__':
    print("==============================================================================")
    print(f"URL base de destino: {url}")
    print(f"Aguardando lote ({TASK_POOL_SIZE}) de jobs em estado pronto para envio ...")
    asyncio.run(main())
