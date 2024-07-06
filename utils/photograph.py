from io import BytesIO
import aiohttp
from aiogram import types


async def certificate_photo_link(photo: types.photo_size.PhotoSize) -> str:
    from loader import bot
    destination = BytesIO()
    await photo.download(destination_file=destination)

    form = aiohttp.FormData()
    form.add_field(
        name='file',
        value=destination.getvalue(),
        content_type='multipart/form-data',
        filename='photo.jpg'
    )

    session = await bot.get_session()
    async with session.post('https://telegra.ph/upload', data=form) as response:
        img_src = await response.json()

    link = 'http://telegra.ph/' + img_src[0]["src"]
    return link
