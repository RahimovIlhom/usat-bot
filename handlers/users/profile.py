import asyncio
import json

from aiogram import types
from aiogram.dispatcher.filters import Text

from filters import IsPrivate
from keyboards.default import profile_menu_markup_uz, profile_menu_markup_ru
from loader import dp, db


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
    created_time = applicant[10]  # Assuming applicant[10] is a datetime object
    formatted_created_time = created_time.strftime("%H:%M %d.%m.%Y")

    # Olimpiada ishtirokchisi (boolean)
    olympian_text = {
        'uz': 'Ha' if applicant[9] else 'Yo\'q',
        'ru': 'Да' if applicant[9] else 'Нет'
    }
    olympian = olympian_text[lang]

    GET_ME_TEXT = {
        'uz': (f"👤 Ism: {applicant[6]}\n"
               f"👤 Familya: {applicant[7]}\n"
               f"📞 Telefoni: {applicant[1]}\n"
               f"📞 Qo'shimcha telefoni: {applicant[2]}\n"
               f"🛂 Pasport: {applicant[3]}\n"
               f"🎂 Tug'ilgan sana: {applicant[4]}\n"
               f"🆔 PINFL: {applicant[5]}\n"
               f"🏆 Olimpiada ishtirokchisi: {olympian}\n"
               f"🗓️ Ro'yxatdan o'tilgan sana: {formatted_created_time}\n"),
        'ru': (f"👤 Имя: {applicant[6]}\n"
               f"👤 Фамилия: {applicant[7]}\n"
               f"📞 Телефон: {applicant[1]}\n"
               f"📞 Дополнительный телефон: {applicant[2]}\n"
               f"🛂 Паспорт: {applicant[3]}\n"
               f"🎂 Дата рождения: {applicant[4]}\n"
               f"🆔 PINFL: {applicant[5]}\n"
               f"🏆 Участник олимпиады: {olympian}\n"
               f"🗓️ Дата регистрации: {formatted_created_time}\n")
    }

    if applicant[11]:  # Check if photo exists
        await msg.answer_photo(applicant[11], caption=GET_ME_TEXT[lang])
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


async def get_science_name_by_id(science_id, lang):
    science = await db.select_science(science_id)
    return science[1] if lang == 'uz' else science[2]


async def format_user_responses(user_responses, lang='uz'):
    responses = json.loads(user_responses)
    grouped_responses = {}

    for response in responses:
        science_id = response['science_id']
        question_info = {
            "question_id": response["question_id"],
            "true_response": response["true_response"],
            "user_response": response["user_response"],
            "correct": response["true_response"] == response["user_response"]
        }
        if science_id not in grouped_responses:
            grouped_responses[science_id] = []
        grouped_responses[science_id].append(question_info)

    # Prepare formatted responses by sciences
    max_questions = max(len(questions) for questions in grouped_responses.values())

    # Fetch science names concurrently
    science_names = await asyncio.gather(*(get_science_name_by_id(science_id, lang)
                                           for science_id in grouped_responses.keys()))

    # Header with science names
    headers = " | ".join(science_names)
    formatted_responses = f"<pre>{headers}\n"

    # Prepare question-response lines
    for i in range(max_questions):
        line = ""
        for science_id, questions in grouped_responses.items():
            if i < len(questions):
                question = questions[i]
                status = "✅" if question["correct"] else "❌"
                line += f"{i + 1}. {question['user_response']} {status} | "
            else:
                line += " " * 15 + " | "  # Add empty space for alignment
        formatted_responses += line.rstrip(' | ') + "\n"

    formatted_responses += "</pre>"
    return formatted_responses


@dp.message_handler(Text(equals=["📊 Imtihon natijam", "📊 Мои результаты экзамена"]), IsPrivate())
async def my_latest_application(msg: types.Message):
    lang = 'uz' if msg.text == "📊 Imtihon natijam" else 'ru'
    applicant_id = msg.from_user.id  # Assuming tg_id is the Telegram user ID
    result = await db.get_exam_result_last(applicant_id)
    if result:
        user_responses = await format_user_responses(result[2], lang)
        minutes = int(result[6])
        seconds = int((result[6] - minutes) * 60)
        if lang == 'uz':
            message = (f"Arizachi ID: {result[1]}\n"
                       f"Umumiy ball: {result[5]}\n"
                       f"Imtihon topshirgan vaqt: {result[7].strftime('%H:%M %d-%m-%Y')}\n"
                       f"Imtihon uchun sarflangan vaqt: {minutes} daqiqa {seconds} soniya\n\n"
                       f"Foydalanuvchi javoblari:\n\n{user_responses}")
        else:
            message = (f"ID заявителя: {result[1]}\n"
                       f"Общий балл: {result[5]}\n"
                       f"Время сдачи экзамена: {result[7].strftime('%H:%M %d-%m-%Y')}\n"
                       f"Время, затраченное на экзамен: {minutes} минут {seconds} секунд\n\n"
                       f"Ответы пользователя:\n\n{user_responses}")
    else:
        if lang == 'uz':
            message = "Natija topilmadi."
        else:
            message = "Результат не найден."

    await msg.reply(message)

