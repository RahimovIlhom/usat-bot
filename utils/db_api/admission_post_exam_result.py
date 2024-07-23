import warnings

import requests
from environs import Env

from utils.db_api import get_token

env = Env()
env.read_env()

SUBMIT_URL = env.str('POST_EXAM_RESULT_URL')


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


async def send_exam_result_for_admission(tgId, ball, examType=True, *args, **kwargs):
    warnings.filterwarnings("ignore", message="Unverified HTTPS request")
    from loader import db
    url = SUBMIT_URL
    active_token = await db.get_active_token()

    data = {
        "id": tgId,
        "ball": ball
    }

    response = await post_request_with_bearer_token(url, data, active_token)
    return response
