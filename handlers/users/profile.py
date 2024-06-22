from aiogram import types

from filters import IsPrivate
from keyboards.default import profile_menu_markup_uz, profile_menu_markup_ru
from loader import dp, db
from states import SimpleRegisterStates


@dp.message_handler(IsPrivate(), text="👤 Profilim")
async def my_profile(msg: types.Message):
    await msg.answer(msg.text, reply_markup=profile_menu_markup_uz)


@dp.message_handler(IsPrivate(), text="👤 Мой профиль")
async def my_profile(msg: types.Message):
    await msg.answer(msg.text, reply_markup=profile_menu_markup_ru)


@dp.message_handler(IsPrivate(), text=["ℹ️ Ma'lumotlarim", "ℹ️ Мои данные"])
async def my_profile(msg: types.Message):
    lang = 'uz' if msg.text == "ℹ️ Ma'lumotlarim" else 'ru'
    applicant = await db.get_me(tgId=str(msg.from_user.id))

    if not applicant:
        no_data_text = {
            'uz': "Sizning ma'lumotlaringiz mavjud emas",
            'ru': "Ваши данные отсутствуют"
        }
        await msg.answer(no_data_text[lang])
        return

    # Format the createdTime
    created_time = applicant[15]  # Assuming applicant[15] is a datetime object
    formatted_created_time = created_time.strftime("%H:%M %d.%m.%Y")

    # Gender mapping
    gender_map = {
        'uz': {'MALE': 'Erkak', 'FEMALE': 'Ayol'},
        'ru': {'MALE': 'Мужчина', 'FEMALE': 'Женщина'}
    }
    gender = gender_map[lang].get(applicant[13], 'N/A')

    GET_ME_TEXT = {
        'uz': (f"👤 Ism: {applicant[6]}\n"
               f"👤 Familya: {applicant[7]}\n"
               f"📞 Telefoni: {applicant[1]}\n"
               f"📞 Qo'shimcha telefoni: {applicant[2]}\n"
               f"🛂 Pasport: {applicant[3]}\n"
               f"🎂 Tug'ilgan sana: {applicant[4]}\n"
               f"🆔 PINFL: {applicant[5]}\n"
               f"🌍 Tug'ilgan joyi: {applicant[9]}\n"
               f"🏳️ Tug'ilgan mamlakat: {applicant[10]}\n"
               f"🌐 Millati: {applicant[11]}\n"
               f"🏳️ Fuqarolik: {applicant[12]}\n"
               f"🚻 Jins: {gender}\n"
               f"🗓️ Ro'yxatdan o'tilgan sana: {formatted_created_time}\n"),
        'ru': (f"👤 Имя: {applicant[6]}\n"
               f"👤 Фамилия: {applicant[7]}\n"
               f"📞 Телефон: {applicant[1]}\n"
               f"📞 Дополнительный телефон: {applicant[2]}\n"
               f"🛂 Паспорт: {applicant[3]}\n"
               f"🎂 Дата рождения: {applicant[4]}\n"
               f"🆔 PINFL: {applicant[5]}\n"
               f"🌍 Место рождения: {applicant[9]}\n"
               f"🏳️ Страна рождения: {applicant[10]}\n"
               f"🌐 Национальность: {applicant[11]}\n"
               f"🏳️ Гражданство: {applicant[12]}\n"
               f"🚻 Пол: {gender}\n"
               f"🗓️ Дата регистрации: {formatted_created_time}\n")
    }

    if applicant[14]:  # Check if photo exists
        await msg.answer_photo(applicant[14], caption=GET_ME_TEXT[lang])
    else:
        await msg.answer(GET_ME_TEXT[lang])


@dp.message_handler(IsPrivate(), text=["📄 Arizalarim", "📄 Мои заявки"])
async def my_applications(msg: types.Message):
    lang = 'uz' if msg.text == "📄 Arizalarim" else 'ru'
    applicant = await db.get_my_application(tgId=str(msg.from_user.id))

    if not applicant:
        no_application_text = {
            'uz': "Sizning arizangiz mavjud emas!",
            'ru': "Ваша заявка не найдена!"
        }
        await msg.answer(no_application_text[lang])
        return

    resp_text = {
        'uz': "Sizning universitetga hujjat topshirish bo'yicha arizangiz\n\n",
        'ru': "Ваша заявка на поступление в университет\n\n"
    }

    # Mapping for application status
    status_map = {
        'uz': {
            'DRAFT': 'QORALAMA',
            'SUBMITTED': 'ARIZA YUBORILDI',
            'REJECTED': 'ARIZA RAD ETILDI',
            'ACCEPTED': 'ARIZA QABUL QILINDI',
            'EXAMINED': 'IMTIHON TOPSHIRDI',
            'FAILED': 'IMTIHON MUVAFFAQIYATSIZ',
            'PASSED': 'IMTHONDAN MUVAFFAQIYATLI O\'TDI'
        },
        'ru': {
            'DRAFT': 'ЧЕРНОВИК',
            'SUBMITTED': 'ЗАЯВКА ОТПРАВЛЕНА',
            'REJECTED': 'ЗАЯВКА ОТКЛОНЕНА',
            'ACCEPTED': 'ЗАЯВКА ПРИНЯТА',
            'EXAMINED': 'ЭКЗАМЕН СДАН',
            'FAILED': 'ЭКЗАМЕН НЕ СДАН',
            'PASSED': 'ЭКЗАМЕН УСПЕШНО СДАН'
        }
    }

    status = status_map[lang].get(applicant[8], 'N/A')
    updated_time = applicant[7].strftime("%H:%M %d.%m.%Y")
    olympian = 'Ha' if applicant[6] else 'Yo\'q' if lang == 'uz' else 'Да' if applicant[6] else 'Нет'

    GET_APPLICATION_TEXT = {
        'uz': (f"📚 Ta'lim yo'nalishi: {applicant[1]}\n"
               f"🏫 Ta'lim turi: {applicant[3]}\n"
               f"🗣️ Ta'lim tili: {applicant[5]}\n"
               f"🏅 Olimpiadachi: {olympian}\n"
               f"🕒 Oxirgi o'zgarish vaqti: {updated_time}\n"
               f"📄 Ariza holati: {status}\n"),
        'ru': (f"📚 Направление обучения: {applicant[2]}\n"
               f"🏫 Тип образования: {applicant[4]}\n"
               f"🗣️ Язык обучения: {applicant[5]}\n"
               f"🏅 Олимпиадник: {olympian}\n"
               f"🕒 Время последнего изменения: {updated_time}\n"
               f"📄 Статус заявки: {status}\n")
    }

    await msg.answer(resp_text[lang] + GET_APPLICATION_TEXT[lang])


@dp.message_handler(IsPrivate(), text=["📊 Imtihon natijam", "📊 Мои результаты экзамена"])
async def my_applications(msg: types.Message):
    pass
