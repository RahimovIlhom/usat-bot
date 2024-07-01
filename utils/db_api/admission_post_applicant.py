import aiohttp
import asyncio
from environs import Env

from utils.db_api import get_token

env = Env()
env.read_env()

url = env.str('SUBMIT_APPLICATION_URL')
print(url.format('1234567'))


async def post_request_with_bearer_token(url, data, token):
    from loader import db
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as response:
            if response.status == 200:
                return response
            elif response.status == 401:
                active_token = await get_token()
                await db.add_active_token(active_token)
                headers = {"Authorization": f"Bearer {active_token}"}
                async with session.get(url, headers=headers) as resp:
                    if resp.status == 200:
                        return resp
                    return None
            else:
                return None


async def submit_applicant(tgId, firstName, lastName, middleName, phoneNumber, birthDate, gender, nationality, passport,
                           pinfl, additionalPhoneNumber, directionOfEducationId, directionOfEducationName,
                           typeOfEducationId, typeOfEducationName, languageOfEducationId, languageOfEducationName,
                           photo=None, *args, **kwargs):
    from loader import db
    url = env.str('SUBMIT_APPLICATION_URL')
    active_token = await db.get_active_token()
    data = {
        "firstName": firstName,
        "lastName": lastName,
        "middleName": middleName,
        "applicantNumber": phoneNumber,
        "birthDate": birthDate,
        "gender": gender,
        "nationality": nationality,
        "passportNumber": passport,
        "jshir": pinfl,
        "homePhone": additionalPhoneNumber,
        "educationType": {
            "id": typeOfEducationId,
            "name": typeOfEducationName
        },
        "educationLanguage": {
            "id": languageOfEducationId,
            "name": languageOfEducationName
        },
        "educationFaculty": {
            "id": directionOfEducationId,
            "name": directionOfEducationName
        },
        "photo": photo,
        "status": "SUBMITTED",
        "typeAbiturient": "ABITURIENT",
    }

    response = await post_request_with_bearer_token(url, data, active_token)
    print(response.status)
    print(response)


if __name__ == "__main__":
    pass
    # asyncio.run(submit_applicant("Ilxomjon", "Raximov", "Nikolaevich", "+998909090909", "1990-01-01", "MALE",
    # "UZBEK", "AA1234567", "12345678912345", "+998916589340", 1, "Turizm", 1, "Kunduzgi ta'lim", 1, "uz"))
