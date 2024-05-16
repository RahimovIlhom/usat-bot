import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, InputFile, ReplyKeyboardRemove

from filters import IsPrivate
from keyboards.default import phone_markup_uz, phone_markup_ru, menu_markup_uz, menu_markup_ru
from keyboards.inline import all_faculties_inlines, application_callback_data, types_and_contracts, \
    choices_e_edu_language
from loader import dp, db
from states import ApplicantRegisterStates


@dp.message_handler(IsPrivate(), text="Universitetga hujjat topshirish")
async def submit_application_uz(msg: types.Message, state: FSMContext):
    applicant = await db.get_applicant(msg.from_user.id)
    if applicant:
        await msg.answer("❗️ Siz allaqachon hujjat topshirib bo'lgansiz!")
    else:
        await msg.answer("Pastdagi tugmani bosib, telefon raqamingizni yuboring.", reply_markup=phone_markup_uz)
        await state.set_state(ApplicantRegisterStates.phone)


@dp.message_handler(IsPrivate(), text="Подать документы в университет")
async def submit_application_ru(msg: types.Message, state: FSMContext):
    applicant = await db.get_applicant(msg.from_user.id)
    if applicant:
        await msg.answer("❗️ Вы уже подали документы!")
    else:
        await msg.answer("Нажмите кнопку ниже и отправьте свой номер телефона.", reply_markup=phone_markup_ru)
        await state.set_state(ApplicantRegisterStates.phone)


@dp.message_handler(IsPrivate(), content_types=ContentType.CONTACT, state=ApplicantRegisterStates.phone)
async def send_contact(msg: types.Message, state: FSMContext):
    simple_user = await db.select_simple_user(msg.from_user.id)
    await state.set_data({'phone': msg.contact.phone_number,
                          'language': simple_user[2]})
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


@dp.message_handler(state=ApplicantRegisterStates.pinfl, content_types=ContentType.TEXT)
async def send_pinfl(msg: types.Message, state: FSMContext):
    pinfl = msg.text
    data = await state.get_data()
    if data.get('language') == 'uz':
        err_text = "❗️ Shaxsiy raqam xato. Iltimos, qayta yuboring."
        one_resp_text = "Talabalik - oltin davr deyishadi. Shu davrni bizning universitetda o'tkazishga ahd qilganingizdan xursandmiz. O'z navbatida biz ham sizga sifatli ta'lim berishga, kelajakda yetuk mutaxassis bo'lib yetishingizga yordam berishga tayyormiz!"
        question = "Hurmatli {}! Aytingchi, siz universitetimizdagi qaysi ta'lim yo'nalishiga hujjatlaringizni topshirmoqchisiz?"
        pinfl_exist_text = "❗️ Bunday shaxsiy raqam yoki telefon raqam bilan hujjat topshirilgan. Iltimos, qayta kiriting:"

    else:
        err_text = "❗️ Персональный номер указан неверно. Пожалуйста, отправьте повторно."
        one_resp_text = "Студенчество называют золотой эпохой. Мы рады, что вы решили провести этот период в нашем университете. В свою очередь, мы также готовы предоставить вам качественное образование и помочь вам стать квалифицированным специалистом в будущем!"
        question = "Уважаемый {}! Скажите, пожалуйста, на какое направление обучения в нашем университете вы собираетесь подавать документы?"
        pinfl_exist_text = "❗️ Документы с таким персональным номером или номером телефона уже поданы. Пожалуйста, введите заново:"
    if pinfl.isdigit():
        if len(pinfl) == 14:
            # admissionga post qilishda avval pinfl orqali ariza topshirmaganli tekshiriladi
            if await db.get_applicant(msg.from_user.id, pinfl, data.get('phone')):
                await msg.answer(pinfl_exist_text)
                return
            # pinflni admissionga post qilish kerak
            fullname = msg.from_user.full_name  # admissiondan kelgan ma'lumotlarni ichidan fullname ni ovolamiz
            await state.update_data({'pinfl': pinfl, 'fullname': fullname})
            await msg.answer(one_resp_text)
            await ApplicantRegisterStates.next()
            await asyncio.sleep(1.5)
            await msg.answer(question.format(fullname), reply_markup=await all_faculties_inlines())
            return

    await msg.answer(err_text)


@dp.message_handler(state=ApplicantRegisterStates.pinfl, content_types=ContentType.ANY)
async def err_send_pinfl(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    await msg.delete()
    if data.get('language') == 'uz':
        err_resp = "Iltimos, ID-kartangizdagi Shaxsiy raqamingizni kiriting."
    else:
        err_resp = "Пожалуйста, введите ваш личный номер, указанный на вашей ID-карте."
    await msg.answer(err_resp)


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
        await send_data_admission(call, direction_id, type_id, edu_language, language, fullname, state)


async def show_faculties(call, language, fullname):
    if language == 'uz':
        question = "Hurmatli {}! Aytingchi, siz universitetimizdagi qaysi ta'lim yo'nalishiga hujjatlaringizni topshirmoqchisiz?"
    else:
        question = "Уважаемый {}! Скажите, пожалуйста, на какое направление обучения в нашем университете вы собираетесь подавать документы?"
    await call.message.edit_text(question.format(fullname), reply_markup=await all_faculties_inlines(language))


async def show_types_and_contracts(call, direction_id, language):
    if language == 'uz':
        question = "Aytingchi, qaysi ta'lim shaklida o'qishni rejalashtirgangiz?\n\nKunduzgi ta'lim odatda ertalab 09:00 dan boshlanib, o'rtacha 14:00 gacha davom etadi. Kechki ta'lim - 16:00 dan 20:00 gacha davom etadi va kontrakt narxlari judayam past. Sirtqi ta'lim talabalari yiliga 2 marta 1 oyga chaqiriladi, shu sababli kontrakt narxlari eng past hisoblanadi. Bunda talaba ham ishlab, ham o'qish imkoniyatiga ega bo'ladi."
    else:
        question = "Скажите, пожалуйста, в какой форме обучения вы планируете учиться?\n\nДневное обучение обычно начинается в 09:00 утра и продолжается до примерно 14:00. Вечернее обучение длится с 16:00 до 20:00, и стоимость контракта заметно ниже. Заочное обучение предполагает, что студенты приезжают два раза в год на месяц, поэтому стоимость контракта считается самой низкой. Это дает возможность одновременно работать и учиться."
    await call.message.edit_text(question, reply_markup=await types_and_contracts(direction_id, language))


async def show_edu_languages(call, direction_id, type_id, language):
    direction = await db.select_direction(direction_id)
    type_of_edu = await db.select_type_of_education(type_id)
    if language == 'uz':
        question = f"Zo'r! Demak, siz Fan va texnologiyalar universitetining <b>{direction[1]}</b> yo'nalishiga, <b>{type_of_edu[1]}</b> ta'lim shakliga hujjat topshirmoqdasiz. Ta'lim tilini tanlang:"
    else:
        question = f"Отлично! Итак, вы подаете документы на направление <b>{direction[2]}</b> в Факультет науки и технологий, форма обучения <b>{type_of_edu[2]}</b>. Выберите язык обучения:"
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


async def send_data_admission(call, direction_id, type_id, edu_language, lang, fullname, state):
    data = await state.get_data()
    phone = data.get('phone')
    pinfl = data.get('pinfl')
    firstName = data.get('firstName')
    lastName = data.get('lastName')
    middleName = data.get('middleName')
    passport = data.get('passport')
    olympian = data.get('olympian', False)
    await db.add_applicant(call.from_user.id, phone, pinfl, firstName, lastName, middleName, passport, direction_id, type_id, edu_language, olympian)
    # shu yerda admissionga barcha datalarni yuborish kerak
    if lang == "uz":
        resp_info = f"✅ Hurmatli {fullname}! Arizangiz qabul qilindi!"
        question = "Tayyor bo'lsangiz, pastdagi \"Imtihon topshirish\" tugmasini bosib, test sinovlarini o'tishingiz mumkin.\n\nTest natijasiga ko'ra yetarlicha ball to'plasangiz, sizga o'qishga qabul qilinganingiz haqida xabar chiqadi. Shu zahotiyoq shartnomangizni ko'chirib olishingiz mumkin bo'ladi. Yetarlicha ball to'play olmasangiz, yana bir bor urinib ko'rishingizga imkoniyat beriladi. Sizga omad tilaymiz!"
        markup = menu_markup_uz
    else:
        resp_info = f"✅ Уважаемый {fullname}! Ваша заявка принята!"
        question = "Когда будете готовы, нажмите кнопку \"Сдать экзамен\" ниже, чтобы пройти тестирование.\n\nЕсли вы наберете достаточное количество баллов по результатам теста, вам будет сообщено о зачислении на учебу. Сразу после этого вы сможете скачать ваш контракт. Если набранных баллов не хватит, вам будет предоставлена возможность попробовать еще раз. Желаем вам удачи!"
        markup = menu_markup_ru
    await call.message.edit_text(resp_info, reply_markup=None)
    await asyncio.sleep(0.4)
    await call.message.answer(question, reply_markup=markup)
    await state.reset_data()
    await state.finish()
