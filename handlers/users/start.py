import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ContentType

from data.config import ADMINS
from filters import IsPrivate
from keyboards.default import menu_markup_uz, menu_markup_ru, language_markup, admin_menu_markup_uz
from loader import dp, db
from states import SimpleRegisterStates, TestExecutionStates


@dp.message_handler(IsPrivate(), CommandStart(), state='*', user_id=ADMINS)
async def bot_start(message: types.Message, state: FSMContext):
    await message.answer("Menu", reply_markup=admin_menu_markup_uz)
    await state.finish()


@dp.message_handler(IsPrivate(), CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    simple_user = await db.select_simple_user(message.from_user.id)
    if simple_user:
        if await state.get_state() == TestExecutionStates.science.state:
            await message.delete()
            if simple_user[2] == 'uz':
                msg = await message.answer("‼️ Imtihon vaqtida hech qanday buyruq ishlamaydi!")
            else:
                msg = await message.answer("‼️ Во время экзамена никакие команды не работают!")
            await asyncio.sleep(2)
            await msg.delete()
            return
        if simple_user[2] == 'uz':
            await message.answer("Bosh menyu:", reply_markup=menu_markup_uz)
        else:
            await message.answer("Главное меню:", reply_markup=menu_markup_ru)
        await state.finish()
    else:
        answer = ("Assalomu alaykum! Fan va texnologiyalar universitetining rasmiy Telegram botiga xush kelibsiz. Bu "
                  "yerda siz universitetga hujjat topshirishingiz, onlayn imtihon topshirishingiz, shartnomani "
                  "olishingiz, universitet, ta'lim yo'nalishlari va kontrakt summalari haqida ma'lumot olishingiz, "
                  "ma'muriyatga murojaatlaringizni yuborishingiz mumkin.")
        answer += ("\n\nПривет! Добро пожаловать в официальный Telegram-бот Университета науки и технологий. Здесь вы "
                   "можете подать документы в университет, пройти онлайн экзамен, получить контракт, информацию об "
                   "университете, направлениях обучения и суммах контракта, а также направить свои обращения "
                   "администрации.")
        choice_lan = "Iltimos tilni tanlang / Выберите пожалуйста язык:"
        await message.answer(answer)
        await state.set_state(SimpleRegisterStates.language)
        await asyncio.sleep(1)
        await message.answer(choice_lan, reply_markup=language_markup)


@dp.message_handler(IsPrivate(), state=SimpleRegisterStates.language)
async def choice_language_func(msg: types.Message, state: FSMContext):
    if msg.text == "O'zbek tili":
        language = 'uz'
        answer = "Bosh menyu:"
        markup = menu_markup_uz
    elif msg.text == "Русский язык":
        language = 'ru'
        answer = "Главное меню:"
        markup = menu_markup_ru
    else:
        await msg.delete()
        await msg.answer("Iltimos tilni tanlang / Выберите пожалуйста язык:", reply_markup=language_markup)
        return
    await db.add_or_set_simple_user(msg.from_user.id, msg.from_user.full_name, language)
    await msg.answer(answer, reply_markup=markup)
    await state.finish()


@dp.message_handler(IsPrivate(), state=SimpleRegisterStates.language, content_types=ContentType.ANY)
async def choice_language_err_func(msg: types.Message):
    await msg.delete()
    await msg.answer("Iltimos tilni tanlang / Выберите пожалуйста язык:", reply_markup=language_markup)
