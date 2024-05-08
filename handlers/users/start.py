from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ContentType

from filters import IsPrivate
from keyboards.default import manu_markup, language_markup
from loader import dp, db
from states import SimpleRegisterStates


@dp.message_handler(IsPrivate(), CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    simple_users = await db.select_simple_user(message.from_user.id)
    if simple_users:
        await message.answer("Bosh menyu:", reply_markup=manu_markup)
    else:
        answer = "Iltimos tilni tanlang / Выберите пожалуйста язык:"
        await message.answer(answer, reply_markup=language_markup)
        await state.set_state(SimpleRegisterStates.language)


@dp.message_handler(IsPrivate(), state=SimpleRegisterStates.language)
async def choice_language_func(msg: types.Message, state: FSMContext):
    if msg.text == "O'zbek tili":
        language = 'uz'
        answer = ("Assalomu alaykum! Fan va texnologiyalar universitetining rasmiy Telegram botiga xush kelibsiz. Bu "
                  "yerda siz universitetga hujjat topshirishingiz, onlayn imtihon topshirishingiz, shartnomani "
                  "olishingiz, universitet, ta'lim yo'nalishlari va kontrakt summalari haqida ma'lumot olishingiz, "
                  "ma'muriyatga murojaatlaringizni yuborishingiz mumkin.")
    elif msg.text == "Русский язык":
        language = 'ru'
        answer = ("Привет! Добро пожаловать в официальный Telegram-бот Университета науки и технологий. Здесь вы "
                  "можете подать документы в университет, пройти онлайн экзамен, получить контракт, информацию об "
                  "университете, направлениях обучения и суммах контракта, а также направить свои обращения "
                  "администрации.")
    else:
        await msg.delete()
        await msg.answer("Iltimos tilni tanlang / Выберите пожалуйста язык:", reply_markup=language_markup)
        return
    await db.add_simple_user(msg.from_user.id, msg.from_user.full_name, language)
    await msg.answer(answer, reply_markup=manu_markup)
    await state.finish()


@dp.message_handler(IsPrivate(), state=SimpleRegisterStates.language, content_types=ContentType.ANY)
async def choice_language_err_func(msg: types.Message):
    await msg.delete()
    await msg.answer("Iltimos tilni tanlang / Выберите пожалуйста язык:", reply_markup=language_markup)
