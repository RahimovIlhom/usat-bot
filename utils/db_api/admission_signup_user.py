import aiohttp
from environs import Env

from utils.db_api import get_token

env = Env()
env.read_env()


async def signup_applicant(tgId, phoneNumber, passport, birthDate):
    from loader import db
    url = env.str('USER_REGISTER_URL')
    active_token = await db.get_active_token()
    headers = {
        "Authorization": active_token,
        "Content-Type": "application/json"
    }
    birth_date = birthDate.isoformat()
    data = {
        "telegrammId": tgId,
        "phone": phoneNumber,
        "passportNumber": passport,
        "birthDate": birth_date
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as response:
            if response.status == [201, 400]:
                return response
            elif response.status == 401:
                new_token = await get_token()
                headers = {
                    "Authorization": new_token,
                    "Content-Type": "application/json"
                }
                await db.add_active_token(new_token)
                async with session.post(url, json=data, headers=headers) as resp:
                    return resp
            else:
                return None

# {
#     "code": 499,
#     "meta": {
#         "phone": [
#             "Error. Phone already exist exception"
#         ],
#         "general_errors": [
#             "Pasport raqami allaqachon mavjud"
#         ]
#     }
# }

# {
#     "code": 499,
#     "meta": {
#         "general_errors": [
#             "Pasport raqami allaqachon mavjud"
#         ]
#     }
# }
