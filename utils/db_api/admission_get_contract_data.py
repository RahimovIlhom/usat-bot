import warnings
import requests
from environs import Env

env = Env()
env.read_env()

GET_STATUS_APPLICANT = env.str('GET_CONTRACT_DATA_URL')


async def get_contract_data_in_admission(tgId):
    warnings.filterwarnings("ignore", message="Unverified HTTPS request")
    from utils.db_api import get_token
    from loader import db

    active_token_object = await db.get_active_token()
    if active_token_object:
        token = active_token_object[1]
    else:
        token = await get_token()
        await db.add_active_token(token)

    url = GET_STATUS_APPLICANT.format(telegramm_id=tgId)

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers, verify=False)

    try:
        if response.status_code == 401:
            new_token = await get_token()
            headers["Authorization"] = f"Bearer {new_token}"
            await db.add_active_token(new_token)
            resp = requests.get(url, headers=headers, verify=False)
            return resp
        else:
            return response
    except Exception as e:
        return str(e)
