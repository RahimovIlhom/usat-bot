from typing import Union

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, ContentType
from aiogram.utils.exceptions import BadRequest

from data.config import ADMINS
from filters import IsPrivate
from keyboards.default import tests_menu_markup, no_send_image_markup
from keyboards.inline import all_science_inlines_for_test, lang_inlines_for_test, test_callback_data, \
    all_sciences_markup, tests_for_science_markup, test_markup, question_delete_test_markup, questions_list_markup, \
    question_markup, question_delete_question_markup
from loader import dp, db
from states import AddTestStates, AddQuestionStates
from utils.misc.send_photo_telegraph import question_photo_link


@dp.message_handler(IsPrivate(), text="➕ Yangi test qo'shish", user_id=ADMINS)
async def add_or_set_test(msg: Union[Message, CallbackQuery], state: FSMContext, test_id=None):
    if isinstance(msg, CallbackQuery):
        call = msg
        await call.message.edit_text("Testning fanini tanlang:", reply_markup=await all_science_inlines_for_test())
    else:
        await msg.answer("Testning fanini tanlang: ", reply_markup=await all_science_inlines_for_test())
    await state.set_state(AddTestStates.science)
    await state.set_data({'id': test_id})


@dp.callback_query_handler(state=AddTestStates.science)
async def choice_science(call: CallbackQuery, state: FSMContext):
    if call.data == 'close':
        await call.message.delete()
        await call.message.answer("🗃️ Testlar", reply_markup=tests_menu_markup)
        await state.finish()
    else:
        await state.update_data({'science_id': call.data})
        science = await db.select_science(call.data)
        await call.message.edit_text(f"✅ <b>{science[1]}</b>", reply_markup=None)
        await call.message.answer("Testning nechta savollari abituriyentga uzatiladi? ",
                                  reply_markup=ReplyKeyboardRemove())
        await AddTestStates.next()


@dp.message_handler(state=AddTestStates.count, regexp=r"^(100|[1-9]?[0-9])$")
async def handle_count(message: Message, state: FSMContext):
    await state.update_data({'questionsCount': int(message.text)})
    await message.answer("Test tilini tanlang: ", reply_markup=lang_inlines_for_test)
    await AddTestStates.next()


@dp.callback_query_handler(state=AddTestStates.language)
async def handle_lang_for_test(call: CallbackQuery, state: FSMContext):
    await state.update_data({'language': call.data})
    data = await state.get_data()
    if data.get('id'):
        await db.update_test(**data)
        await call.message.answer("✅Test muvaffaqiyatli o'zgartirildi!", reply_markup=tests_menu_markup)
        await show_test(call, data.get('id'))
    else:
        await db.add_test(**data)
        await call.message.edit_text("✅Test muvaffaqiyatli qo'shildi!", reply_markup=None)
        await call.message.answer("🗃️ Testlar", reply_markup=tests_menu_markup)
    await state.finish()


@dp.message_handler(state=AddTestStates.all_states, content_types=ContentType.ANY)
async def error_add_test(msg: Message):
    await msg.delete()


@dp.message_handler(IsPrivate(), text="📂 Fanlar bo'yicha testlar", user_id=ADMINS)
async def show_sciences_for_test(msg: Union[Message, CallbackQuery]):
    if isinstance(msg, CallbackQuery):
        call = msg
        await call.message.edit_text("📂 Fanlar bo'yicha testlar", reply_markup=await all_sciences_markup())
    else:
        await msg.answer(msg.text, reply_markup=await all_sciences_markup())


@dp.callback_query_handler(test_callback_data.filter())
async def select_test_func(call: CallbackQuery, callback_data: dict, state: FSMContext):
    science_id = callback_data.get('science')
    test_id = callback_data.get('test')
    step = callback_data.get('step')
    action = callback_data.get('action')
    do = callback_data.get('do')
    ques_id = callback_data.get('ques_id')
    if step == '0':
        await show_sciences_for_test(call)
    elif step == '1':
        await show_tests_for_science(call, science_id)
    elif step == '2':
        await show_test(call, test_id)
    elif step == '3':
        if action == 'add':
            await add_or_set_question(call, test_id, state)
        elif action == 'list':
            await questions_list_for_test(call, science_id, test_id)
        elif action == 'edit':
            await add_or_set_test(call, state, test_id)
        elif action == 'delete':
            await question_delete_test(call, test_id)
    elif step == '4':
        if do == 'yes':
            await delete_test_func(call, science_id, test_id)
        elif ques_id != '0':
            await show_question_for_test(call, ques_id)
    elif step == '5':
        if action == 'delete':
            await question_delete_question(call, ques_id)
        elif action == 'edit':
            await add_or_set_question(call, test_id, state, ques_id)
    elif step == '6':
        if do == 'yes':
            await delete_question_func(call, science_id, test_id, ques_id)
    else:
        await call.message.delete()


async def show_tests_for_science(call, sc_id):
    science = await db.select_science(sc_id)
    info = f"{science[1]} testlari:"
    await call.message.edit_text(info, reply_markup=await tests_for_science_markup(sc_id))


async def show_test(call: Union[Message, CallbackQuery], test_id):
    test = await db.select_test(test_id)
    info = (f"<b>{test[7]}</b> uchun test:\n\n"
            f"Test tili: {'🇺🇿' if test[3] == 'uz' else '🇷🇺'} {test[3]}\n"
            f"Savollar soni: {test[6]}/{test[2]}\n"
            f"Holat: {'✅ Active' if test[4] else '🚫 No active'}")

    if isinstance(call, Message):
        msg = call
        await msg.answer(info, reply_markup=await test_markup(test[0]))
    else:
        await call.message.edit_text(info, reply_markup=await test_markup(test[0]))


async def question_delete_test(call, test_id):
    test = await db.select_test(test_id)
    info = (f"<b>{test[7]}</b> uchun test:\n\n"
            f"Test tili: {'🇺🇿' if test[3] == 'uz' else '🇷🇺'} {test[3]}\n"
            f"Savollar soni: {test[6]}/{test[2]}\n"
            f"Holat: {'✅ Active' if test[4] else '🚫 No active'}\n\n"
            f"Ushbu testni rostdan ham o'chirmoqchimisiz?")

    await call.message.edit_text(info, reply_markup=await question_delete_test_markup(test[0]))


async def question_delete_question(call, question_id):
    result = await db.select_question(question_id)
    text = (f"Fan: {result[7]}\n"
            f"Savol tili: {'🇺🇿 Uz' if result[6] == 'uz' else '🇷🇺 Ru'}\n\n"
            f"Savol:\n{result[3].replace('<', '&lt')}\n\n"
            f"To'g'ri javob: {result[4]}")
    try:
        await call.message.edit_caption(text, reply_markup=await question_delete_question_markup(result[5], result[1],
                                                                                                 question_id))
    except BadRequest:
        await call.message.edit_text(text, reply_markup=await question_delete_question_markup(result[5], result[1],
                                                                                              question_id))


async def delete_test_func(call, sc_id, test_id):
    await db.delete_test(test_id)
    await show_tests_for_science(call, sc_id)
    await call.message.answer("✅ Test muvaffaqiyatli o'chirildi!")


async def delete_question_func(call, sc_id, test_id, ques_id):
    await db.delete_question(ques_id, test_id)
    await questions_list_for_test(call, sc_id, test_id)
    await call.message.answer("✅ Savol muvaffaqiyatli o'chirildi!")


async def add_or_set_question(call, test_id, state, question_id=None):
    test = await db.select_test(test_id)
    await state.set_data({'test_id': test_id, 'question_id': question_id, 'language': test[3]})
    lang_text = f"🇺🇿 O'zbek tilida, " if test[3] == 'uz' else f"🇷🇺 Rus tilida, "
    if question_id:
        if call.message.text:
            await call.message.edit_text(call.message.text + "\n\n✏️ Savolni o'zgartirish", reply_markup=None)
        elif call.message.caption:
            await call.message.edit_caption(call.message.caption + "\n\n✏️ Savolni o'zgartirish", reply_markup=None)
    else:
        await call.message.edit_text(lang_text + f"➕ {test[7]} uchun savol qo'shish", reply_markup=None)
    await call.message.answer("Savol rasmini yuboring:", reply_markup=no_send_image_markup)
    await state.set_state(AddQuestionStates.image)


@dp.message_handler(state=AddQuestionStates.image, text="Rasm mavjud emas!")
async def no_send_image_question(msg: Message, state: FSMContext):
    data = await state.get_data()
    await state.update_data({'image': None})
    lang_text = f"🇺🇿 O'zbek tilida, " if data['language'] == 'uz' else f"🇷🇺 Rus tilida, "
    # text = ("savolni yuboring (variantlari bilan!)\n\nOxirgi qismda to'g'ri variantni raqam orqali "
    #         "ifodalang.\nTo'g'ri javob raqamlari: 1 - A, 2 - B, 3 - C, 4 - D.")
    text = "savolni yuboring"
    await msg.answer(lang_text + text, reply_markup=ReplyKeyboardRemove())
    await AddQuestionStates.next()


@dp.message_handler(state=AddQuestionStates.image, content_types=ContentType.PHOTO)
async def send_image_question(msg: Message, state: FSMContext):
    data = await state.get_data()
    photo = msg.photo[-1]
    image_url = await question_photo_link(photo)
    await state.update_data({'image': image_url})
    lang_text = f"🇺🇿 O'zbek tilida, " if data['language'] == 'uz' else f"🇷🇺 Rus tilida, "
    # text = ("savolni yuboring (variantlari bilan!)\n\nOxirgi qismda to'g'ri variantni raqam orqali "
    #         "ifodalang.\nTo'g'ri javob raqamlari: 1 - A, 2 - B, 3 - C, 4 - D.")
    text = "savolni yuboring"
    await msg.answer(lang_text + text, reply_markup=ReplyKeyboardRemove())
    await AddQuestionStates.next()


# @dp.message_handler(state=AddQuestionStates.question, content_types=ContentType.TEXT)
# async def send_question_text(msg: Message, state: FSMContext):
#     question_text = msg.text[0:-1:1]
#     true_resp_dict = {'1': 'a', '2': 'b', '3': 'c', '4': 'd'}
#     true_resp = true_resp_dict.get(msg.text[-1], None)
#     if not true_resp:
#         await msg.answer("‼️ Xatolik, to'g'ri javob ko'rsatilmagan. Iltimos, savolni qayta yuboring:")
#         return
#     await state.update_data({'question': question_text, 'trueResponse': true_resp})
#     data = await state.get_data()
#     resp = await db.add_or_update_question(**data)
#     if resp == 'add':
#         await msg.answer("✅ Savol muvaffaqiyatli qo'shildi!", reply_markup=tests_menu_markup)
#     else:
#         await msg.answer("✅ Savol muvaffaqiyatli o'zgartirildi!", reply_markup=tests_menu_markup)
#     await state.finish()
#     await show_test(call=msg, test_id=data.get('test_id'))


@dp.message_handler(state=AddQuestionStates.question, content_types=ContentType.TEXT)
async def send_question_text(msg: Message, state: FSMContext):
    question_text = msg.text
    await state.update_data({'question': question_text, 'trueResponse': 'a'})
    await msg.answer("1-variantni yuboring (1-varint to'g'ri javob sifatida qanul qilinadi!)")
    await AddQuestionStates.next()


@dp.message_handler(state=AddQuestionStates.response1, content_types=ContentType.TEXT)
async def send_question_response1(msg: Message, state: FSMContext):
    true_resp = msg.text
    await state.update_data({'response1': true_resp})
    await msg.answer("2-variantni yuboring")
    await AddQuestionStates.next()


@dp.message_handler(state=AddQuestionStates.response2, content_types=ContentType.TEXT)
async def send_question_response1(msg: Message, state: FSMContext):
    true_resp = msg.text
    await state.update_data({'response2': true_resp})
    await msg.answer("3-variantni yuboring")
    await AddQuestionStates.next()


@dp.message_handler(state=AddQuestionStates.response3, content_types=ContentType.TEXT)
async def send_question_response1(msg: Message, state: FSMContext):
    true_resp = msg.text
    await state.update_data({'response3': true_resp})
    await msg.answer("4-variantni yuboring")
    await AddQuestionStates.next()


@dp.message_handler(state=AddQuestionStates.response4, content_types=ContentType.TEXT)
async def send_question_response1(msg: Message, state: FSMContext):
    true_resp = msg.text
    await state.update_data({'response4': true_resp})
    data = await state.get_data()
    resp = await db.add_or_update_question(**data)
    if resp == 'add':
        await msg.answer("✅ Savol muvaffaqiyatli qo'shildi!", reply_markup=tests_menu_markup)
    else:
        await msg.answer("✅ Savol muvaffaqiyatli o'zgartirildi!", reply_markup=tests_menu_markup)
    await state.finish()
    await show_test(call=msg, test_id=data.get('test_id'))


async def questions_list_for_test(call, science_id, test_id):
    test = await db.select_test(test_id)
    info = (f"<b>{test[7]}</b> uchun test:\n\n"
            f"Test tili: {'🇺🇿' if test[3] == 'uz' else '🇷🇺'} {test[3]}\n"
            f"Savollar soni: {test[6]}/{test[2]}\n"
            f"Holat: {'✅ Active' if test[4] else '🚫 No active'}\n\n"
            f"Test savollar ro'yxati:")
    try:
        await call.message.edit_text(info, reply_markup=await questions_list_markup(science_id, test_id))
    except BadRequest:
        await call.message.delete()
        await call.message.answer(info, reply_markup=await questions_list_markup(science_id, test_id))


async def show_question_for_test(call, ques_id):
    result = await db.select_question(ques_id)
    text = (f"Fan: {result[7]}\n"
            f"Savol tili: {'🇺🇿 Uz' if result[6] == 'uz' else '🇷🇺 Ru'}\n\n"
            f"Savol:\n{result[3].replace('<', '&lt')}\n"
            f"A) {result[8].replace('<', '&lt')}\n"
            f"B) {result[9].replace('<', '&lt')}\n"
            f"C) {result[10].replace('<', '&lt')}\n"
            f"D) {result[11].replace('<', '&lt')}\n\n"
            f"To'g'ri javob: {result[4]}")
    if result[2]:
        try:
            await call.message.edit_caption(caption=text,
                                            reply_markup=await question_markup(result[5], result[1], ques_id))
        except BadRequest:
            await call.message.delete()
            await call.message.answer_photo(result[2], caption=text,
                                            reply_markup=await question_markup(result[5], result[1], ques_id))
    else:
        await call.message.edit_text(text, reply_markup=await question_markup(result[5], result[1], ques_id))
