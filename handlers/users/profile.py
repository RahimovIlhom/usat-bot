from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from data.config import ADMINS
from filters import IsPrivate
from keyboards.default import language_markup, profile_menu_markup_uz, profile_menu_markup_ru
from loader import dp, db
from states import SimpleRegisterStates


@dp.message_handler(IsPrivate(), text="👤 Profilim")
async def my_profile(msg: types.Message):
    await msg.answer(msg.text, reply_markup=profile_menu_markup_uz)


@dp.message_handler(IsPrivate(), text="👤 Мой профиль")
async def my_profile(msg: types.Message):
    await msg.answer(msg.text, reply_markup=profile_menu_markup_ru)
