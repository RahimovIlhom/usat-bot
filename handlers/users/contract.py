from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from data.config import ADMINS
from filters import IsPrivate
from keyboards.default import directions_menu_markup, types_of_education_menu_markup
from keyboards.inline import all_directions_inlines, directions_callback_data, all_types_of_edu_inlines, \
    types_callback_data, type_of_edu_inlines, delete_type_of_edu_inlines, direction_inlines, delete_direction_inlines
from loader import dp, db
from states import AddDirectionStates, TypesOfEduStates


@dp.message_handler(IsPrivate(), text="Barcha yo'nalishlar", user_id=ADMINS)
async def all_directions_branch(msg: Union[types.Message, types.CallbackQuery]):
    if isinstance(msg, types.CallbackQuery):
        call = msg
        await call.message.edit_text("Barcha yo'nalishlar", reply_markup=await all_directions_inlines())
    else:
        await msg.answer(msg.text, reply_markup=await all_directions_inlines())


@dp.message_handler(IsPrivate(), text="Yo'nalish qo'shish", user_id=ADMINS)
async def add_or_set_direction_branch(msg: Union[types.Message, types.CallbackQuery], state: FSMContext,
                                      direction_id: int = None):
    if isinstance(msg, types.CallbackQuery):
        call = msg
        await call.message.edit_text("❗️ Ta'lim yo'nalishini o'zgartirmoqdasiz!", reply_markup=None)
        await call.message.answer("Ta'lim yo'nalishi nomini o'zbek tilida kiriting:",
                                  reply_markup=ReplyKeyboardRemove())
    else:
        await msg.answer("Ta'lim yo'nalishi nomini o'zbek tilida kiriting:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddDirectionStates.nameUz)
    await state.set_data({'id': direction_id})


@dp.message_handler(state=AddDirectionStates.nameUz, user_id=ADMINS)
async def add_direction_uz(msg: types.Message, state: FSMContext):
    await state.update_data({'nameUz': msg.text})
    await msg.answer("Ta'lim yo'nalishi nomini rus tilida kiriting:", reply_markup=ReplyKeyboardRemove())
    await AddDirectionStates.next()


@dp.message_handler(state=AddDirectionStates.nameRu, user_id=ADMINS)
async def add_direction_ru(msg: types.Message, state: FSMContext):
    await state.update_data({'nameRu': msg.text})
    data = await state.get_data()
    await db.add_or_set_direction(**data)
    if data.get('id'):
        info = "✅ Ta'lim yo'nalishi muvaffaqiyatli o'zgartirildi"
    else:
        info = "✅ Ta'lim yo'nalishi qo'shildi"
    await msg.answer(info, reply_markup=directions_menu_markup)
    await state.finish()


@dp.callback_query_handler(IsPrivate(), directions_callback_data.filter(), user_id=ADMINS)
async def show_direction(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    direction_id = callback_data.get('id')
    action = callback_data.get('action')
    do = callback_data.get('do')
    if direction_id == 'close':
        await call.message.delete()
    elif action == 'read':
        await show_direction_of_edu(call, direction_id)
    elif action == 'back':
        await all_directions_branch(call)
    elif action == "delete":
        if do == 'yes':
            await db.delete_direction(direction_id)
            await call.message.edit_text("✅ Ta'lim yo'nalishi muvaffaqiyatli o'chirildi!", reply_markup=None)
            await all_directions_branch(call)
        elif do == 'no':
            await show_direction_of_edu(call, direction_id)
        else:
            await delete_direction_of_edu(call, direction_id)
    elif action == 'edit':
        await add_or_set_direction_branch(call, state, direction_id=direction_id)


async def show_direction_of_edu(call, id):
    direction = await db.select_direction(id)
    info = (f"Ta'lim yo'nalishi:\n\n"
            f"uz: {direction[1]}\n"
            f"ru: {direction[2]}")
    await call.message.edit_text(info, reply_markup=await direction_inlines(direction[0]))


async def delete_direction_of_edu(call, id):
    direction = await db.select_direction(id)
    info = (f"Bu ta'lim yo'nalishi o'chirishni tasdiqlang?\n\n"
            f"uz: {direction[1]}\n"
            f"ru: {direction[2]}")
    await call.message.edit_text(info, reply_markup=await delete_direction_inlines(direction[0]))


@dp.message_handler(IsPrivate(), text="Barcha ta'lim turlari", user_id=ADMINS)
async def all_types_branch(msg: Union[types.Message, types.CallbackQuery]):
    if isinstance(msg, types.CallbackQuery):
        call = msg
        await call.message.edit_text("Barcha ta'lim turlari", reply_markup=await all_types_of_edu_inlines())
    else:
        await msg.answer(msg.text, reply_markup=await all_types_of_edu_inlines())


@dp.message_handler(IsPrivate(), text="Ta'lim turi qo'shish", user_id=ADMINS)
async def add_or_set_type_branch(msg: Union[types.Message, types.CallbackQuery], state: FSMContext,
                                 type_id: int = None):
    if isinstance(msg, types.CallbackQuery):
        call = msg
        await call.message.edit_text("❗️ Ta'lim turini o'zgartirmoqdasiz!", reply_markup=None)
        await call.message.answer("Ta'lim turi nomini o'zbek tilida kiriting:", reply_markup=ReplyKeyboardRemove())
    else:
        await msg.answer("Ta'lim turi nomini o'zbek tilida kiriting:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(TypesOfEduStates.nameUz)
    await state.set_data({'id': type_id})


@dp.message_handler(state=TypesOfEduStates.nameUz, user_id=ADMINS)
async def add_type_uz(msg: types.Message, state: FSMContext):
    await state.update_data({'nameUz': msg.text})
    await msg.answer("Ta'lim turi nomini rus tilida kiriting:", reply_markup=ReplyKeyboardRemove())
    await TypesOfEduStates.next()


@dp.message_handler(state=TypesOfEduStates.nameRu, user_id=ADMINS)
async def add_direction_ru(msg: types.Message, state: FSMContext):
    await state.update_data({'nameRu': msg.text})
    data = await state.get_data()
    await db.add_or_set_type_of_education(**data)
    if data.get('id'):
        info = "✅ Ta'lim turi muvaffaqiyatli o'zgartirildi"
    else:
        info = "✅ Ta'lim turi qo'shildi"
    await msg.answer(info, reply_markup=types_of_education_menu_markup)
    await state.finish()


@dp.callback_query_handler(IsPrivate(), types_callback_data.filter(), user_id=ADMINS)
async def show_type_of_edu(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    type_id = callback_data.get('id')
    action = callback_data.get('action')
    do = callback_data.get('do')
    if type_id == 'close':
        await call.message.delete()
    elif action == 'read':
        await show_type_of_education(call, type_id)
    elif action == 'back':
        await all_types_branch(call)
    elif action == "delete":
        if do == 'yes':
            await db.delete_type_of_education(type_id)
            await call.message.edit_text("✅ Ta'lim turi muvaffaqiyatli o'chirildi!", reply_markup=None)
            await all_types_branch(call)
        elif do == 'no':
            await show_type_of_education(call, type_id)
        else:
            await delete_type_of_edu(call, type_id)
    elif action == 'edit':
        await add_or_set_type_branch(call, state, type_id=type_id)


async def show_type_of_education(call, id):
    type_of_edu = await db.select_type_of_education(id)
    info = (f"Ta'lim turi:\n\n"
            f"uz: {type_of_edu[1]}\n"
            f"ru: {type_of_edu[2]}")
    await call.message.edit_text(info, reply_markup=await type_of_edu_inlines(type_of_edu[0]))


async def delete_type_of_edu(call, id):
    type_of_edu = await db.select_type_of_education(id)
    info = (f"Bu ta'lim turini o'chirishni tasdiqlang?\n\n"
            f"uz: {type_of_edu[1]}\n"
            f"ru: {type_of_edu[2]}")
    await call.message.edit_text(info, reply_markup=await delete_type_of_edu_inlines(type_of_edu[0]))
