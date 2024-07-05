import warnings
import requests
from environs import Env
from utils.db_api import get_token

env = Env()
env.read_env()

USER_UPDATE_URL = env.str('USER_UPDATE_URL')


async def update_profile_applicant(tgId, phoneNumber, passport, birthDate, *args, **kwargs):
    warnings.filterwarnings("ignore", message="Unverified HTTPS request")
    from loader import db
    url = USER_UPDATE_URL.format(telegrammId=tgId)
    active_token_object = await db.get_active_token()
    if active_token_object:
        token = active_token_object[1]
    else:
        token = await get_token()
        await db.add_active_token(token)
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }

    # birthDate to ISO 8601 format with time
    birth_date = birthDate.isoformat() + "T00:00:00Z"
    data = {
        "telegrammId": tgId,
        "phone": phoneNumber.replace("+", ""),
        "passportNumber": passport,
        "birthDate": birth_date
    }

    response = requests.put(url, json=data, headers=headers, verify=False)

    if response.status_code in [201, 400]:
        return response
    elif response.status_code == 401:
        new_token = await get_token()
        headers = {
            "Authorization": new_token,
            "Content-Type": "application/json"
        }
        await db.add_active_token(new_token)
        resp = requests.put(url, json=data, headers=headers, verify=False)
        return resp
    else:
        return None
