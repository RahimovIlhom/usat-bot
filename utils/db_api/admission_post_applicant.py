import warnings

import aiohttp
import requests
from environs import Env

from utils.db_api import get_token

env = Env()
env.read_env()

SUBMIT_URL = env.str('SUBMIT_APPLICATION_URL')


async def post_request_with_bearer_token(url, data, token):
    from loader import db
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    response = requests.post(url, json=data, headers=headers, verify=False)
    if response.status_code == 401:
        new_token = await get_token()
        headers["Authorization"] = f"Bearer {new_token}"
        await db.add_active_token(new_token)
        resp = requests.post(url, json=data, headers=headers, verify=False)
        return resp


async def submit_applicant_for_admission(tgId, firstName, lastName, middleName, applicantNumber, birthDate, gender,
                                         passport, pinfl, additionalPhoneNumber, directionOfEducationId,
                                         directionOfEducationName, typeOfEducationId, typeOfEducationName,
                                         languageOfEducationId, languageOfEducationName, photo=None, *args, **kwargs):
    warnings.filterwarnings("ignore", message="Unverified HTTPS request")
    from loader import db
    url = SUBMIT_URL.format(telegramm_id=tgId)
    active_token = await db.get_active_token()
    birth_date = birthDate.isoformat() + "T00:00:00Z"
    data = {
        "firstName": firstName,
        "lastName": lastName,
        "middleName": middleName,
        "applicantNumber": applicantNumber,
        "birthDate": birth_date,
        "gender": gender,
        "passportNumber": passport,
        "jshir": pinfl,
        "mobilePhone": additionalPhoneNumber.replace("+", ""),
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
        "stage": "COURSE_OF_STUDY"
    }

    response = await post_request_with_bearer_token(url, data, active_token)
    return response


if __name__ == "__main__":
    pass
    # asyncio.run(submit_applicant('1234567', "Ilxomjon", "Raximov", "Nikolaevich", "+998909090909", "1990-01-01",
    # "MALE", "UZBEK", "AA1234567", "12345678912345", "+998916589340", 1, "Turizm", 1, "Kunduzgi ta'lim", 1, "uz"))
