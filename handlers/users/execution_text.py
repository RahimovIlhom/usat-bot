import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, ReplyKeyboardRemove
from aiogram.utils.exceptions import BadRequest

from filters import IsPrivate
from keyboards.default import menu_markup_uz, menu_markup_ru
from keyboards.inline import ready_inline_button, responses_callback_data, all_responses_inlines
from loader import dp, db
from states import TestExecutionStates


@dp.message_handler(IsPrivate(), text=["🧑‍💻 Imtihon topshirish", "🧑‍💻 Сдать экзамен"])
async def check_execution_text(msg: types.Message):
    applicant = await db.get_applicant(msg.from_user.id)
    simple_user = await db.select_simple_user(msg.from_user.id)
    permission = False
    if applicant:
        exam_result = await db.get_exam_result(msg.from_user.id)
        if exam_result:
            resp_text_uz = "❗️ Siz allaqachon imtihon topshirib bo'lgansiz!"
            resp_text_ru = "❗️ Вы уже сдали экзамен!"
        else:
            if len(await db.select_active_tests_for_faculty(applicant[7], applicant[9])) != 3:
                if simple_user[2] == 'uz':
                    await msg.answer(f"❗️ Hozirda imtihon savollari mavjud emas!")
                else:
                    await msg.answer(f"❗️ В настоящее время экзаменационные вопросы отсутствуют!")
                return
            resp_text_uz = "Fan va texnologiyalar universitetining kirish imtihonlari tizimiga xush kelibsiz! Siz 2 ta fandan 25 tadan savolga va 10 ta mantiqiy savolga to'g'ri javob berishingiz kerak bo'ladi. Umumiy 60 ta test savollari uchun 4 soat vaqt beriladi.\nTayyormisiz?"
            resp_text_ru = "Добро пожаловать в систему вступительных экзаменов Университета науки и технологий! Вам нужно будет правильно ответить на 25 вопросов по двум предметам и на 10 логических вопросов. На выполнение 60 тестовых вопросов дается 4 часа.\nВы готовы?"
            permission = True
    else:
        resp_text_uz = "❗️ Imtihon topshirish uchun avval Universitetga hujjat topshirishingiz kerak!"
        resp_text_ru = "❗️ Для сдачи экзамена вам сначала нужно подать документы в университет!"
    if simple_user[2] == 'uz':
        message = await msg.answer(resp_text_uz)
    else:
        message = await msg.answer(resp_text_ru)
    if permission:
        await message.edit_reply_markup(await ready_inline_button(simple_user[2]))


@dp.callback_query_handler(text='ready')
async def you_are_ready(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(TestExecutionStates.science1)
    simple_user = await db.select_simple_user(call.from_user.id)
    applicant = await db.get_applicant(call.from_user.id)
    direction_id = applicant[7]
    tests = list(await db.select_active_tests_for_faculty(direction_id, applicant[9]))
    test = tests.pop(0)
    questions = list(await db.select_questions_for_test(test[0]))
    test_data = {
        'all_tests': tests,
        'test': test,
        'questions': questions,
        'number': 1
    }
    await state.update_data(test_data)
    await call.message.edit_reply_markup(None)
    if simple_user[2] == 'uz':
        await call.message.answer(f"{test[3]} fanidan test savollari. Tayyorlaning, imtixon 10 soniyadan keyin boshlanadi.",
                                  reply_markup=ReplyKeyboardRemove())
    else:
        await call.message.answer(f"Тестовые вопросы по предмету {test[4]}. Подготовьтесь, экзамен начнется через 10 секунд.",
                                  reply_markup=ReplyKeyboardRemove())
    time_message = await call.message.answer(f"{10}")
    # for i in range(9, -1, -1):
    #     await asyncio.sleep(1)
    #     await time_message.edit_text(f"{i}")
    await time_message.delete()
    await science1_all_questions(call, {}, state)


@dp.callback_query_handler(responses_callback_data.filter(), state=TestExecutionStates.science1)
async def science1_all_questions(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    user_resp = callback_data.get('response')
    simple_user = await db.select_simple_user(call.from_user.id)
    language = simple_user[2]
    data = await state.get_data()
    questions = data.get('questions')
    number = data.get('number')
    true_responses = data.get('true_responses')
    user_responses = data.get('user_responses')
    await state.update_data(
        {
            'user_responses': user_responses + user_resp if user_responses else f"{user_resp if user_resp else ''}",
        }
    )

    if user_resp:
        text_template = "{}\n\nВаш ответ: {}" if language != 'uz' else "{}\n\nSizning javobingiz: {}"
        try:
            await call.message.edit_caption(text_template.format(call.message.caption, user_resp).replace('<', '&lt'),
                                            reply_markup=None)
        except BadRequest:
            await call.message.edit_text(text_template.format(call.message.text, user_resp).replace('<', '&lt'),
                                         reply_markup=None)

    if not questions:
        data = await state.get_data()
        user_responses = data.get('user_responses')
        count = len(tuple(filter(lambda array: array[0] == array[1], zip(true_responses, user_responses))))
        if language == 'uz':
            await call.message.answer(f"Hozirgi kod uchun test yakunlandi. Natija: {count}",
                                      reply_markup=menu_markup_uz)
        else:
            await call.message.answer(f"Тест для текущего кода завершен. Результат: {count}",
                                      reply_markup=menu_markup_ru)
        await state.finish()
        return
    question = questions.pop(0)
    image = question[2]
    if language == 'uz':
        q_text = f"{number}-savol.\n\n{question[3].replace('<', '&lt')}"
    else:
        q_text = f"{number}-й вопрос.\n\n{question[3].replace('<', '&lt')}"
    true_resp = question[4]
    await state.update_data(
        {
            'true_responses': true_responses + true_resp if true_responses else f"{true_resp}",
            'questions': questions,
            'number': number + 1,
        }
    )

    if image:
        try:
            await call.message.answer_photo(image, q_text, reply_markup=await all_responses_inlines(language))
        except BadRequest:
            await call.message.answer(q_text, reply_markup=await all_responses_inlines(language))
    else:
        await call.message.answer(q_text, reply_markup=await all_responses_inlines(language))


@dp.message_handler(IsPrivate(), state=TestExecutionStates.all_states, content_types=ContentType.ANY)
async def err_msg_for_test_exe(msg: types.Message):
    await msg.delete()
