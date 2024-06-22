import aiohttp
from environs import Env

env = Env()
env.read_env()

GET_STATUS_APPLICANT = env.str('GET_APPLICATION_URL')


async def get_application_status_from_api(pinfl):
    from utils.db_api import get_token
    from loader import db
    active_token = await db.get_active_token()
    url = f"{GET_STATUS_APPLICANT}?pinfl={pinfl}"
    headers = {"Authorization": f"Bearer {active_token}"}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            elif response.status == 401:
                active_token = await get_token()
                await db.add_active_token(active_token)
                headers = {"Authorization": f"Bearer {active_token}"}
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        return await response.json()
                    return None
            else:
                return None
