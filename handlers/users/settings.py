import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from data.config import ADMINS
from filters import IsPrivate
from keyboards.default import language_markup, settings_markup_uz, settings_markup_ru
from loader import dp, db
from states import SimpleRegisterStates, TestExecutionStates


@dp.message_handler(IsPrivate(), Command('set_lang'), state='*', user_id=ADMINS)
async def set_language(msg: types.Message):
    await msg.answer("Bu buyruq admin uchun emas!")


@dp.message_handler(IsPrivate(), text=["🌐 Tilni o'zgartirish", "🌐 Изменение языка"])
@dp.message_handler(IsPrivate(), Command('set_lang'), state='*')
async def set_language(msg: types.Message, state: FSMContext):
    simple_user = await db.select_simple_user(msg.from_user.id)
    if await state.get_state() == TestExecutionStates.science.state:
        await msg.delete()
        if simple_user[2] == 'uz':
            msg_to_del = await msg.answer("‼️ Imtihon vaqtida hech qanday buyruq ishlamaydi!")
        else:
            msg_to_del = await msg.answer("‼️ Во время экзамена никакие команды не работают!")
        await asyncio.sleep(2)
        await msg_to_del.delete()
        return
    if simple_user:
        if simple_user[2] == 'uz':
            question = "Iltimos tilni tanlang:"
        else:
            question = "Выберите пожалуйста язык:"
        await msg.answer(question, reply_markup=language_markup)
    else:
        choice_lan = "Iltimos tilni tanlang / Выберите пожалуйста язык:"
        await msg.answer(choice_lan, reply_markup=language_markup)
    await state.set_state(SimpleRegisterStates.language)


@dp.message_handler(IsPrivate(), text="⚙️ Sozlamalar")
async def settings(msg: types.Message):
    await msg.answer(msg.text, reply_markup=settings_markup_uz)


@dp.message_handler(IsPrivate(), text="⚙️ Настройки")
async def settings(msg: types.Message):
    await msg.answer(msg.text, reply_markup=settings_markup_ru)
