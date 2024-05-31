from typing import Union

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, ContentType

from data.config import ADMINS
from filters import IsPrivate
from keyboards.default import tests_menu_markup
from keyboards.inline import all_faculty_inlines_for_test, all_science_inlines_for_test, lang_inlines_for_test
from loader import dp, db
from states import AddTestStates


@dp.message_handler(IsPrivate(), text="➕ Yangi test qo'shish", user_id=ADMINS)
async def add_or_set_test(msg: Union[Message, CallbackQuery], state: FSMContext):
    if isinstance(msg, CallbackQuery):
        call = msg
    else:
        await msg.answer("Testning ta'lim yo'nalishini tanlang: ", reply_markup=await all_faculty_inlines_for_test())
    await state.set_state(AddTestStates.faculty)


@dp.callback_query_handler(state=AddTestStates.faculty)
async def choice_faculty(call: CallbackQuery, state: FSMContext):
    if call.data == 'close':
        await call.message.delete()
        await state.finish()
    else:
        await state.update_data({'directionOfEducation_id': call.data})
        await call.message.edit_text("Testning fanini tanlang: ", reply_markup=await all_science_inlines_for_test())
        await AddTestStates.next()


@dp.callback_query_handler(state=AddTestStates.science)
async def choice_science(call: CallbackQuery, state: FSMContext):
    if call.data == 'back':
        await call.message.edit_text("Testning ta'lim yo'nalishini tanlang: ",
                                     reply_markup=await all_faculty_inlines_for_test())
        await AddTestStates.previous()
    else:
        await state.update_data({'science_id': call.data})
        data = await state.get_data()
        faculty = await db.select_direction(data.get('directionOfEducation_id'))
        science = await db.select_science(call.data)
        await call.message.edit_text(f"<b>{faculty[1]}</b> ta'lim yo'nalishi, <b>{science[1]}</b> uchun",
                                     reply_markup=None)
        await call.message.answer("Testning savollar sonini kiriting: ", reply_markup=ReplyKeyboardRemove())
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
    await db.add_test(**data)
    await call.message.edit_text("✅Test muvaffaqiyatli qo'shildi!", reply_markup=None)
    await call.message.answer("🗃️ Testlar", reply_markup=tests_menu_markup)
    await state.finish()


@dp.message_handler(state=AddTestStates.all_states, content_types=ContentType.ANY)
async def error_add_test(msg: Message):
    await msg.delete()


@dp.message_handler(IsPrivate(), text="📂 Yo'nalishlar bo'yicha testlar", user_id=ADMINS)
async def show_faculties_for_test(msg: Message):
    pass
