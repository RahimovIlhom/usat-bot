from aiogram import types

from data.config import ADMINS
from filters import IsPrivate
from keyboards.default import admin_menu_markup_uz, menu_markup_uz, menu_markup_ru, exams_menu_markup
from keyboards.inline import application_callback_data
from loader import dp, db


@dp.message_handler(IsPrivate(), state=None, text="◀️ Orqaga", user_id=ADMINS)
async def bot_echo(message: types.Message):
    await message.answer("Menu", reply_markup=admin_menu_markup_uz)


@dp.message_handler(IsPrivate(), state=None, text="⬅️ Orqaga", user_id=ADMINS)
async def bot_echo(message: types.Message):
    await message.answer("📚 Imtihon bo'limi", reply_markup=exams_menu_markup)


@dp.message_handler(IsPrivate(), state=None, text=["◀️ Orqaga", "◀️ Назад"])
async def bot_echo(message: types.Message):
    simple_user = await db.select_simple_user(message.from_user.id)
    if simple_user:
        if simple_user[2] == 'uz':
            await message.answer("Bosh menyu:", reply_markup=menu_markup_uz)
        else:
            await message.answer("Главное меню:", reply_markup=menu_markup_ru)


@dp.message_handler(IsPrivate(), state=None)
async def bot_echo(message: types.Message):
    await message.answer(message.text)


@dp.callback_query_handler(application_callback_data.filter(), state=None)
async def delete_call_message_application(call: types.CallbackQuery):
    await call.message.delete()


@dp.callback_query_handler(state=None)
async def delete_call_message(call: types.CallbackQuery):
    await call.message.delete()
