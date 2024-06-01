from typing import Union

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, ContentType

from data.config import ADMINS
from filters import IsPrivate
from keyboards.default import tests_menu_markup
from keyboards.inline import all_science_inlines_for_test, lang_inlines_for_test, test_callback_data, \
    all_sciences_markup, tests_for_science_markup, test_markup, question_delete_test_markup
from loader import dp, db
from states import AddTestStates


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
        await call.message.edit_text("🗃️ Testlar", reply_markup=tests_menu_markup)
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
        await call.message.edit_text("✅Test muvaffaqiyatli o'zgartirildi!", reply_markup=None)
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
    if step == '0':
        await show_sciences_for_test(call)
    elif step == '1':
        await show_tests_for_science(call, science_id)
    elif step == '2':
        await show_test(call, test_id)
    elif step == '3':
        if action == 'add':
            pass
        elif action == 'list':
            pass
        elif action == 'edit':
            await add_or_set_test(call, state, test_id)
        elif action == 'delete':
            await question_delete_test(call, test_id)
    elif step == '4':
        if do == 'yes':
            await delete_test_func(call, science_id, test_id)
    else:
        await call.message.delete()


async def show_tests_for_science(call, sc_id):
    science = await db.select_science(sc_id)
    info = f"{science[1]} testlari:"
    await call.message.edit_text(info, reply_markup=await tests_for_science_markup(sc_id))


async def show_test(call, test_id):
    test = await db.select_test(test_id)
    info = (f"<b>{test[7]}</b> uchun test:\n\n"
            f"Test tili: {'🇺🇿' if test[3] == 'uz' else '🇷🇺'} {test[3]}\n"
            f"Savollar soni: {test[6]}/{test[2]}\n"
            f"Holat: {'✅ Active' if test[6] >= test[2] else '🚫 No active'}")

    await call.message.edit_text(info, reply_markup=await test_markup(test[0]))


async def question_delete_test(call, test_id):
    test = await db.select_test(test_id)
    info = (f"<b>{test[7]}</b> uchun test:\n\n"
            f"Test tili: {'🇺🇿' if test[3] == 'uz' else '🇷🇺'} {test[3]}\n"
            f"Savollar soni: {test[6]}/{test[2]}\n"
            f"Holat: {'✅ Active' if test[6] >= test[2] else '🚫 No active'}\n\n"
            f"Ushbu testni rostdan ham o'chirmoqchimisiz?")

    await call.message.edit_text(info, reply_markup=await question_delete_test_markup(test_id[0]))


async def delete_test_func(call, sc_id, test_id):
    await db.delete_test(test_id)
    await show_tests_for_science(call, sc_id)
    await call.message.answer("✅ Test muvaffaqiyatli o'chirildi!")
