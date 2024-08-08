from typing import Union

import aiohttp
from io import BytesIO


async def contract_file_link(fullname: str, contract_file_path: str) -> Union[None, str]:
    with open(contract_file_path, 'rb') as f:
        file = BytesIO(f.read())

    file.seek(0)

    form = aiohttp.FormData()
    form.add_field(
        name=fullname,
        value=file,
        filename=fullname,
        content_type='application/octet-stream'
    )

    async with aiohttp.ClientSession() as session:
        async with session.post('https://telegra.ph/upload', data=form) as response:
            resp = await response.json()
            print(resp)

    if 'src' in resp[0]:
        link = 'http://telegra.ph/' + resp[0]["src"]
        return link
    else:
        return None
