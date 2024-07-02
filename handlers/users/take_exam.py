import asyncio
from datetime import datetime
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, ReplyKeyboardRemove
from aiogram.utils.exceptions import BadRequest
from data import RESPONSE_TEXTS
from filters import IsPrivate
from keyboards.default import menu_markup_uz, menu_markup_ru
from keyboards.inline import ready_inline_button, responses_callback_data, all_responses_inlines, ready_callback_data
from loader import dp, db
from states import TestExecutionStates
from utils.db_api import get_applicant_in_admission

SCORE_MAP = {
    1: 3.1,
    2: 2.1,
    3: 1.1,
    4: 0
}


@dp.message_handler(IsPrivate(), text=["🧑‍💻 Imtihon topshirish", "🧑‍💻 Сдать экзамен"])
async def check_execution_text(msg: types.Message):
    try:
        applicant = await db.get_applicant(msg.from_user.id)
        language = 'uz' if msg.text == '🧑‍💻 Imtihon topshirish' else 'ru'
        permission = False

        if not applicant:
            await msg.answer(RESPONSE_TEXTS[language]['need_application'])
            return

        status = applicant[14]
        status_to_key = {
            'DRAFT': 'draft',
            'SUBMITTED': 'submitted',
            'REJECTED': 'rejected',
            'PASSED': 'passed',
            'ACCEPTED': 'welcome_message',
            'FAILED': 'failed',
            'EXAMINED': 'examined'
        }

        if status not in status_to_key:
            await msg.answer(RESPONSE_TEXTS[language]['error'])
            return

        if status in ['SUBMITTED', 'EXAMINED', 'REJECTED']:
            user_data_resp = await get_applicant_in_admission(msg.from_user.id)
            if user_data_resp.status_code == 200:
                status = user_data_resp.json().get('status')
                await db.update_application_status(msg.from_user.id, status)

        if status == 'FAILED':
            results = await db.get_applicant_exam_results(msg.from_user.id)
            if len(results) >= 2:
                await msg.answer(RESPONSE_TEXTS[language]['two_failed'])
                return

        if status in ('ACCEPTED', 'FAILED'):
            sciences = await db.get_sciences_for_exam(applicant[8])
            if not sciences:
                await msg.answer(RESPONSE_TEXTS[language]['no_exam_questions'])
                return

            sciences_info = "\nFanlar ro'yxati va savollar soni:\n" \
                if language == 'uz' else '\nСписок предметов и количество вопросов:\n'
            all_count = 0
            ready = True

            for i, sc in enumerate(sciences, start=1):
                tests = await db.select_active_tests_for_science(sc[0], applicant[10])
                questions_count = sum(test[2] for test in tests)
                if not tests:
                    ready = False
                    break
                all_count += questions_count
                if language == 'uz':
                    sciences_info += f"{i}. {sc[1]} - {questions_count} ta savol\n"
                else:
                    sciences_info += f"{i}. {sc[2]} - {questions_count} вопросов\n"

            if ready:
                resp_text = (RESPONSE_TEXTS[language][status_to_key[status]].format(len(sciences), all_count) +
                             sciences_info)
                permission = True
            else:
                resp_text = RESPONSE_TEXTS[language]['no_exam_questions']
        else:
            resp_text = RESPONSE_TEXTS[language][status_to_key[status]]

        message = await msg.answer(resp_text)
        if permission:
            await message.edit_reply_markup(await ready_inline_button(language))

    except Exception as e:
        await msg.answer(f"An error occurred: {e}")


@dp.callback_query_handler(ready_callback_data.filter())
async def you_are_ready(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    do = callback_data.get('do')
    language_text = callback_data.get('lang')
    if not do:
        await call.message.delete()
        return
    try:
        start_time = datetime.now()  # Imtihon boshlanish vaqti
        await state.set_state(TestExecutionStates.science)
        applicant = await db.get_applicant(call.from_user.id)
        languageOfEducation = applicant[10]
        direction_id = applicant[8]
        sciences = await db.get_sciences_for_exam(direction_id)

        science = sciences[0]
        tests = await db.select_active_tests_for_science(science[0], languageOfEducation)
        if not tests:
            await call.message.answer("No active tests available.")
            return

        questions = []
        for test in tests:
            questions.extend(await db.select_questions_for_test(test[0], test[2]))

        test_data = {
            'languageOfEducation': languageOfEducation,
            'language_text': language_text,
            'sciences': sciences[1:],
            'science_id': science[0],
            'science_number': 1,
            'questions': questions,
            'question_id': questions[0][0],
            'number': 0,
            'true_responses': [],
            'user_responses': [],
            'scores': [],
            'start_time': start_time
        }
        await state.update_data(test_data)

        await call.message.edit_reply_markup(None)

        msg = await call.message.answer(
            f"❕ Tayyorlaning, {science[1]} testi 10 soniyadan keyin boshlanadi." if language_text == 'uz'
            else f"❕ Подготовьтесь, тест {science[1]} начнется через 10 секунд.",
            reply_markup=ReplyKeyboardRemove()
        )

        # await countdown(call, 10)
        await msg.delete()
        await science_all_questions(call, {}, state)

    except Exception as e:
        await call.message.answer(f"An error occurred: {e}")
        await state.finish()


@dp.callback_query_handler(responses_callback_data.filter(), state=TestExecutionStates.science)
async def science_all_questions(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    user_resp = callback_data.get('response')
    data = await state.get_data()
    language_text = data.get('language_text')
    sciences = data.get('sciences')
    science_id = data.get('science_id')
    science_number = data.get('science_number')
    questions = data.get('questions')
    question_id = data.get('question_id')
    number = data.get('number')
    true_responses = data.get('true_responses')
    user_responses = data.get('user_responses')
    scores = data.get('scores')
    start_time = data.get('start_time')
    elapsed_time = (datetime.now() - start_time).total_seconds() / 60  # minutes

    if elapsed_time > 240:
        await call.message.delete()
        await call.message.answer(RESPONSE_TEXTS[language_text]['time_up'])
        await finish_test(call, state, language_text, true_responses, user_responses, scores, elapsed_time,
                          science_id, questions, sciences)
        return

    if user_resp:
        score = SCORE_MAP.get(science_number, 4)

        user_response_data = {
            "science_id": science_id,
            "question_id": question_id,
            "true_response": true_responses[number - 1],
            "user_response": user_resp,
            "score": score
        }

        if user_resp == true_responses[number - 1]:
            scores.append(score)
        else:
            scores.append(0)

        updated_user_responses = user_responses + [user_response_data] if user_responses else [user_response_data]
        await state.update_data({'user_responses': updated_user_responses,
                                 'scores': scores})
        await call.message.delete()

    if not questions:
        if sciences:
            await handle_new_test(call, state, language_text, true_responses, sciences, data.get('languageOfEducation'),
                                  science_number)
        else:
            data = await state.get_data()
            user_responses = data.get('user_responses')
            await finish_test(call, state, language_text, true_responses, user_responses, scores, elapsed_time)
        return

    await ask_next_question(call, state, language_text, questions, number, true_responses)


async def handle_new_test(call, state, language_text, true_responses, sciences, languageOfEducation, science_number):
    science = sciences[0]
    msg = await call.message.answer(
        f"❕ Tayyorlaning, {science[1]} testi 10 soniyadan keyin boshlanadi." if language_text == 'uz'
        else f"❕ Подготовьтесь, тест {science[1]} начнется через 10 секунд.",
        reply_markup=ReplyKeyboardRemove()
    )
    # await countdown(call, 10)
    await msg.delete()
    tests = await db.select_active_tests_for_science(science[0], languageOfEducation)
    if not tests:
        await call.message.answer("No active tests available.")
        return

    questions = []
    for test in tests:
        questions.extend(await db.select_questions_for_test(test[0], test[2]))
    question = questions[0]

    await state.update_data(
        {
            'science_id': science[0],
            'sciences': sciences[1:],
            'science_number': science_number + 1,
            'true_responses': true_responses + [question[4]],
            'questions': questions[1:],
            'number': 1,
        }
    )
    await ask_question(call, language_text, question, 1)


async def finish_test(call, state, language, true_responses, user_responses, scores, elapsed_time,
                      science_id=None, questions=None, sciences=None):
    data = await state.get_data()
    languageOfEducation = data.get('languageOfEducation')
    if science_id:
        for question in questions:
            user_responses.append({
                "science_id": science_id,
                "question_id": question[0],
                "true_response": question[4],
                "user_response": '',
                "score": 0
            })
        if sciences:
            for science in sciences:
                tests = await db.select_active_tests_for_science(science[0], languageOfEducation)
                questions = []
                for test in tests:
                    questions.extend(await db.select_questions_for_test(test[0], test[2]))
                for question in questions:
                    user_responses.append({
                        "science_id": science[0],
                        "question_id": question[0],
                        "true_response": question[4],
                        "user_response": '',
                        "score": 0
                    })
    user_defined_options = ''.join(item['user_response'] for item in user_responses)
    correct_answers = sum(1 for t, u in zip(true_responses, user_defined_options) if t == u)
    result = round((correct_answers / len(true_responses)) * 100, 2)
    applicantStatus = 'EXAMINED'
    total_score = round(sum(scores), 1)
    interval_time = round(elapsed_time, 2)

    await db.add_exam_result(call.from_user.id, correct_answers, result, total_score, user_responses, interval_time)
    await db.update_application_status(call.from_user.id, applicantStatus)
    RESPONSE_RESULT = {
        'uz': ("✅ Tabriklaymiz, siz imtihonni tugatdingiz!\n"
               "Natijangiz tekshirishga yuborildi. Umumiy ball: {}"),
        'ru': ("✅ Поздравляем, вы завершили экзамен!\n"
               "Ваш результат отправлен на проверку. Общий балл: {}")
    }

    await call.message.answer(
        RESPONSE_RESULT[language].format(total_score),
        reply_markup=menu_markup_uz if language == 'uz' else menu_markup_ru
    )
    await state.finish()


async def ask_next_question(call, state, language, questions, number, true_responses):
    question = questions[0]
    await state.update_data(
        {
            'question_id': question[0],
            'true_responses': true_responses + [question[4]],
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
