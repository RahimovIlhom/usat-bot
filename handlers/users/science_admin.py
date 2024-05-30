from typing import Union

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, ContentType

from data.config import ADMINS
from filters import IsPrivate
from keyboards.default import tests_menu_markup
from keyboards.inline import science_list_markup, science_callback_data, science_show_markup, request_deletion_markup
from loader import dp, db
from states import ScienceAddStates


@dp.message_handler(IsPrivate(), text="🗃️ Testlar", user_id=ADMINS)
async def test_category(msg: Message):
    await msg.answer(msg.text, reply_markup=tests_menu_markup)


@dp.message_handler(IsPrivate(), text="📚 Fanlar ro'yxati", user_id=ADMINS)
async def science_list(msg: Union[Message, CallbackQuery]):
    if isinstance(msg, CallbackQuery):
        call = msg
        await call.message.edit_text("📚 Fanlar ro'yxati", reply_markup=await science_list_markup())
    else:
        await msg.answer(msg.text, reply_markup=await science_list_markup())


@dp.message_handler(IsPrivate(), text="➕ Yangi fan qo'shish", user_id=ADMINS)
async def add_or_set_science(msg: Union[Message, CallbackQuery], state: FSMContext, sc_id=None):
    if isinstance(msg, CallbackQuery):
        call = msg
        await call.message.edit_text("✏️ Fanni o'zgartirish", reply_markup=None)
        await call.message.answer("🇺🇿 Fan nomini o'zbek tilida kiriting:", reply_markup=ReplyKeyboardRemove())
    else:
        await msg.answer("🇺🇿 Fan nomini o'zbek tilida kiriting:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(ScienceAddStates.nameUz)
    await state.set_data({'science_id': sc_id})


@dp.message_handler(state=ScienceAddStates.nameUz)
async def science_name_uz(msg: Message, state: FSMContext):
    await state.update_data({'nameUz': msg.text})
    await msg.answer("🇷🇺 Fan nomini rus tilida kiriting:")
    await ScienceAddStates.next()


@dp.message_handler(state=ScienceAddStates.nameRu)
async def science_name_ru(msg: Message, state: FSMContext):
    await state.update_data({'nameRu': msg.text})
    data = await state.get_data()
    await db.add_or_update_science(**data)
    if not data.get('science_id'):
        await msg.answer("✅ Fan muvaffaqiyatli qo'shildi!", reply_markup=tests_menu_markup)
    else:
        await msg.answer("✅ Fan muvaffaqiyatli o'zgartirildi!", reply_markup=tests_menu_markup)
    await state.reset_data()
    await state.finish()


@dp.message_handler(state=ScienceAddStates.states, content_types=ContentType.ANY)
async def error_science_add(msg: Message):
    await msg.delete()


@dp.callback_query_handler(science_callback_data.filter())
async def select_sc_func(call: CallbackQuery, callback_data: dict, state: FSMContext):
    sc_id = callback_data.get('id')
    step = callback_data.get('step')
    action = callback_data.get('action')
    do = callback_data.get('do')

    if step == '0':
        await science_list(call)
    elif step == '1':
        await show_science(call, sc_id)
    elif step == '2':
        if action == 'edit':
            await add_or_set_science(call, state, sc_id)
        elif action == 'delete':
            if do == 'yes':
                await delete_science_func(call, sc_id)
            elif do == 'no':
                await show_science(call, sc_id)
            else:
                await request_deletion(call, sc_id)
    else:
        await call.message.delete()


async def show_science(call, sc_id):
    science = await db.select_science(sc_id)
    sc_info = (f"🇺🇿 Fan nomi: {science[1]}\n"
               f"🇷🇺 Имя субъекта: {science[2]}")
    await call.message.edit_text(sc_info, reply_markup=await science_show_markup(science[0]))


async def request_deletion(call, sc_id):
    msg_text = call.message.text
    answer_text = (f"‼️ Quyidagi fanni rostdan ham o'chirmoqchimisiz?\n\n"
                   f"{msg_text}")
    await call.message.edit_text(answer_text, reply_markup=await request_deletion_markup(sc_id))


async def delete_science_func(call, sc_id):
    await db.delete_science(sc_id)
    await call.message.edit_text("✅ Fan muvaffaqiyatli o'chirildi!", reply_markup=None)
    await call.message.answer("📚 Fanlar ro'yxati", reply_markup=await science_list_markup())
