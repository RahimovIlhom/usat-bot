from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, InputFile, ReplyKeyboardRemove

from filters import IsPrivate
from keyboards.default import phone_markup_uz, phone_markup_ru
from loader import dp, db
from states import ApplicantRegisterStates


@dp.message_handler(IsPrivate(), text="Universitetga hujjat topshirish")
async def submit_application_uz(msg: types.Message, state: FSMContext):
    applicant = await db.get_applicant(msg.from_user.id)
    if applicant:
        await msg.answer("Siz allaqachon hujjat topshirib bo'lgansiz!")
    else:
        await msg.answer("Pastdagi tugmani bosib, telefon raqamingizni yuboring.", reply_markup=phone_markup_uz)
        await state.set_state(ApplicantRegisterStates.phone)


@dp.message_handler(IsPrivate(), text="Подать документы в университет")
async def submit_application_ru(msg: types.Message, state: FSMContext):
    applicant = await db.get_applicant(msg.from_user.id)
    if applicant:
        await msg.answer("Вы уже подали документы!")
    else:
        await msg.answer("Нажмите кнопку ниже и отправьте свой номер телефона.", reply_markup=phone_markup_ru)
        await state.set_state(ApplicantRegisterStates.phone)


@dp.message_handler(IsPrivate(), content_types=ContentType.CONTACT, state=ApplicantRegisterStates.phone)
async def send_contact(msg: types.Message, state: FSMContext):
    await state.set_data({'phone': msg.contact.phone_number})
    simple_user = await db.select_simple_user(msg.from_user.id)
    if simple_user[2] == 'uz':
        info = "ID-kartangizdagi Shaxsiy raqamingizni kiriting. "
        image = InputFile('data/images/pinfl.jpg')
        image_url = "http://telegra.ph//file/97b3043fbcdc89ba48360.jpg"
    else:
        info = "Введите персональный идентификационный номер, указанный на ID-карте."
        image = InputFile('data/images/pinfl_ru.jpg')
        image_url = "http://telegra.ph//file/e815e58a3c4c08948b617.jpg"
    try:
        await msg.answer_photo(image_url, caption=info, reply_markup=ReplyKeyboardRemove())
    except:
        await msg.answer_photo(image, caption=info, reply_markup=ReplyKeyboardRemove())
    await ApplicantRegisterStates.next()
