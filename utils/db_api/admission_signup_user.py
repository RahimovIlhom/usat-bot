import warnings
import requests
from environs import Env
from utils.db_api import get_token

env = Env()
env.read_env()

REGISTER_URL = env.str('USER_REGISTER_URL')


async def signup_applicant(tgId, phoneNumber, passport, birthDate, *args, **kwargs):
    warnings.filterwarnings("ignore", message="Unverified HTTPS request")
    from loader import db
    url = REGISTER_URL
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

    try:
        response = requests.post(url, json=data, headers=headers, verify=False)

        if response.status_code == 401:
            new_token = await get_token()
            headers = {
                "Authorization": new_token,
                "Content-Type": "application/json"
            }
            await db.add_active_token(new_token)
            response = requests.post(url, json=data, headers=headers, verify=False)
            return response
        return response

    except requests.exceptions.RequestException as e:
        return str(e)
