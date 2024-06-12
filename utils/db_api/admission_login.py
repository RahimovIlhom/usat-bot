import asyncio

import aiohttp
import warnings
from environs import Env

env = Env()
env.read_env()

CREATE_TOKEN_URL = env.str("CREATE_TOKEN_URL")
ADMISSION_USERNAME = env.str('ADMISSION_USERNAME')
ADMISSION_PASSWORD = env.str('ADMISSION_PASSWORD')


async def get_token():
    warnings.filterwarnings("ignore", message="Unverified HTTPS request")

    user_login = {
        "username": ADMISSION_USERNAME,
        "password": ADMISSION_PASSWORD
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(CREATE_TOKEN_URL, json=user_login, verify_ssl=False) as resp:
            resp_json = await resp.json()
            return resp_json['token']


# async def main():
#     resp = await get_token()
#     print(resp)
#
#
# asyncio.run(main())
