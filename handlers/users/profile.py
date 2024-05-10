from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from data.config import ADMINS
from filters import IsPrivate
from keyboards.default import language_markup
from loader import dp, db
from states import SimpleRegisterStates


@dp.message_handler(IsPrivate(), Command('set_lang'), state='*', user_id=ADMINS)
async def set_language(msg: types.Message):
    await msg.answer("Bu buyruq admin uchun emas!")


@dp.message_handler(IsPrivate(), Command('set_lang'), state='*')
async def set_language(msg: types.Message, state: FSMContext):
    simple_user = await db.select_simple_user(msg.from_user.id)
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
