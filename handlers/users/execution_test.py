import asyncio

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

        # if status in ('SUBMITTED', 'EXAMINED'):
        #     admission_applicant = await get_application_status_from_api(applicant[0])
        #     if admission_applicant:
        #         status = admission_applicant.get('applicationStatus')
        #         await db.update_application_status(applicant[0], status)

        if status not in status_to_key:
            await msg.answer(RESPONSE_TEXTS[language]['error'])
            return

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
            'sciences': sciences[1:],
            'questions': questions,
            'number': 0
        }
        await state.update_data(test_data)

        await call.message.edit_reply_markup(None)

        if language_text == 'uz':
            await call.message.answer(
                f"❕ Tayyorlaning, {science[1]} testi 10 soniyadan keyin boshlanadi.",
                reply_markup=ReplyKeyboardRemove()
            )
        else:
            await call.message.answer(
                f"❕ Подготовьтесь, тест {science[1]} начнется через 10 секунд.",
                reply_markup=ReplyKeyboardRemove()
            )

        await countdown(call, 10)
        await science_all_questions(call, {}, state)

    except Exception as e:
        await call.message.answer(f"An error occurred: {e}")
        await state.finish()


@dp.callback_query_handler(responses_callback_data.filter(), state=TestExecutionStates.science)
async def science_all_questions(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    user_resp = callback_data.get('response')
    simple_user = await db.select_simple_user(call.from_user.id)
    language = simple_user[2]
    data = await state.get_data()
    sciences = data.get('sciences')
    questions = data.get('questions')
    number = data.get('number')
    true_responses = data.get('true_responses')
    user_responses = data.get('user_responses')

    if user_resp:
        updated_user_responses = user_responses + user_resp if user_responses else f"{user_resp}"
        await state.update_data({'user_responses': updated_user_responses})
        await call.message.delete()

    if not questions:
        if sciences:
            await handle_new_test(call, state, simple_user, true_responses, sciences, data.get('languageOfEducation'))
        else:
            data = await state.get_data()
            user_responses = data.get('user_responses')
            await finish_test(call, state, language, true_responses, user_responses)
        return

    await ask_next_question(call, state, language, questions, number, true_responses)


async def handle_new_test(call, state, simple_user, true_responses, sciences, languageOfEducation):
    language = simple_user[2]
    science = sciences[0]
    await call.message.answer(
        f"❕ Tayyorlaning, {science[1]} testi 10 soniyadan keyin boshlanadi." if language == 'uz'
        else f"❕ Подготовьтесь, тест {science[1]} начнется через 10 секунд.",
        reply_markup=ReplyKeyboardRemove()
    )
    await countdown(call, 10)
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
            'sciences': sciences[1:],
            'true_responses': true_responses + question[4],
            'questions': questions[1:],
            'number': 1,
        }
    )
    await ask_question(call, language, question, 1)


async def finish_test(call, state, language, true_responses, user_responses):
    correct_answers = sum(1 for t, u in zip(true_responses, user_responses) if t == u)
    result = round((correct_answers / len(true_responses)) * 100, 2)
    applicantStatus = 'EXAMINED'
    await db.add_exam_result(call.from_user.id, result, correct_answers)
    await db.update_application_status(call.from_user.id, applicantStatus)
    RESPONSE_RESULT = {
        'uz': ("✅ Tabriklaymiz, siz imtihonni tugatdingiz!\n"
               "Natijangiz tekshirishga yuborildi"),
        'ru': ("✅ Поздравляем, вы завершили экзамен!\n"
               "Ваш результат отправлен на проверку")
    }

    await call.message.answer(
        RESPONSE_RESULT[language].format(correct_answers),
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
