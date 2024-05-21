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
    try:
        applicant = await db.get_applicant(msg.from_user.id)
        simple_user = await db.select_simple_user(msg.from_user.id)
        language = simple_user[2]
        permission = False

        response_texts = {
            'uz': {
                'already_examined': "❗️ Siz allaqachon imtihon topshirib bo'lgansiz!",
                'no_exam_questions': "❗️ Hozirda imtihon savollari mavjud emas!",
                'welcome_message': ("Fan va texnologiyalar universitetining kirish imtihonlari tizimiga xush kelibsiz! "
                                    "Siz 2 ta fandan 25 tadan savolga va 10 ta mantiqiy savolga to'g'ri javob "
                                    "berishingiz kerak bo'ladi. Mummify 60 ta test savollari uchun 4 soat vaqt "
                                    "beriladi.\nTayyormisiz?"),
                'need_application': "❗️ Imtihon topshirish uchun avval Universitetga hujjat topshirishingiz kerak!"
            },
            'ru': {
                'already_examined': "❗️ Вы уже сдали экзамен!",
                'no_exam_questions': "❗️ В настоящее время экзаменационные вопросы отсутствуют!",
                'welcome_message': ("Добро пожаловать в систему вступительных экзаменов Университета науки и "
                                    "технологий! Вам нужно будет правильно ответить на 25 вопросов по двум предметам "
                                    "и на 10 логических вопросов. На выполнение 60 тестовых вопросов дается 4 "
                                    "часа.\nВы готовы?"),
                'need_application': "❗️ Для сдачи экзамена вам сначала нужно подать документы в университет!"
            }
        }

        if applicant:
            exam_result = await db.get_exam_result(msg.from_user.id)
            if exam_result:
                resp_text = response_texts[language]['already_examined']
            else:
                active_tests = await db.select_active_tests_for_faculty(applicant[7], applicant[9])
                if len(active_tests) != 3:
                    resp_text = response_texts[language]['no_exam_questions']
                else:
                    resp_text = response_texts[language]['welcome_message']
                    permission = True
        else:
            resp_text = response_texts[language]['need_application']

        message = await msg.answer(resp_text)
        if permission:
            await message.edit_reply_markup(await ready_inline_button(language))

    except Exception as e:
        await msg.answer(f"An error occurred: {e}")


@dp.callback_query_handler(text='ready')
async def you_are_ready(call: types.CallbackQuery, state: FSMContext):
    try:
        await state.set_state(TestExecutionStates.science)

        simple_user = await db.select_simple_user(call.from_user.id)
        applicant = await db.get_applicant(call.from_user.id)
        direction_id = applicant[7]

        tests = await db.select_active_tests_for_faculty(direction_id, applicant[9])
        if not tests:
            await call.message.answer("No active tests available.")
            return

        test = tests[0]
        questions = await db.select_questions_for_test(test[0])

        test_data = {
            'all_tests': tests[1:],
            'test': test,
            'questions': questions,
            'number': 0
        }
        await state.update_data(test_data)

        await call.message.edit_reply_markup(None)

        language = simple_user[2]
        if language == 'uz':
            await call.message.answer(
                f"{test[3]} fanidan test savollari. Tayyorlaning, imtixon 10 soniyadan keyin boshlanadi.",
                reply_markup=ReplyKeyboardRemove()
            )
        else:
            await call.message.answer(
                f"Тестовые вопросы по предмету {test[4]}. Подготовьтесь, экзамен начнется через 10 секунд.",
                reply_markup=ReplyKeyboardRemove()
            )

        await countdown(call, 10)
        await science_all_questions(call, {}, state)

    except Exception as e:
        await call.message.answer(f"An error occurred: {e}")


@dp.callback_query_handler(responses_callback_data.filter(), state=TestExecutionStates.science)
async def science_all_questions(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    user_resp = callback_data.get('response')
    simple_user = await db.select_simple_user(call.from_user.id)
    language = simple_user[2]
    data = await state.get_data()
    all_tests = data.get('all_tests')
    questions = data.get('questions')
    number = data.get('number')
    true_responses = data.get('true_responses')
    user_responses = data.get('user_responses')

    if user_resp:
        updated_user_responses = user_responses + user_resp if user_responses else f"{user_resp}"
        await state.update_data({'user_responses': updated_user_responses})
        text_template = "{}\n\nВаш ответ: {}" if language != 'uz' else "{}\n\nSizning javobingiz: {}"
        try:
            await call.message.edit_caption(
                text_template.format(call.message.caption, user_resp).replace('<', '&lt'),
                reply_markup=None
            )
        except BadRequest:
            await call.message.edit_text(
                text_template.format(call.message.text, user_resp).replace('<', '&lt'),
                reply_markup=None
            )

    if not questions:
        if all_tests:
            await handle_new_test(call, state, simple_user, all_tests, true_responses)
        else:
            data = await state.get_data()
            user_responses = data.get('user_responses')
            await finish_test(call, state, language, true_responses, user_responses)
        return

    await ask_next_question(call, state, language, questions, number, true_responses)


async def handle_new_test(call, state, simple_user, all_tests, true_responses):
    language = simple_user[2]
    test = all_tests[0]
    await call.message.answer(
        f"{test[3]} fanidan test savollari. Tayyorlaning, imtixon 10 soniyadan keyin boshlanadi." if language == 'uz'
        else f"Тестовые вопросы по предмету {test[4]}. Подготовьтесь, экзамен начнется через 10 секунд.",
        reply_markup=ReplyKeyboardRemove()
    )
    await countdown(call, 10)
    questions = await db.select_questions_for_test(test[0])
    question = questions[0]
    await state.update_data(
        {
            'all_tests': all_tests[1:],
            'test': test,
            'true_responses': true_responses + question[4],
            'questions': questions[1:],
            'number': 1,
        }
    )
    await ask_question(call, language, question, 1)


async def finish_test(call, state, language, true_responses, user_responses):
    correct_answers = sum(1 for t, u in zip(true_responses, user_responses) if t == u)
    print(true_responses)
    print(user_responses)
    await call.message.answer(
        f"Hozirgi kod uchun test yakunlandi. Natija: {correct_answers}" if language == 'uz'
        else f"Тест для текущего кода завершен. Результат: {correct_answers}",
        reply_markup=menu_markup_uz if language == 'uz' else menu_markup_ru
    )
    await state.finish()


async def ask_next_question(call, state, language, questions, number, true_responses):
    question = questions[0]
    await state.update_data(
        {
            'true_responses': true_responses + question[4] if true_responses else f"{question[4]}",
            'questions': questions[1:],
            'number': number + 1,
        }
    )
    await ask_question(call, language, question, number + 1)


async def ask_question(call, language, question, number):
    image = question[2]
    question_text = f"{number}-savol.\n\n{question[3].replace('<', '&lt')}" if language == 'uz' else \
                    f"{number}-й вопрос.\n\n{question[3].replace('<', '&lt')}"
    try:
        if image:
            await call.message.answer_photo(image, question_text, reply_markup=await all_responses_inlines(language))
        else:
            await call.message.answer(question_text, reply_markup=await all_responses_inlines(language))
    except BadRequest:
        await call.message.answer(question_text, reply_markup=await all_responses_inlines(language))


async def countdown(call, seconds):
    time_message = await call.message.answer(f"{seconds}")
    for i in range(seconds - 1, -1, -1):
        await asyncio.sleep(1)
        await time_message.edit_text(f"{i}")
    await time_message.delete()


@dp.message_handler(IsPrivate(), state=TestExecutionStates.all_states, content_types=ContentType.ANY)
async def err_msg_for_test_exe(msg: types.Message):
    await msg.delete()
