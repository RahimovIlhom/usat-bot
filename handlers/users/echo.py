from aiogram import types
from aiogram.utils.exceptions import MessageCantBeDeleted

from data.config import ADMINS
from filters import IsPrivate
from keyboards.default import admin_menu_markup_uz, menu_markup_uz, menu_markup_ru, exams_menu_markup, \
    sub_menu_markup_uz, sub_menu_markup_ru
from keyboards.inline import application_callback_data
from loader import dp, db, db_olympian
from utils.misc.send_photo_telegraph import question_photo_link


@dp.message_handler(IsPrivate(), state=None, text="◀️ Orqaga", user_id=ADMINS)
async def bot_echo(message: types.Message):
    await message.answer("Menu", reply_markup=admin_menu_markup_uz)


@dp.message_handler(IsPrivate(), state=None, text="⬅️ Orqaga", user_id=ADMINS)
async def bot_echo(message: types.Message):
    await message.answer("📚 Imtihon bo'limi", reply_markup=exams_menu_markup)


@dp.message_handler(IsPrivate(), state=None, text=["⬅️ Orqaga", "⬅️ Назад"])
async def bot_echo(message: types.Message):
    lang = 'uz' if message.text == "⬅️ Orqaga" else 'ru'
    text = "ℹ️ Ma'lumotlar" if lang == 'uz' else "ℹ️ Информация"
    await message.answer(text, reply_markup=sub_menu_markup_uz if lang == 'uz' else sub_menu_markup_ru)


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
    if message.text == 'test_olympian_user_ilhomjon':
        applicant = await db.get_applicant(message.from_user.id)
        await message.answer(f"{await db_olympian.get_olympian(message.from_user.id, applicant[3])}")
    await message.answer(message.text)


# @dp.message_handler(IsPrivate(), state=None, content_types=types.ContentTypes.PHOTO)
# async def bot_echo(message: types.Message):
#     photo_link = await question_photo_link(message.photo[-1])
#     await message.answer(photo_link)


@dp.callback_query_handler(application_callback_data.filter(), state=None)
async def delete_call_message_application(call: types.CallbackQuery):
    try:
        await call.message.delete()
    except MessageCantBeDeleted:
        await call.message.edit_reply_markup(None)


@dp.callback_query_handler(state=None)
async def delete_call_message(call: types.CallbackQuery):
    try:
        await call.message.delete()
    except MessageCantBeDeleted:
        await call.message.edit_reply_markup(None)
