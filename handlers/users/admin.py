import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ContentType

from data.config import ADMINS
from filters import IsPrivate
from keyboards.default import menu_markup_uz, menu_markup_ru, language_markup, applications_menu_markup, \
    exams_menu_markup, directions_menu_markup, types_of_education_menu_markup, contract_menu_markup
from loader import dp, db


@dp.message_handler(IsPrivate(), text="Arizalar bo'limi", user_id=ADMINS)
async def applications_branch(msg: types.Message, state: FSMContext):
    await msg.answer(msg.text, reply_markup=applications_menu_markup)


@dp.message_handler(IsPrivate(), text="Imtihon bo'limi", user_id=ADMINS)
async def exams_branch(msg: types.Message, state: FSMContext):
    await msg.answer(msg.text, reply_markup=exams_menu_markup)


@dp.message_handler(IsPrivate(), text="Yo'nalishlar bo'limi", user_id=ADMINS)
async def directions_branch(msg: types.Message, state: FSMContext):
    await msg.answer(msg.text, reply_markup=directions_menu_markup)


@dp.message_handler(IsPrivate(), text="Ta'lim turlari bo'limi", user_id=ADMINS)
async def types_of_edu_branch(msg: types.Message, state: FSMContext):
    await msg.answer(msg.text, reply_markup=types_of_education_menu_markup)


@dp.message_handler(IsPrivate(), text="Kontrakt summalari", user_id=ADMINS)
async def contract_branch(msg: types.Message, state: FSMContext):
    await msg.answer(msg.text, reply_markup=contract_menu_markup)



