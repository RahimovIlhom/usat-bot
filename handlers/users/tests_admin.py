from typing import Union

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from data.config import ADMINS
from filters import IsPrivate
from loader import dp, db


@dp.message_handler(IsPrivate(), text="➕ Yangi test qo'shish", user_id=ADMINS)
async def add_or_set_test(msg: Union[Message, CallbackQuery], state: FSMContext):
    if isinstance(msg, CallbackQuery):
        call = msg
    else:
        await msg.answer("Testning ta'lim yo'nalishini tanlang: ", )