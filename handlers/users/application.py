import asyncio
import os
from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, ReplyKeyboardRemove
from aiogram.utils.exceptions import BadRequest

from data.config import ADMINS
from filters import IsPrivate
from keyboards.default import phone_markup_uz, phone_markup_ru, menu_markup_uz, menu_markup_ru
from keyboards.inline import all_faculties_inlines, application_callback_data, types_and_contracts, \
    choices_e_edu_language
from loader import dp, db
from states import ApplicantRegisterStates


@dp.message_handler(IsPrivate(), text="📰 Universitetga hujjat topshirish")
async def submit_application_uz(msg: types.Message, state: FSMContext):
    simple_user = await db.select_simple_user(msg.from_user.id)
    await state.set_data({'language': simple_user[2]})
    applicant = await db.get_applicant(msg.from_user.id)
    if applicant:
        if applicant[14] == 'DRAFT':
            await show_faculties(msg, 'uz', f"{applicant[4]} {applicant[5]}")
            await state.set_state(ApplicantRegisterStates.direction_type_lan)
            return
        await msg.answer("❗️ Siz allaqachon hujjat topshirib bo'lgansiz!")
    else:
        await msg.answer("Pastdagi tugmani bosib, telefon raqamingizni yuboring.", reply_markup=phone_markup_uz)
        await state.set_state(ApplicantRegisterStates.phone)
        await state.update_data({'tgId': msg.from_user.id})


@dp.message_handler(IsPrivate(), text="📰 Подать документы в университет")
async def submit_application_ru(msg: types.Message, state: FSMContext):
    simple_user = await db.select_simple_user(msg.from_user.id)
    await state.set_data({'language': simple_user[2]})
    applicant = await db.get_applicant(msg.from_user.id)
    if applicant:
        if applicant[14] == 'DRAFT':
            await show_faculties(msg, 'ru', f"{applicant[4]} {applicant[5]}")
            await state.set_state(ApplicantRegisterStates.direction_type_lan)
            return
        await msg.answer("❗️ Вы уже подали документы!")
    else:
        await msg.answer("Нажмите кнопку ниже и отправьте свой номер телефона.", reply_markup=phone_markup_ru)
        await state.set_state(ApplicantRegisterStates.phone)
        await state.update_data({'tgId': msg.from_user.id})


@dp.message_handler(IsPrivate(), content_types=ContentType.CONTACT, state=ApplicantRegisterStates.phone)
async def send_contact(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data({'phoneNumber': msg.contact.phone_number})
    if data.get('language') == 'uz':
        info = "Qo'shimcha telefon raqam yuboring."
    else:
        info = "Отправьте дополнительный номер телефона."
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

    await state.update_data({'additionalPhoneNumber': msg.text})

    if user_language == 'uz':
        info = "Passportingiz seriasi va raqamini yuboring.\n\nMisol uchun: AA1234567"
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
    await state.update_data({'passport': passport})
    await msg.answer(TEXTS[data.get('language')])
    await ApplicantRegisterStates.next()


@dp.message_handler(state=ApplicantRegisterStates.passport, content_types=ContentType.ANY)
async def err_send_passport(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    await msg.delete()
    TEXTS = {
        'uz': {
            'err_text': "❗️ Pasport seria va raqam xato. Iltimos, quyidagi tartibda yuboring.\n\n<b>AA1234567</b>",
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
    language = data.get('language', 'ru')
    TEXTS = {
        'uz': {
            'one_resp_text': (
                "Talabalik - oltin davr deyishadi. Shu davrni bizning universitetda o'tkazishga ahd qilganingizdan "
                "xursandmiz. O'z navbatida biz ham sizga sifatli ta'lim berishga, kelajakda yetuk mutaxassis bo'lib "
                "yetishingizga yordam berishga tayyormiz!"
            ),
            'pinfl_exist_text': ("❗️ Bunday passport ma'lumotlari bilan hujjat topshirilgan. Iltimos, "
                                 "qayta hujjat topshiring:")
        },
        'ru': {
            'one_resp_text': (
                "Студенчество называют золотой эпохой. Мы рады, что вы решили провести этот период в нашем "
                "университете. В свою очередь, мы также готовы предоставить вам качественное образование и помочь вам "
                "стать квалифицированным специалистом в будущем!"
            ),
            'pinfl_exist_text': ("❗️ С документами с такими паспортными данными уже была подана заявка. Пожалуйста, "
                                 "подайте заявку снова.")
        }
    }
    if await db.get_applicant(msg.from_user.id, data.get('passport'), birthDate):
        await msg.answer(TEXTS[language]['pinfl_exist_text'],
                         reply_markup=menu_markup_uz if language == 'uz' else menu_markup_ru)
        await state.finish()
    else:
        data.update({'birthDate': birthDate})
        # applicant register for admission and get data
        # data ni olamiz admissiondan
        # fullname ni data ning ism va familiyasidan olib, statega update qilamiz
        await db.add_draft_applicant(**data)
        fullname = msg.from_user.full_name
        await state.update_data({'fullname': fullname})
        await msg.answer(TEXTS[language]['one_resp_text'])
        await asyncio.sleep(1.5)
        await show_faculties(msg, language, fullname)
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


@dp.callback_query_handler(application_callback_data.filter(), state=ApplicantRegisterStates.direction_type_lan)
async def select_application_func(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    fullname = data.get('fullname')
    direction_id = callback_data.get('direction_id')
    type_id = callback_data.get('type_id')
    edu_language = callback_data.get('edu_language')
    level = callback_data.get('level')
    if level == '0':
        await show_faculties(call, language, fullname)
    elif level == '1':
        await show_types_and_contracts(call, direction_id, language)
    elif level == '2':
        await show_edu_languages(call, direction_id, type_id, language)
    elif level == '3':
        await save_send_data_admission(call, direction_id, type_id, edu_language, language, fullname, state)


async def show_faculties(call, language, fullname):
    resp_texts = {
        'uz': {
            'question': ("Hurmatli {}! Aytingchi, siz universitetimizdagi qaysi ta'lim yo'nalishiga hujjatlaringizni "
                         "topshirmoqchisiz?")
        },
        'ru': {
            'question': ("Уважаемый {}! Скажите, пожалуйста, на какое направление обучения в нашем университете вы "
                         "собираетесь подавать документы?")
        }
    }
    if isinstance(call, types.Message):
        await call.answer("Arizangiz to'liq yuborilmagan!", reply_markup=ReplyKeyboardRemove())
        await call.answer(resp_texts[language]['question'].format(fullname),
                          reply_markup=await all_faculties_inlines(language))
    else:
        await call.message.edit_text(resp_texts[language]['question'].format(fullname),
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


async def save_send_data_admission(call, direction_id, type_id, edu_language, lang, fullname, state):
    await db.submit_applicant(call.from_user.id, direction_id, type_id, edu_language)
    # shu yerda admissionga barcha datalarni yuborish kerak
    if lang == "uz":
        resp_info = f"✅ Hurmatli {fullname}! Arizangiz qabul qilindi!"
        question = ("Tayyor bo'lsangiz, pastdagi \"🧑‍💻 Imtihon topshirish\" tugmasini bosib, test sinovlarini "
                    "o'tishingiz mumkin.\n\n"
                    "Test natijasiga ko'ra yetarlicha ball to'plasangiz, sizga o'qishga qabul "
                    "qilinganingiz haqida xabar chiqadi. Shu zahotiyoq shartnomangizni ko'chirib olishingiz mumkin "
                    "bo'ladi. Yetarlicha ball to'play olmasangiz, yana bir bor urinib ko'rishingizga imkoniyat "
                    "beriladi. Sizga omad tilaymiz!")
        markup = menu_markup_uz
    else:
        resp_info = f"✅ Уважаемый {fullname}! Ваша заявка принята!"
        question = ("Когда будете готовы, нажмите кнопку \"🧑‍💻 Сдать экзамен\" ниже, чтобы пройти тестирование.\n\n"
                    "Если вы наберете достаточное количество баллов по результатам теста, вам будет сообщено о "
                    "зачислении на учебу. Сразу после этого вы сможете скачать ваш контракт. Если набранных баллов "
                    "не хватит, вам будет предоставлена возможность попробовать еще раз. Желаем вам удачи!")
        markup = menu_markup_ru
    await call.message.edit_text(resp_info, reply_markup=None)
    await asyncio.sleep(0.4)
    await call.message.answer(question, reply_markup=markup)
    # applicant_file = await write_applicant_to_excel(call.from_user.id)
    #
    # # Send the file to all admins
    # for admin_id in ADMINS:
    #     try:
    #         await bot.send_document(admin_id, open(applicant_file, 'rb'), caption="Yangi arizachi",
    #                                 reply_markup=await accept_applicant_inline(call.from_user.id))
    #     except BadRequest:
    #         pass
    # os.remove(applicant_file)
    await state.reset_data()
    await state.finish()
