from aiogram.types import Message

from filters import IsPrivate
from loader import dp, db


@dp.message_handler(IsPrivate(), text=['🔗 Admin bilan bog\'lanish', '🔗 Связаться с администратором'])
async def contact_admin(msg: Message):
    await msg.answer("Bu funksiya hali ishga tushmadi!")


@dp.message_handler(IsPrivate(), text=['✉️ Universitet ma\'muriyatiga murojaat yuborish',
                                       '✉️ Отправить обращение в ректорат университета'])
async def university_admin(msg: Message):
    await msg.answer("Bu funksiya hali ishga tushmadi!")
