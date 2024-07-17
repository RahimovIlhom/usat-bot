import base64
import warnings

import aiohttp
import requests
from environs import Env

from utils.db_api import get_token

env = Env()
env.read_env()

SUBMIT_URL = env.str('SUBMIT_APPLICATION_URL')
OLYMPIAN_RESULT_URL = env.str('OLYMPIAN_RESULT_URL')


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


async def encode_image_to_base64(image_path):
    with open(f"admin/media/{image_path}", 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string


async def send_exam_result_for_admission(tgId, ball, examType=True, *args, **kwargs):
    warnings.filterwarnings("ignore", message="Unverified HTTPS request")
    from loader import db
    url = SUBMIT_URL.format(telegramm_id=tgId)
    active_token = await db.get_active_token()
    applicant = await db.get_applicant_for_post_exam_result(tgId)

    if not applicant:
        return {
            'status': 'error',
            'message': 'Applicant not found'
        }

    birth_date = applicant['birthDate'].isoformat() + "T00:00:00Z"
    languageOfEducationId = 1 if applicant['languageOfEducation'] == 'uz' else 2

    data = {
        "firstName": applicant['firstName'],
        "lastName": applicant['lastName'],
        "middleName": applicant['middleName'],
        "applicantNumber": applicant['applicantNumber'],
        "birthDate": birth_date,
        "gender": applicant['gender'],
        "passportNumber": applicant['passport'],
        "jshir": applicant['pinfl'],
        "mobilePhone": applicant['additionalPhoneNumber'].replace("+", ""),
        "homePhone": applicant['phoneNumber'].replace("+", ""),
        "region": {
            "id": applicant['regionId'],
            "name": applicant['regionName']
        },
        "city": {
            "id": applicant['cityId'],
            "name": applicant['cityName']
        },
        "educationType": {
            "id": applicant['typeOfEducation_id'],
            "name": applicant['typeOfEducationName']
        },
        "educationLanguage": {
            "id": languageOfEducationId,
            "name": applicant['languageOfEducation']
        },
        "educationFaculty": {
            "id": applicant['directionOfEducation_id'],
            "name": applicant['directionOfEducationName']
        },
        "passportPhoto": encode_image_to_base64(applicant['passportPhotoFront']),  # base64
        "passportBackPhoto": encode_image_to_base64(applicant['passportPhotoBack']),  # base64
        "ball": ball,
        "examType": examType,
        "photo": applicant['photo'],
        "status": "EXAMINED",
        "typeAbiturient": "ABITURIENT",
    }
    if applicant.get('vaucher'):
        data.update({
            "score": f"{applicant['vaucher']}",
            "certificateNumber": "vaucher"
        })

    response = await post_request_with_bearer_token(url, data, active_token)
    return response
