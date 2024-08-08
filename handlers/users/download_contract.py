import os

from aiogram.types import Message, InputFile

from filters import IsPrivate
from loader import dp, db
from utils.db_api import get_contract_data_in_admission
from utils.misc.generate_contract_file import generate_pdf
from utils.misc.send_contract_file_telegraph import contract_file_link

TEXTS = {
    'uz': {
        'NOT_FOUND': "❗️ Siz yubormagansiz!",
        'DRAFT': "❗️ Kontrakt fayl mavjud emas. Arizangiz hali tayyor emas. Iltimos, arizangizni yuboring.",
        'SUBMITTED': "❗️ Kontrakt fayl mavjud emas. Arizangiz yuborilgan. Iltimos, arizangiz qabul qilinishini kuting.",
        'REJECTED': ("😔 Kontrakt fayl mavjud emas. Afsuski, arizangiz tasdiqlanmadi. Iltimos, kiritgan "
                     "ma’lumotlaringizni tekshirib, yana boshqatdan yuboring."),
        'FAILED': ("Kontrakt fayl mavjud emas. Afsuski siz imtihondan yiqilgansiz. Iltimos, \"🧑‍💻 Imtihon "
                   "topshirish\" tugmasi orqali qayta imtihon topshiring"),
        'EXAMINED': "✅ Kontrakt fayl mavjud emas. Siz imtihon topshirib bo'lgansiz! Iltimos, natijangizni kuting",
        'ACCEPTED': ("✅ Kontrakt fayl mavjud emas. Arizangiz tasdiqlangan. Iltimos, \"🧑‍💻 Imtihon topshirish\" tugmasi "
                     "orqali imtihon topshiring"),
        'NOT_READY': "Kontrakt faylingiz hali tayyor emas. Iltimos, keyinroq qayta urining.",
    },
    'ru': {
        'NOT_FOUND': "❗️ Вы не отправили!",
        'DRAFT': "❗️ Файл контракта не найден. Ваша заявка еще не готова. Пожалуйста, отправьте свою заявку.",
        'SUBMITTED': "❗️ Файл контракта не найден. Ваша заявка отправлена. Пожалуйста, дождитесь принятия вашей заявки.",
        'REJECTED': ("😔 Файл контракта не найден. К сожалению, ваша заявка не была подтверждена. Пожалуйста, проверьте "
                     "введенные данные и отправьте заново."),
        'FAILED': ("Файл контракта не найден. К сожалению, вы не прошли экзамен. Пожалуйста, нажмите кнопку \"🧑‍💻 "
                   "Сдать экзамен\" и сдайте экзамен снова."),
        'EXAMINED': "✅ Файл контракта не найден. Вы уже сдали экзамен! Пожалуйста, дождитесь результатов. ",
        'ACCEPTED': ("✅ Файл контракта не найден. Ваша заявка подтверждена. Пожалуйста, нажмите кнопку "
                     "\"🧑‍💻 Сдать экзамен\" и сдайте экзамен."),
        'NOT_READY': "Ваш файл контракта еще не готов. Пожалуйста, попробуйте позже.",
    }
}


@dp.message_handler(IsPrivate(), text=['📥 Shartnomani olish', '📥 Получить контракт'])
async def download_contract(msg: Message):
    lang = 'uz' if msg.text == '📥 Shartnomani olish' else 'ru'
    applicant_obj = await db.get_applicant(msg.from_user.id)
    if applicant_obj is None:
        await msg.answer(TEXTS[lang]['NOT_FOUND'])
        return
    else:
        status = applicant_obj[14]
        if status == 'PASSED':
            contract_file = applicant_obj[11]
            if not contract_file:
                response = await get_contract_data_in_admission(msg.from_user.id)
                if response.status_code == 200:
                    data = response.json()
                    contract_file_path = await generate_pdf(data)
                    input_file = InputFile(contract_file_path)
                    await msg.answer_document(input_file)
                    os.remove(contract_file_path)
                    # contract_file_url = await contract_file_link(data['fullName'], contract_file_path)
                    # await db.update_contract_file(msg.from_user.id, contract_file_url)
                    return
                else:
                    status = 'NOT_READY'

            else:
                input_file = InputFile(contract_file)
                await msg.answer_document(input_file)
                return

    await msg.answer(TEXTS[lang][status])
