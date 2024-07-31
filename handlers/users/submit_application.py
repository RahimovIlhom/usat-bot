import asyncio
import os
import re
from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType, ReplyKeyboardRemove, InputFile
from aiogram.utils.exceptions import BadRequest

from filters import IsPrivate
from keyboards.default import phone_markup_uz, phone_markup_ru, menu_markup_uz, menu_markup_ru, no_olympian_markup, \
    dtm_markup
from keyboards.inline import all_faculties_inlines, application_callback_data, types_and_contracts, \
    choices_e_edu_language, regions_buttons, region_callback_data, cities_buttons, city_callback_data
from loader import dp, db, db_olympian
from states import ApplicantRegisterStates
from utils import certificate_photo_link
from utils.db_api import signup_applicant, get_applicant_in_admission, submit_applicant_for_admission


@dp.message_handler(IsPrivate(), Text(equals=["📰 Universitetga hujjat topshirish", "📰 Подать документы в университет"]))
async def submit_application(msg: types.Message, state: FSMContext):
    language = 'uz' if msg.text == '📰 Universitetga hujjat topshirish' else 'ru'
    await state.set_data({'language': language})

    applicant = await db.get_applicant(msg.from_user.id)
    if applicant:
        if applicant[14] == 'DRAFT':
            await state.update_data({
                'tgId': applicant[0],
                'applicantNumber': applicant[15],
                'birthDate': applicant[16],
                'passport': applicant[7],
                'phoneNumber': applicant[1],
                'additionalPhoneNumber': applicant[2],
                'applicantId': applicant[19],
            })

            await question_first_name(msg, language)  # shu yerda ism dan boshlab so'rab ketilishi kerak.
            await state.set_state(ApplicantRegisterStates.first_name)
            return
        else:
            user_data_resp = await get_applicant_in_admission(msg.from_user.id)
            if user_data_resp.status_code == 200:
                status = user_data_resp.json().get('status')
                await db.update_application_status(msg.from_user.id, status)
                if status == 'REJECTED':
                    await state.update_data({
                        'tgId': applicant[0],
                        'applicantNumber': applicant[15],
                        'birthDate': applicant[16],
                        'passport': applicant[7],
                        'phoneNumber': applicant[1],
                        'additionalPhoneNumber': applicant[2],
                        'applicantId': applicant[19],
                    })
                    TEXTS = {
                        "uz": "❗️ Afsuski, arizangiz tasdiqlanmadi. Iltimos, kiritgan ma’lumotlaringizni tekshirib, yana boshqatdan yuboring.",
                        "ru": "❗️ К сожалению, ваша заявка не была подтверждена. Пожалуйста, проверьте введенные данные и отправьте их снова."
                    }
                    await msg.answer(TEXTS[language])
                    await question_first_name(msg, language)  # shu yerda ism dan boshlab so'rab ketilishi kerak.
                    await state.set_state(ApplicantRegisterStates.first_name)
                    return

        if language == "uz":
            await msg.answer("❗️ Siz allaqachon hujjat topshirib bo'lgansiz!")
        else:
            await msg.answer("❗️ Вы уже подали документы!")
    else:
        if language == "uz":
            await msg.answer("Pastdagi tugmani bosib, telefon raqamingizni yuboring.", reply_markup=phone_markup_uz)
        else:
            await msg.answer("Нажмите кнопку ниже и отправьте свой номер телефона.", reply_markup=phone_markup_ru)

        await state.set_state(ApplicantRegisterStates.phone)
        await state.update_data({'tgId': msg.from_user.id})


@dp.message_handler(IsPrivate(), content_types=ContentType.CONTACT, state=ApplicantRegisterStates.phone)
async def send_contact(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data({'phoneNumber': msg.contact.phone_number})
    if data.get('language') == 'uz':
        info = ("Iltimos, yana bitta qo’shimcha telefon raqamini yuboring. Bunda onangiz yoki otangizni telefon raqami "
                "bo’lishi maqsadga muvofiq.")
    else:
        info = ("Пожалуйста, отправьте еще один дополнительный номер телефона. Лучше всего указать номер телефона "
                "вашей мамы или папы.")
    await msg.answer(info, reply_markup=ReplyKeyboardRemove())
    await ApplicantRegisterStates.next()


@dp.message_handler(IsPrivate(), content_types=ContentType.ANY, state=ApplicantRegisterStates.phone)
async def send_contact(msg: types.Message):
    await msg.delete()
    simple_user = await db.select_simple_user(msg.from_user.id)
    if simple_user[2] == 'uz':
        info = "Iltimos, pastdagi tugmani bosib, telefon raqamingizni yuboring."
        markup = phone_markup_uz
    else:
        info = "Пожалуйста, нажмите кнопку ниже и укажите свой номер телефона."
        markup = phone_markup_ru
    await msg.answer(info, reply_markup=markup)


@dp.message_handler(IsPrivate(), regexp=r"^\+?(998)?[0-9]{2}[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{2}[-\s\.]?[0-9]{2}$",
                    state=ApplicantRegisterStates.additional_phone)
async def send_contact(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    user_language = data.get('language')

    if msg.text in data.get('phoneNumber'):
        message_text = "❗️ Qo'shimcha telefon raqam asosiy raqam bilan bir xil. Iltimos, qayta yuboring." \
            if user_language == 'uz' \
            else "❗️ Дополнительный номер телефона аналогичен основному. Пожалуйста, отправьте повторно."
        await msg.answer(message_text)
        return

    phone = msg.text.replace('+', '')
    if not phone.startswith('998'):
        phone = f"998{phone}"
    await state.update_data({'additionalPhoneNumber': phone})

    if user_language == 'uz':
        info = "Pasportingiz seriyasini va raqamini yuboring.\n\nMisol uchun: AA1234567"
    else:
        info = "Пожалуйста, отправьте серию и номер вашего паспорта.\n\nПример: AA1234567"

    await msg.answer(info, reply_markup=ReplyKeyboardRemove())
    await ApplicantRegisterStates.next()


@dp.message_handler(IsPrivate(), content_types=ContentType.ANY, state=ApplicantRegisterStates.additional_phone)
async def send_contact(msg: types.Message):
    await msg.delete()
    simple_user = await db.select_simple_user(msg.from_user.id)
    if simple_user[2] == 'uz':
        info = "❗️ Qo'shimcha telefon raqamingiz xato. Iltimos, qayta yuboring."
    else:
        info = "❗️ Ваш дополнительный номер телефона неверен. Пожалуйста, отправьте повторно."
    await msg.answer(info)


@dp.message_handler(state=ApplicantRegisterStates.passport, regexp=r'^[A-Z]{2}\d{7}$', content_types=ContentType.TEXT)
async def send_passport(msg: types.Message, state: FSMContext):
    TEXTS = {
        'uz': "Tug'ilgan sanangizni yuboring.\n\nMisol uchun: 01.01.2000 yoki 01-01-2000",
        'ru': "Пожалуйста, отправьте вашу дату рождения.\n\nПример: 01.01.2000 или 01-01-2000",
    }
    passport = msg.text
    data = await state.get_data()
    await state.update_data({'passport': passport.upper()})
    await msg.answer(TEXTS[data.get('language')])
    await ApplicantRegisterStates.next()


@dp.message_handler(state=ApplicantRegisterStates.passport, content_types=ContentType.ANY)
async def err_send_passport(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    await msg.delete()
    TEXTS = {
        'uz': {
            'err_text': ("❗️ Pasport seriyasi yoki raqami xato kiritildi. Iltimos, quyidagi tartibda yuboring:"
                         "\n\n<b>AA1234567</b>"),
        },
        'ru': {
            'err_text': "❗️ Серия и номер паспорта неправильные. Пожалуйста, отправьте в следующем "
                        "формате.\n\n<b>AA1234567</b>",
        }
    }
    await msg.answer(TEXTS[data.get('language')]['err_text'])


@dp.message_handler(state=ApplicantRegisterStates.birth_date, content_types=ContentType.TEXT,
                    regexp=r'^(0[1-9]|[12][0-9]|3[01])[-.](0[1-9]|1[012])[-.](19|20)\d{2}$')
async def send_birth_date(msg: types.Message, state: FSMContext):
    birthDateText = msg.text
    separator = '-' if '-' in birthDateText else '.'
    birthDate = datetime.strptime(birthDateText, f'%d{separator}%m{separator}%Y').date()
    data = await state.get_data()
    data.update({'birthDate': birthDate})
    language = data.get('language', 'ru')

    TEXTS = {
        'uz': {
            'pinfl_exist_text': ("❗️ Bunday passport ma'lumotlari bilan hujjat topshirilgan. Iltimos, "
                                 "pasport ma'lumotlaringizni qayta yuboring:"),
            'checking': "♻️ Ma'lumotlar tekshirilmoqda",
            'data_error': ("❗️ Pasport ma'lumotlaringiz yoki tug'ilgan kuningiz xato kiritilgan bo'lishi mumkin. "
                           "Iltimos, tekshirib qayta kiriting."),
            'unknown_error': "❗️ Noma'lum xatolik. Iltimos, qayta hujjat topshiring.",
            'exists_phone': ("❗️ Siz ushbu telefon raqamingiz bilan qabul.usat.uz sayti orqali ro'yxatdan o'tgansiz. "
                             "Shaxsiy kabinetga kirish uchun qabul.usat.uz saytida \"Kirish\" tugmasini bosib, "
                             "telefon raqamingizga SMS orqali yuborilgan parolni kiriting. Parolni yo'qotgan "
                             "bo'lsangiz, \"Parolni unutdingizmi?\" tugmasini bosing va parolingizni tiklang."),
        },
        'ru': {
            'pinfl_exist_text': (
                "❗️ С такими паспортными данными уже поданы документы. Пожалуйста, подайте документы повторно:"),
            'checking': "♻️ Данные проверяются",
            'data_error': ("❗️ Возможно, вы неправильно ввели паспортные данные или дату рождения. "
                           "Пожалуйста, проверьте и введите заново."),
            'unknown_error': "❗️ Неизвестная ошибка. Пожалуйста, подайте документы повторно.",
            'exists_phone': ("❗️ Вы уже зарегистрированы на сайте qabul.usat.uz с этим номером телефона. "
                             "Для входа в личный кабинет на сайте qabul.usat.uz нажмите кнопку \"Вход\" и введите "
                             "пароль, отправленный по SMS на ваш номер телефона. Если вы потеряли пароль, нажмите "
                             "кнопку \"Забыли пароль?\" и восстановите его."),

        }
    }

    async def handle_error(message, error_key):
        await message.answer(TEXTS[language][error_key],
                             reply_markup=menu_markup_uz if language == 'uz' else menu_markup_ru)
        await state.finish()

    applicant_exists = await db.get_applicant(msg.from_user.id, data.get('passport'), birthDate)
    if applicant_exists:
        await handle_error(msg, 'pinfl_exist_text')
        if language == 'uz':
            info = "Pasportingiz seriyasini va raqamini yuboring.\n\nMisol uchun: AA1234567"
        else:
            info = "Пожалуйста, отправьте серию и номер вашего паспорта.\n\nПример: AA1234567"

        await msg.answer(info, reply_markup=ReplyKeyboardRemove())
        await state.set_state(ApplicantRegisterStates.passport)
        return

    user_data_resp = await get_applicant_in_admission(msg.from_user.id)

    if isinstance(user_data_resp, str):
        await msg.answer(user_data_resp)
        return

    if user_data_resp.status_code == 200:
        user_data = user_data_resp.json()
        data.update({
            'applicantId': user_data.get('id'),
            'applicantNumber': user_data.get('applicantNumber')
        })
    elif user_data_resp.status_code == 404:
        resp = await signup_applicant(**data)
        await msg.answer(TEXTS[language]['checking'])
        await asyncio.sleep(0.5)

        if isinstance(resp, str):
            await msg.answer(resp)
            return
        elif resp.status_code != 201:
            if resp.status_code == 400:
                error_meta = resp.json().get('meta', {})
                if 'phone' in error_meta:
                    await handle_error(msg, 'exists_phone')
                    return
                else:
                    await msg.answer(error_meta.get('general_errors', [TEXTS[language]['unknown_error']])[0],
                                     reply_markup=menu_markup_uz if language == 'uz' else menu_markup_ru)
                    await state.finish()
                    return
            else:
                await handle_error(msg, 'unknown_error')
                return
        else:
            user_data_resp = await get_applicant_in_admission(msg.from_user.id)
            if user_data_resp.status_code == 200:
                user_data = user_data_resp.json()
                data.update({
                    'applicantId': user_data.get('id'),
                    'applicantNumber': user_data.get('applicantNumber'),
                })
    else:
        await handle_error(msg, 'unknown_error')
        return

    await db.add_draft_applicant(**data)
    await state.update_data(data)
    await asyncio.sleep(0.5)
    await question_first_name(msg, language)  # shu yerda ism dan boshlab so'rab ketilishi kerak.
    await ApplicantRegisterStates.next()


@dp.message_handler(state=ApplicantRegisterStates.birth_date, content_types=ContentType.ANY)
async def err_send_birth_date(msg: types.Message, state: FSMContext):
    await msg.delete()
    data = await state.get_data()
    language = data.get('language')
    TEXTS = {
        'uz': {
            'err_text': ("❗️ Tug'ilgan sanangizni ko'rsatilgan formatda yuboring.\n\nMisol uchun: 01.01.2000 yoki "
                         "01-01-2000"),
        },
        'ru': {
            'err_text': "❗️ Отправьте вашу дату рождения в указанном формате.\n\nНапример: 01.01.2000 или 01-01-2000",
        }
    }
    await msg.answer(TEXTS[language]['err_text'])


async def question_first_name(msg, language):
    QUESTION_TEXTS = {
        'uz': "Ismingizni yuboring (pasportingiz bo'yicha)",
        'ru': "Отправьте своё имя (как в паспорте)"
    }
    await msg.answer(QUESTION_TEXTS[language],
                     reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=ApplicantRegisterStates.first_name, content_types=ContentType.TEXT)
async def send_first_name(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    LAST_NAME_TEXTS = {
        'uz': "Familiyangizni yuboring (pasportingiz bo'yicha)",
        'ru': "Отправьте своё фамилию (как в паспорте)"
    }
    await state.update_data({'firstName': msg.text})
    await msg.answer(LAST_NAME_TEXTS[language])
    await ApplicantRegisterStates.next()


@dp.message_handler(state=ApplicantRegisterStates.first_name, content_types=ContentType.ANY)
async def err_send_first_name(msg: types.Message, state: FSMContext):
    await msg.delete()
    data = await state.get_data()
    language = data.get('language')
    TEXTS = {
        'uz': "Iltimos, ismingizni yuboring!",
        'ru': "Пожалуйста, Отправьте своё имя!"
    }
    err_msg = await msg.answer(TEXTS[language])
    await asyncio.sleep(2)
    await err_msg.delete()


@dp.message_handler(state=ApplicantRegisterStates.last_name, content_types=ContentType.TEXT)
async def send_last_name(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    MIDDLE_NAME_TEXTS = {
        'uz': "Sha'rifingizni yuboring (otangizni ismini yozing)",
        'ru': "Отправьте своё отчество (напишите имя отца)"
    }
    await state.update_data({'lastName': msg.text})
    await msg.answer(MIDDLE_NAME_TEXTS[language])
    await ApplicantRegisterStates.next()


@dp.message_handler(state=ApplicantRegisterStates.last_name, content_types=ContentType.ANY)
async def err_send_last_name(msg: types.Message, state: FSMContext):
    await msg.delete()
    data = await state.get_data()
    language = data.get('language')
    TEXTS = {
        'uz': "Iltimos, familiyangizni yuboring!",
        'ru': "Пожалуйста, Отправьте своё фамилию!"
    }
    err_msg = await msg.answer(TEXTS[language])
    await asyncio.sleep(2)
    await err_msg.delete()


@dp.message_handler(state=ApplicantRegisterStates.middle_name, content_types=ContentType.TEXT)
async def send_middle_name(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    await state.update_data({'middleName': msg.text})
    PINFL_DATA = {
        'uz': {
            'text': "JSHSHIR (PINFL) yoki ID-kartangizdagi Shaxsiy raqamingizni yuboring.",
            'image_url': "http://telegra.ph//file/97b3043fbcdc89ba48360.jpg",
            'image': InputFile('data/images/pinfl.jpg')
        },
        'ru': {
            'text': "Отправьте JSHSHIR (PINFL) или персональный идентификационный номер, указанный на ID-карте.",
            'image_url': "http://telegra.ph//file/e815e58a3c4c08948b617.jpg",
            'image': InputFile('data/images/pinfl_ru.jpg')
        }
    }
    try:
        await msg.answer_photo(PINFL_DATA[language]['image_url'], caption=PINFL_DATA[language]['text'])
    except BadRequest:
        await msg.answer_photo(PINFL_DATA[language]['image'], caption=PINFL_DATA[language]['text'])
    await ApplicantRegisterStates.next()


@dp.message_handler(state=ApplicantRegisterStates.middle_name, content_types=ContentType.ANY)
async def err_send_middle_name(msg: types.Message, state: FSMContext):
    await msg.delete()
    data = await state.get_data()
    language = data.get('language')
    TEXTS = {
        'uz': "Iltimos, sharifingizni yuboring!",
        'ru': "Пожалуйста, Отправьте своё отчество!"
    }
    err_msg = await msg.answer(TEXTS[language])
    await asyncio.sleep(2)
    await err_msg.delete()


@dp.message_handler(state=ApplicantRegisterStates.pinfl, content_types=ContentType.TEXT, regexp=r'^\d{14}$')
async def send_pinfl(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    await state.update_data({'pinfl': msg.text})
    PASSPORT_DATA = {
        'uz': "Pasport yoki ID Kartangiz old qismining rasmini yuboring.",
        'ru': "Отправьте, пожалуйста, фотографию передней стороны вашего паспорта или ID-карты."
    }
    await msg.answer(PASSPORT_DATA[language])
    # await show_regions(msg, language)
    await ApplicantRegisterStates.next()


@dp.message_handler(state=ApplicantRegisterStates.pinfl, content_types=ContentType.ANY)
async def err_send_pinfl(msg: types.Message, state: FSMContext):
    await msg.delete()
    data = await state.get_data()
    language = data.get('language')
    TEXTS = {
        'uz': ("Iltimos, JSHSHIR (PINFL) yoki ID-kartangizdagi shaxsiy raqamingizni yuboring! Odatda JSHSHIR (PINFL) "
               "yoki ID-kartangizdagi shaxsiy raqam 14ta raqamdan iborat bo'ladi."),
        'ru': ("Пожалуйста, oтправьте JSHSHIR (PINFL) или персональный идентификационный номер, указанный на ID-карте! "
               "Обычно ваш ПИНФЛ или личный номер на ID-карте состоит из 14 цифр.")
    }
    err_msg = await msg.answer(TEXTS[language])
    await asyncio.sleep(2)
    await err_msg.delete()


@dp.message_handler(state=ApplicantRegisterStates.passport_image_front, content_types=ContentType.PHOTO)
async def send_passport_front(msg: types.Message, state: FSMContext):
    photo = msg.photo[-1]
    directory = 'admin/media/passport/images/front/'
    image_path = f'{directory}{photo.file_id}.jpg'
    image_db_path = f'passport/images/front/{photo.file_id}.jpg'

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Download and save the image
    await photo.download(destination_file=image_path)

    # Update state with the image path
    await state.update_data({'passportPhotoFront': image_db_path})
    data = await state.get_data()
    lang = data.get('language')
    PASSPORT_DATA = {
        'uz': "Pasport yoki ID Kartangiz orqa qismining rasmini yuboring.",
        'ru': "Отправьте пожалуйста, фотографию задней стороны вашего паспорта или ID-карты."
    }
    await msg.answer(PASSPORT_DATA[lang])
    await ApplicantRegisterStates.next()


@dp.message_handler(state=ApplicantRegisterStates.passport_image_front, content_types=ContentType.ANY)
async def err_send_passport_front(msg: types.Message, state: FSMContext):
    await msg.delete()
    data = await state.get_data()
    language = data.get('language')
    TEXTS = {
        'uz': "Iltimos, pasport yoki ID Kartangiz old qismining rasmini yuboring!",
        'ru': "Пожалуйста, отправьте фото копии передней стороны вашего паспорта или ID-карты!"
    }
    err_msg = await msg.answer(TEXTS[language])
    await asyncio.sleep(2)
    await err_msg.delete()


@dp.message_handler(state=ApplicantRegisterStates.passport_image_back, content_types=ContentType.PHOTO)
async def send_passport_back(msg: types.Message, state: FSMContext):
    photo = msg.photo[-1]
    directory = 'admin/media/passport/images/back/'
    image_path = f'{directory}{photo.file_id}.jpg'
    image_db_path = f'passport/images/back/{photo.file_id}.jpg'

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Download and save the image
    await photo.download(destination_file=image_path)
    await state.update_data({'passportBackPhoto': image_db_path})
    data = await state.get_data()
    lang = data.get('language')
    await show_regions(msg, lang)
    await ApplicantRegisterStates.next()


@dp.message_handler(state=ApplicantRegisterStates.passport_image_back, content_types=ContentType.ANY)
async def err_send_passport_back(msg: types.Message, state: FSMContext):
    await msg.delete()
    data = await state.get_data()
    language = data.get('language')
    TEXTS = {
        'uz': "Iltimos, pasport yoki ID Kartangiz orqa qismining rasmini yuboring!",
        'ru': "Пожалуйста, отправьте фото копии задней стороны вашего паспорта или ID-карты!"
    }
    err_msg = await msg.answer(TEXTS[language])
    await asyncio.sleep(2)
    await err_msg.delete()


async def show_regions(msg, lang):
    resp_texts = {
        'uz': {
            'question': "O’zbekistonning qaysi hududidansiz?"
        },
        'ru': {
            'question': "В каком регионе Узбекистана вы проживаете?"
        }
    }
    if isinstance(msg, types.CallbackQuery):
        await msg.message.edit_text(resp_texts[lang]['question'], reply_markup=await regions_buttons(lang))
    else:
        await msg.answer(resp_texts[lang]['question'], reply_markup=await regions_buttons(lang))


@dp.callback_query_handler(region_callback_data.filter(), state=ApplicantRegisterStates.region)
async def send_region(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    region_name = callback_data.get('name')
    region_id = callback_data.get('id')
    cities_texts = {
        'uz': f"{region_name}ning qaysi tumanidansiz?",
        'ru': f"В каком районе {region_name} вы проживаете?"
    }
    await state.update_data({
        'regionName': region_name,
        'regionId': region_id
    })
    await call.message.edit_text(cities_texts[language], reply_markup=await cities_buttons(region_id, language))
    await ApplicantRegisterStates.next()


@dp.callback_query_handler(city_callback_data.filter(), state=ApplicantRegisterStates.city)
async def show_cities_for_reg(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    city_name = callback_data.get('name')
    city_id = callback_data.get('id')
    if city_id == 'back':
        await show_regions(call, language)
        await state.set_state(ApplicantRegisterStates.region)
        return
    else:
        await state.update_data({
            'cityName': city_name,
            'cityId': city_id
        })
        TEXTS = {
            'uz': {
                'success': "Yashash manzilingiz qabul qilindi.",
                'dtm': ("DTM balingizni yuboring. \n(Agar DTM balingiz mavjud bo'lmasa, quyidagi \"MAVJUD EMAS\" "
                        "tugmani bosing)"),
            },
            'ru': {
                'success': "Ваш адрес проживания принят.",
                'dtm': "Отправьте ваш балл DTM. \n(Если у вас нет балла DTM, нажмите кнопку \"НЕ СУЩЕСТВУЕТ\" ниже)",
            }
        }
    await ApplicantRegisterStates.next()
    await call.message.edit_text(TEXTS[language]['success'], reply_markup=None)
    await call.message.answer(TEXTS[language]['dtm'], reply_markup=await dtm_markup(language))
    # await check_olympian(call, state)


@dp.message_handler(state=[ApplicantRegisterStates.city, ApplicantRegisterStates.region], content_types=ContentType.ANY)
async def error_city_send(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get('language')
    await msg.delete()
    TEXTS = {
        'uz': "‼️ Iltimos, yuqoridagi tugmalardan foydalaning!",
        'ru': "‼️ Пожалуйста, используйте кнопки выше!"
    }
    err_msg = await msg.answer(TEXTS[lang])
    await asyncio.sleep(2)
    await err_msg.delete()


@dp.message_handler(state=ApplicantRegisterStates.dtm_score, content_types=ContentType.TEXT)
async def dtm_send(msg: types.Message, state: FSMContext):
    ball = msg.text
    if ball in ["MAVJUD EMAS", "НЕ СУЩЕСТВУЕТ"]:
        await ApplicantRegisterStates.certificate.set()
        await check_olympian(msg, state)
        return
    data = await state.get_data()
    language = data.get('language')
    TEXTS = {
        'uz': "DTM Abituriyent ID raqamini yuboring",
        'ru': "Отправьте ID номер абитуриента DTM"
    }

    def is_decimal(s):
        decimal_pattern = re.compile(r'^-?\d+(\.\d+)?$')
        return bool(decimal_pattern.match(s))

    if not is_decimal(ball):
        await error_dtm_send(msg, state)
        return

    await state.update_data({
        'dtmScore': ball
    })
    await msg.answer(TEXTS[language])
    await ApplicantRegisterStates.next()


@dp.message_handler(state=ApplicantRegisterStates.dtm_score, content_types=ContentType.ANY)
async def error_dtm_send(msg: types.Message, state: FSMContext):
    await msg.delete()
    data = await state.get_data()
    language = data.get('language')
    TEXTS = {
        'uz': "Iltimos, DTM balingizni yuboring yoki quyidagi tugmadan foydalaning!",
        'ru': "Пожалуйста, отправьте ваш балл DTM или воспользуйтесь кнопкой ниже!"
    }
    err_msg = await msg.answer(TEXTS[language])
    await asyncio.sleep(2)
    await err_msg.delete()


@dp.message_handler(state=ApplicantRegisterStates.dtm_abiturient_number, content_types=ContentType.TEXT)
async def dtm_number_send(msg: types.Message, state: FSMContext):
    dtm_number = msg.text
    if not dtm_number.isdigit() or len(dtm_number) != 7:
        await error_dtm_number_send(msg, state)
        return
    await state.update_data({
        'dtmAbiturientNumber': msg.text
    })
    await ApplicantRegisterStates.next()
    await check_olympian(msg, state)


@dp.message_handler(state=ApplicantRegisterStates.dtm_abiturient_number, content_types=ContentType.ANY)
async def error_dtm_number_send(msg: types.Message, state: FSMContext):
    await msg.delete()
    data = await state.get_data()
    language = data.get('language')
    TEXTS = {
        'uz': "Iltimos, DTM Abituriyent ID raqamini yuboring!",
        'ru': "Пожалуйста, отправьте ID номер абитуриента DTM!"
    }
    err_msg = await msg.answer(TEXTS[language])
    await asyncio.sleep(2)
    await err_msg.delete()


async def check_olympian(msg, state):
    OLYMPIAN_TEXTS = {
        'uz': {
            'olympian': ("Siz \"Fan javohirlari\" olimpiadasi ishtirok etib, {science} fanidan {vaucher} so'mlik "
                         "vaucherga egasiz!"),
            'no_olympian': ("Agar olimpiadada qo’lga kiritgan sertifikatingiz bo'lsa, rasmini yuboring. "
                            "\nSertifikatingiz mavjud bo'lmasa quyidagi \"MAVJUD EMAS\" tugmasini bosing."),
        },
        'ru': {
            'olympian': ("Вы являетесь участником олимпиады \"Fan javohirlari\" и обладателем ваучера на {vaucher} "
                         "сум по предмету {science}!"),
            'no_olympian': ("Если у вас есть сертификат, полученный на олимпиаде, отправьте его фотографию. \n"
                            "Если сертификата нет, нажмите кнопку «НЕ ИМЕЕТСЯ».")
        },
    }
    data = await state.get_data()
    pinfl = data.get('pinfl')
    lang = data.get('language')
    olympian_result = await db_olympian.get_olympian(msg.from_user.id, pinfl)
    if olympian_result:
        science = olympian_result[3]
        result = olympian_result[8]
        vaucher = (2000000 if result >= 26 else 1500000 if result >= 20 else 1000000) if result >= 10 else 0
        if vaucher > 0:
            await msg.answer(OLYMPIAN_TEXTS[lang]['olympian'].format(science=science, vaucher=vaucher))
            await state.update_data({
                'vaucher': vaucher,
                'certificateImage': olympian_result[7],
                'result': result,
                'olympian': True
            })
            await state.set_state(ApplicantRegisterStates.direction_type_lan)
            await asyncio.sleep(1.5)
            await show_faculties(msg, lang, data.get('firstName'), answer_text=True)
            return
    await msg.answer(OLYMPIAN_TEXTS[lang]['no_olympian'], reply_markup=await no_olympian_markup(lang))


@dp.message_handler(state=ApplicantRegisterStates.certificate, text=['MAVJUD EMAS', 'НЕ ИМЕЕТСЯ'])
async def no_certificate(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.set_state(ApplicantRegisterStates.direction_type_lan)
    await show_faculties(msg, data.get('language'), data.get('firstName'), answer_text=True)


@dp.message_handler(state=ApplicantRegisterStates.certificate, content_types=ContentType.PHOTO)
async def send_certificate(msg: types.Message, state: FSMContext):
    photo = msg.photo[-1]
    image_url = await certificate_photo_link(photo)
    await state.update_data({'certificateImage': image_url, 'olympian': True})
    data = await state.get_data()
    await state.set_state(ApplicantRegisterStates.direction_type_lan)
    await show_faculties(msg, data.get('language'), data.get('firstName'), answer_text=True)


@dp.message_handler(state=ApplicantRegisterStates.certificate, content_types=ContentType.ANY)
async def send_certificate(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get('language')
    ERR_TEXTS = {
        'uz': "Iltimos, quyidagi tugmadan foydalaning yoki sertifikatingiz rasmini yuboring!",
        'ru': "Пожалуйста, воспользуйтесь кнопкой ниже или отправьте фото вашего сертификата!",
    }
    await msg.answer(ERR_TEXTS[lang])


@dp.callback_query_handler(application_callback_data.filter(), state=ApplicantRegisterStates.direction_type_lan)
async def select_application_func(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    first_name = data.get('firstName')
    direction_id = callback_data.get('direction_id')
    type_id = callback_data.get('type_id')
    edu_language = callback_data.get('edu_language')
    level = callback_data.get('level')
    if level == '0':
        await show_faculties(call, language, first_name)
    elif level == '1':
        await show_types_and_contracts(call, direction_id, language)
    elif level == '2':
        await show_edu_languages(call, direction_id, type_id, language)
    elif level == '3':
        await save_send_data_admission(call, direction_id, type_id, edu_language, language, first_name, state)


async def show_faculties(call, language, first_name, answer_text=False):
    resp_texts = {
        'uz': {
            'one_resp_text': (
                "Talabalik - oltin davr deyishadi. Shu davrni bizning universitetda o'tkazishga ahd qilganingizdan "
                "xursandmiz. O'z navbatida biz ham sizga sifatli ta'lim berishga, kelajakda yetuk mutaxassis bo'lib "
                "yetishingizga yordam berishga tayyormiz!"
            ),
            'question': ("Hurmatli {}! Aytingchi, siz universitetimizdagi qaysi ta'lim yo'nalishiga hujjatlaringizni "
                         "topshirmoqchisiz?")
        },
        'ru': {
            'question': ("Уважаемый {}! Скажите, пожалуйста, на какое направление обучения в нашем университете вы "
                         "собираетесь подавать документы?"),
            'one_resp_text': (
                "Студенческая жизнь - золотой век, как говорят. Мы рады, что вы решили провести это время в нашем "
                "университете. Со своей стороны, мы готовы предоставить вам качественное образование и помочь стать "
                "выдающимся специалистом в будущем!"
            ),
        }
    }
    if isinstance(call, types.Message):
        if answer_text:
            await call.answer(resp_texts[language]['one_resp_text'].format(first_name),
                              reply_markup=ReplyKeyboardRemove())
            await asyncio.sleep(3)
            await call.answer(resp_texts[language]['question'].format(first_name),
                              reply_markup=await all_faculties_inlines(language))
        else:
            await call.edit_text(resp_texts[language]['question'].format(first_name),
                                 reply_markup=await all_faculties_inlines(language))
    else:
        if answer_text:
            await call.message.answer(resp_texts[language]['one_resp_text'].format(first_name),
                                      reply_markup=ReplyKeyboardRemove())
            await asyncio.sleep(3)
            await call.message.answer(resp_texts[language]['question'].format(first_name),
                                      reply_markup=await all_faculties_inlines(language))
        else:
            await call.message.edit_text(resp_texts[language]['question'].format(first_name),
                                         reply_markup=await all_faculties_inlines(language))


async def show_types_and_contracts(call, direction_id, language):
    if language == 'uz':
        question = ("Aytingchi, qaysi ta'lim shaklida o'qishni rejalashtirgangiz?\n\nKunduzgi ta'lim odatda ertalab "
                    "09:00 dan boshlanib, o'rtacha 14:00 gacha davom etadi. Kechki ta'lim - 16:00 dan 20:00 gacha "
                    "davom etadi va kontrakt narxlari judayam past. Sirtqi ta'lim talabalari yiliga 2 marta 1 oyga "
                    "chaqiriladi, shu sababli kontrakt narxlari eng past hisoblanadi. Bunda talaba ham ishlab, "
                    "ham o'qish imkoniyatiga ega bo'ladi.")
    else:
        question = ("Скажите, пожалуйста, в какой форме обучения вы планируете учиться?\n\nДневное обучение обычно "
                    "начинается в 09:00 утра и продолжается до примерно 14:00. Вечернее обучение длится с 16:00 до "
                    "20:00, и стоимость контракта заметно ниже. Заочное обучение предполагает, что студенты приезжают "
                    "два раза в год на месяц, поэтому стоимость контракта считается самой низкой. Это дает "
                    "возможность одновременно работать и учиться.")
    await call.message.edit_text(question, reply_markup=await types_and_contracts(direction_id, language))


async def show_edu_languages(call, direction_id, type_id, language):
    direction = await db.select_direction(direction_id)
    type_of_edu = await db.select_type_of_education(type_id)
    if language == 'uz':
        question = (f"Zo'r! Demak, siz Fan va texnologiyalar universitetining <b>{direction[1]}</b> yo'nalishiga, <b>"
                    f"{type_of_edu[1]}</b> ta'lim shakliga hujjat topshirmoqdasiz. Ta'lim tilini tanlang:")
    else:
        question = (f"Отлично! Итак, вы подаете документы на направление <b>{direction[2]}</b> в Факультет науки и "
                    f"технологий, форма обучения <b>{type_of_edu[2]}</b>. Выберите язык обучения:")
    await call.message.edit_text(question, reply_markup=await choices_e_edu_language(direction_id, type_id, language))


@dp.message_handler(state=ApplicantRegisterStates.direction_type_lan, content_types=ContentType.ANY)
async def err_direction_type_lan(msg: types.Message, state: FSMContext):
    await msg.delete()
    data = await state.get_data()
    lang = data.get('language')
    if lang == 'uz':
        err_info = "☝️ Iltimos, yuqoridagi tugmalardan foydalaning!"
    else:
        err_info = "☝️ Пожалуйста, используйте кнопки выше!"
    message = await msg.answer(err_info)
    await asyncio.sleep(1.5)
    await message.delete()


async def save_send_data_admission(call, direction_id, type_id, edu_language, lang, first_name, state):
    data = await state.get_data()
    vaucher = data.get('vaucher', 0)
    certificateImage = data.get('certificateImage', None)
    result = data.get('result', 0)
    olympian = data.get('olympian', False)

    data.update({
        'directionOfEducationId': direction_id,
        'directionOfEducationName': (await db.select_direction(direction_id))[1 if edu_language == 'uz' else 2],
        'typeOfEducationId': type_id,
        'typeOfEducationName': (await db.select_type_of_education(type_id))[1 if edu_language == 'uz' else 2],
        'languageOfEducationId': 1 if edu_language == 'uz' else 2,
        'languageOfEducationName': edu_language,
        'olympian': olympian,
    })
    if certificateImage:
        await db.add_olympian_result(call.from_user.id, vaucher, certificateImage, result)
    await db.submit_applicant(**data)
    await asyncio.sleep(0.5)

    resp = await submit_applicant_for_admission(**data)

    if resp.status_code == 404:
        await applicant_not_found(call, state, lang)
        return
    elif resp.status_code == 500:
        TEXTS = {
            "uz": "Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring!",
            "ru": "Произошла ошибка. Пожалуйста, попробуйте еще раз!",
            "en": "Error occurred. Please try again!",
        }
        await state.reset_data()
        await state.finish()
        await call.message.edit_text(TEXTS[lang], reply_markup=None)
        await call.message.answer("Menyu" if lang == 'uz' else "Меню",
                                  reply_markup=menu_markup_uz if lang == 'uz' else menu_markup_ru)
        return

    if lang == "uz":
        resp_info = f"✅ Hurmatli {first_name}! Arizangiz qabul qilindi!"
        question = ("Tayyor bo'lsangiz, pastdagi \"🧑‍💻 Imtihon topshirish\" tugmasini bosib, test sinovlarini "
                    "o'tishingiz mumkin.\n\n"
                    "Test natijasiga ko'ra yetarlicha ball to'plasangiz, sizga o'qishga qabul "
                    "qilinganingiz haqida xabar chiqadi. Shu zahotiyoq shartnomangizni ko'chirib olishingiz mumkin "
                    "bo'ladi. Yetarlicha ball to'play olmasangiz, yana bir bor urinib ko'rishingizga imkoniyat "
                    "beriladi. Sizga omad tilaymiz!")
        success = ("Barcha ma’lumotlaringiz tasdiqlansa, siz talabalikka tavsiya etilasiz. Bu haqda sizga botda va SMS "
                   "orqali tegishli xabar yuboramiz. Arizani ko’rib chiqish bir necha daqiqa ichida amalga oshiriladi.")
        failed = ("Afsuski UZBMB (DTM) ballingiz sizni imtihonsiz qabul qilishimiz uchun yetarli emas. Shuning uchun "
                  "shu botni o’zida test topshirishingiz kerak bo’ladi. Tayyor bo'lsangiz, pastdagi \"🧑‍💻 Imtihon "
                  "topshirish\" tugmasini bosing.\n\nTest natijasiga ko'ra yetarlicha ball to'plasangiz, "
                  "sizga o'qishga qabul qilinganingiz haqida xabar yuboriladi. Yetarlicha ball to'play olmasangiz, "
                  "yana bir bor urinib ko'rishingizga imkoniyat beriladi. Sizga omad tilaymiz!")
        markup = menu_markup_uz
    else:
        resp_info = f"✅ Уважаемый {first_name}! Ваша заявка принята!"
        question = ("Когда будете готовы, нажмите кнопку \"🧑‍💻 Сдать экзамен\" ниже, чтобы пройти тестирование.\n\n"
                    "Если вы наберете достаточное количество баллов по результатам теста, вам будет сообщено о "
                    "зачислении на учебу. Сразу после этого вы сможете скачать ваш контракт. Если набранных баллов "
                    "не хватит, вам будет предоставлена возможность попробовать еще раз. Желаем вам удачи!")
        success = ("Если вся ваша информация будет подтверждена, вас рекомендуют к зачислению в студенты. "
                   "Об этом вам будет отправлено соответствующее уведомление в боте и по SMS. "
                   "Рассмотрение заявки осуществляется в течение нескольких минут.")
        failed = ("К сожалению, ваш балл UZBMB (DTM) недостаточен для поступления без экзамена. Поэтому вам нужно "
                  "будет сдать тест в этом боте. Когда будете готовы, нажмите кнопку \"🧑‍💻 Сдать экзамен\" "
                  "ниже.\n\nЕсли вы наберете достаточное количество баллов по результатам теста, вам будет отправлено "
                  "уведомление о зачислении. Если вы не наберете достаточное количество баллов, вам будет "
                  "предоставлена еще одна попытка. Желаем вам удачи!")
        markup = menu_markup_ru
    dtm_score = data.get('dtmScore', None)
    await call.message.edit_text(resp_info, reply_markup=None)
    await asyncio.sleep(1)
    await state.reset_data()
    await state.finish()
    if dtm_score:
        if float(dtm_score) > 50.0:
            await call.message.answer(success, reply_markup=markup)
        else:
            await call.message.answer(failed, reply_markup=markup)
    else:
        await call.message.answer(question, reply_markup=markup)


async def applicant_not_found(call: types.CallbackQuery, state: FSMContext, lang: str = "uz"):
    application = await get_applicant_in_admission(call.from_user.id)
    data = application.json()
    data.update({
        'firstName': data['firstName'],
        'lastName': data['lastName'],
        'middleName': data['middleName'],
        'pinfl': data['jshir'],
        'passportPhotoFront': data['passportPhoto'],
        'passportBackPhoto': data['passportBackPhoto'],
        'tgId': call.from_user.id,
        'regionId': data['region']['id'],
        'regionName': data['region']['name'],
        'cityId': data['city']['id'],
        'cityName': data['city']['name'],
        'directionOfEducationId': data['educationFaculty']['id'],
        'directionOfEducationName': data['educationFaculty']['name'],
        'typeOfEducationId': data['educationType']['id'],
        'typeOfEducationName': data['educationType']['name'],
        'languageOfEducationId': data['educationLanguage']['id'],
        'languageOfEducationName': 'uz' if data['educationLanguage']['id'] == 1 else 'ru',
        'dtmScore': data['dtmScore'],
        'dtmAbiturientNumber': data['dtmAbiturientNumber'],
        'olympian': True if data.get('certificateNumber') else False,
    })

    if data.get('certificateNumber', None):
        await db.add_olympian_result(call.from_user.id, data.get('score'))
    await db.submit_applicant(**data)

    if lang == "uz":
        resp_info = "Siz ariza topshirib bo'lgansiz! Ariza ma'lumotlarini Profilim bo'limida ko'rishingiz mumkin."
    else:
        resp_info = "Вы уже подали заявку! Вы можете увидеть информацию о заявке в разделе Профиль."
    await call.message.edit_text(resp_info, reply_markup=None)
    await call.message.answer("Menyu" if lang == "uz" else "Меню",
                              reply_markup=menu_markup_uz if lang == "uz" else menu_markup_ru)
    await state.reset_data()
    await state.finish()
