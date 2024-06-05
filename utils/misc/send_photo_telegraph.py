import aiohttp
from aiogram import types
from io import BytesIO


async def question_photo_link(photo: types.photo_size.PhotoSize) -> str:
    from loader import bot

    file = BytesIO()
    await photo.download(destination_file=file)
    file.seek(0)

    form = aiohttp.FormData()
    form.add_field(
        name='file',
        value=file,
        content_type='multipart/form-data'
    )

    session = await bot.get_session()
    async with session.post('https://telegra.ph/upload', data=form) as response:
        img_src = await response.json()

    link = 'http://telegra.ph/' + img_src[0]["src"]
    return link
