from aiogram import types

from filters import IsPrivate
from keyboards.default import sub_menu_markup_uz, sub_menu_markup_ru
from loader import dp


@dp.message_handler(IsPrivate(), text="ℹ️ Ma'lumotlar")
async def other_information(msg: types.Message):
    await msg.answer(msg.text, reply_markup=sub_menu_markup_uz)


@dp.message_handler(IsPrivate(), text="ℹ️ Информация")
async def other_information(msg: types.Message):
    await msg.answer(msg.text, reply_markup=sub_menu_markup_ru)
