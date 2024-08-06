import warnings
import requests
from environs import Env
import base64
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
    else:
        return response


async def send_olympian_result(url, data, token):
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
        requests.post(url, json=data, headers=headers, verify=False)


async def encode_image_to_base64(image_path):
    with open(f"admin/media/{image_path}", 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string


async def submit_applicant_for_admission(applicantId, tgId, firstName, lastName, middleName, applicantNumber, birthDate,
                                         passport, pinfl, phoneNumber, additionalPhoneNumber, directionOfEducationId,
                                         directionOfEducationName, typeOfEducationId, typeOfEducationName,
                                         languageOfEducationId, languageOfEducationName, passportPhotoFront,
                                         passportBackPhoto, regionId, regionName, cityId, cityName, vaucher=None,
                                         certificateImage=None, dtmScore=None, dtmAbiturientNumber=None,  *args, **kwargs):
    warnings.filterwarnings("ignore", message="Unverified HTTPS request")
    from loader import db
    url = SUBMIT_URL.format(telegramm_id=tgId)
    token_tuple = await db.get_active_token()
    active_token = token_tuple[1] if token_tuple else None
    birth_date = birthDate.isoformat() + "T00:00:00Z"

    # Encode images to base64
    passport_photo_base64 = await encode_image_to_base64(passportPhotoFront)
    passport_back_photo_base64 = await encode_image_to_base64(passportBackPhoto)

    data = {
        "id": applicantId,
        "applicantNumber": applicantNumber,
        "firstName": firstName,
        "lastName": lastName,
        "middleName": middleName,
        "birthDate": birth_date,
        "passportNumber": passport,
        "jshir": pinfl,
        "mobilePhone": phoneNumber.replace("+", ""),
        "homePhone": additionalPhoneNumber.replace('+', ''),
        'dtmScore': dtmScore,
        'dtmAbiturientNumber': dtmAbiturientNumber,
        "country": {
            "id": 1,
        },
        "region": {
            "id": regionId,
            "name": regionName
        },
        "city": {
            "id": cityId,
            "name": cityName
        },
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
        "passportPhoto": passport_photo_base64,  # base64
        "passportBackPhoto": passport_back_photo_base64,  # base64
        "needChangePhoto": True,
        "status": "SUBMITTED",  # DRAFT, SUBMITTED
        "typeAbiturient": "ABITURIENT",
        "stage": "COURSE_OF_STUDY"  # REGISTRATION, COURSE_OF_STUDY
    }
    if vaucher:
        data.update({
            "score": f"{vaucher}",
            "certificateNumber": "vaucher"
        })
    elif certificateImage:
        olympiad_data = {
            "id": tgId,
            "telegrammId": tgId,
            "result": "no value",
            "certificateImage": certificateImage
        }
        data.update({
            "certificateNumber": "vaucher"
        })
        await send_olympian_result(OLYMPIAN_RESULT_URL, olympiad_data, active_token)

    response = await post_request_with_bearer_token(url, data, active_token)
    return response
