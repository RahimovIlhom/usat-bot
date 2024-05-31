from typing import Union

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, ContentType

from data.config import ADMINS
from filters import IsPrivate
from keyboards.default import tests_menu_markup
from keyboards.inline import all_science_inlines_for_test, lang_inlines_for_test, test_callback_data, \
    all_sciences_markup
from loader import dp, db
from states import AddTestStates


@dp.message_handler(IsPrivate(), text="➕ Yangi test qo'shish", user_id=ADMINS)
async def add_or_set_test(msg: Union[Message, CallbackQuery], state: FSMContext):
    if isinstance(msg, CallbackQuery):
        call = msg
    else:
        await msg.answer("Testning fanini tanlang: ", reply_markup=await all_science_inlines_for_test())
    await state.set_state(AddTestStates.science)


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
    await db.add_test(**data)
    await call.message.edit_text("✅Test muvaffaqiyatli qo'shildi!", reply_markup=None)
    await call.message.answer("🗃️ Testlar", reply_markup=tests_menu_markup)
    await state.finish()


@dp.message_handler(state=AddTestStates.all_states, content_types=ContentType.ANY)
async def error_add_test(msg: Message):
    await msg.delete()


@dp.message_handler(IsPrivate(), text="📂 Fanlar bo'yicha testlar", user_id=ADMINS)
async def show_faculties_for_test(msg: Union[Message, CallbackQuery]):
    if isinstance(msg, CallbackQuery):
        call = msg
    else:
        await msg.answer(msg.text, reply_markup=await all_sciences_markup())


@dp.callback_query_handler(test_callback_data.filter())
async def select_test_func(call: CallbackQuery, callback_data: dict, state: FSMContext):
    pass
