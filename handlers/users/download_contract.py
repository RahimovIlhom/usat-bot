from aiogram.types import Message

from filters import IsPrivate
from loader import dp, db


@dp.message_handler(IsPrivate(), text=['📥 Shartnomani olish', '📥 Получить контракт'])
async def download_contract(msg: Message):
    await msg.answer("Bu funksiya hali ishga tushmadi!")
