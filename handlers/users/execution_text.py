import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType

from filters import IsPrivate
from loader import dp, db
from states import TestExecutionStates


@dp.message_handler(IsPrivate(), text=["Imtihon topshirish", "Сдать экзамен"])
async def check_execution_text(msg: types.Message, state: FSMContext):
    applicant = await db.get_applicant(msg.from_user.id)
    simple_user = await db.select_simple_user(msg.from_user.id)
    if applicant:
        exam_result = await db.get_exam_result(msg.from_user.id)
        if exam_result:
            resp_text_uz = "❗️ Siz allaqachon imtihon topshirib bo'lgansiz!"
            resp_text_ru = "❗️ Вы уже сдали экзамен!"
            permission = False
        else:
            resp_text_uz = "Fan va texnologiyalar universitetining kirish imtihonlari tizimiga xush kelibsiz! Siz 2 ta fandan 25 tadan savolga va 10 ta mantiqiy savolga to'g'ri javob berishingiz kerak bo'ladi. Umumiy 60 ta test savollari uchun 4 soat vaqt beriladi. Tayyorlaning, imtixon 10 soniyadan keyin boshlanadi."
            resp_text_ru = "Добро пожаловать в систему вступительных экзаменов Университета науки и технологий! Вам нужно будет правильно ответить на 25 вопросов по двум предметам и на 10 логических вопросов. На выполнение 60 тестовых вопросов дается 4 часа. Подготовьтесь, экзамен начнется через 10 секунд."
            permission = True
    else:
        resp_text_uz = "❗️ Imtihon topshirish uchun avval Universitetga hujjat topshirishingiz kerak!"
        resp_text_ru = "❗️ Для сдачи экзамена вам сначала нужно подать документы в университет!"
        permission = False
    if simple_user[2] == 'uz':
        await msg.answer(resp_text_uz)
    else:
        await msg.answer(resp_text_ru)
    if permission:
        time_message = await msg.answer(f"{10}")
        await state.set_state(TestExecutionStates.execution)
        # for i in range(9, -1, -1):
        #     await asyncio.sleep(1)
        #     await time_message.edit_text(f"{i}")
        await time_message.edit_text("Tayyormisiz?")
        await asyncio.sleep(1)
        await choices_test(time_message, applicant, simple_user)


async def choices_test(msg, applicant, simple_user):
    direction_id = applicant[7]
    language = simple_user[2]
    tests = await db.select_active_tests_for_faculty(direction_id, language)
    print(tests)
    await msg.edit_text("(birinchi fan)dan test savollari:")


@dp.message_handler(IsPrivate(), state=TestExecutionStates.execution, content_types=ContentType.ANY)
async def err_msg_for_test_exe(msg: types.Message):
    await msg.delete()
