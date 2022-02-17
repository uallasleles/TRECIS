#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import asyncio
from pprint import pprint
import aiohttp
import requests
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
TASK_POOL_SIZE=10

# url                 = 'https://webhook.site'
# url_API             = 'https://webhook.site'
# url_Login           = '/c678c35d-9b08-4fff-8a76-016bb3667d80'
# url_SavePlate       = '/c678c35d-9b08-4fff-8a76-016bb3667d80'

url                 = 'https://api.coi.coi-desenvolvimento.com.br'
url_API             = 'https://api.coi.coi-desenvolvimento.com.br'
url_Login           = 'https://api.coi.coi-desenvolvimento.com.br/api/Account/Login'
url_SavePlate       = '/api/TRecis/SavePlate?savePhotoDebug=false'
url_GetAllPlate     = '/api/TRecis/GetAllPlate'
url_EraseAllPlate   = '/api/TRecis/EraseAllPlate'

username = "996655@atibaia.sp.gov.br"
password = "1234567890"
auth = aiohttp.BasicAuth(login=username, password=password)

headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Basic OTk2NjU1QGF0aWJhaWEuc3AuZ292LmJyOjEyMzQ1Njc4OTA=',
  'Cookie': '.AspNetCore.Identity.Application=CfDJ8NbjMtpvc5dGhHZNlSCV4wCN9-SfrEPWvMqsg6RV6SLnl5D-QuJ1U0pkxUiUFgnsLwAyTKQOfKqAiXFWwK7kiuZS9xgKc1JzjL9NOh0O0h9uT7L9bdtXvulHGW4OYVJYaW4zk8gtJ3i11z405KXfT8Po_FweqvFo7YyrZRJVdR108IAudumbWwJQbY6Ds7y1_eDlG_bNJjT8aDxPo7AbTz9hMlX0iZ_jGyNKBy68P0g6CTH8QZIAfqUS_aXCikI-On7c8qgcrlnvnTm4N4pOnsbpsIr5VZ3eRMgsaTL27_kRAkQZ4FKNkfahfAgU0Zitkrw36tli5NuCdB5K8a56lU4LrlgGxOMaTwGNJdACN77ELBd-MJhwVg6oUbUEDXDY27MJNk0UoHxQk_75keBSZN4fhzRqXPyFsusnBOuKGr0c5PtNzNuQTyyZ91JM1TyfLEPT2IoGonBnQfEGBE6c7Tcw-HKP8MhTjRdpwwfIv4EOjT6NShkMMQAzkb24KA7rMqw3BqSbcra3Zbj69yak1UvvzZt2SZcSN6uvRaF7BD5lI_yomwvXyY9jUIKokcoo5gjfAOQ6-gadp8ZGvPxf6pJ4kvk3MHCHiYA8FOUei0USdNbP9NY0waM8gRGYu1gSo34kYKv1aFUNkA_6Fp5-tcsmykubshOpnGDwo7LKD55I4nTbQjusdhQZY_pUmeGNSjXJaHVn1yG3U0bvIy8eE4A_-LA0DFwq9X8Yols3vRlS'
}

payload = json.dumps({
  "email": "996655@atibaia.sp.gov.br",
  "password": 1234567890
})

async def send(session, url, headers, data):
    async with session.post(url, headers=headers, data=data) as resp:
        # [ resp.raise_for_status() ] object NoneType can't be used in 'await' expression
        resp.raise_for_status()
        # [ resp ]        object ClientResponse can't be used in 'await' expression
        # [ resp.text ]   object method can't be used in 'await' expression
        async for data, _ in resp.content.iter_chunks():
            return data
    
# Asynchronous Generator Expressions
async def one_at_a_time():
    async with aiostalk.Client((HOST_NAME, PORT), use=TUBE_NAME, watch=TUBE_NAME) as client:
        for _ in range(TASK_POOL_SIZE):
            await asyncio.sleep(1)
            job = await client.reserve()
            await asyncio.sleep(0.1)
            await client.delete(job)
            yield job

async def ship(session, url_SavePlate, headers):
    dados = [job.body async for job in one_at_a_time()]
    tasks = [asyncio.create_task(send(session=session, headers=headers, url=url_SavePlate, data=json)) for json in dados]
    await asyncio.sleep(0.1)
    results = await asyncio.gather(*tasks)
    return(results)

def fetch(url_Login, headers, payload):
    with requests.request("POST", url=url_Login, headers=headers, data=payload) as response:
        response.raise_for_status()
        return response.content

async def main():
    async with aiohttp.ClientSession(base_url=url_API) as session:

        token = fetch(url_Login, headers, payload)

        if token:
            headers2 = {
                'Accept': '*/*',
                'Authorization': f"Bearer {token}",
                'Content-Type': 'application/json'
            }
            await asyncio.sleep(0.1)
            result_ship = await ship(session, url_SavePlate, headers=headers2)
            print(result_ship)
    
if __name__=='__main__':
    print("==============================================================================")
    print(f"URL base: {url}")
    print(f"Aguardando lote ({TASK_POOL_SIZE}) de jobs em estado pronto para envio ...")
    asyncio.run(main())
