import asyncio
from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ContentType, ReplyKeyboardRemove

from data.config import ADMINS
from filters import IsPrivate
from keyboards.default import directions_menu_markup
from keyboards.inline import all_directions_inlines, directions_callback_data
from keyboards.inline.directions_menu import direction_inlines, delete_direction_inlines
from loader import dp, db
from states import AddDirectionStates


@dp.message_handler(IsPrivate(), text="Barcha yo'nalishlar", user_id=ADMINS)
async def all_directions_branch(msg: Union[types.Message, types.CallbackQuery]):
    if isinstance(msg, types.CallbackQuery):
        call = msg
        await call.message.edit_text("Barcha yo'nalishlar", reply_markup=await all_directions_inlines())
    else:
        await msg.answer(msg.text, reply_markup=await all_directions_inlines())


@dp.message_handler(IsPrivate(), text="Yo'nalish qo'shish", user_id=ADMINS)
async def add_direction_branch(msg: types.Message, state: FSMContext):
    await msg.answer("Ta'lim yo'nalishi nomini o'zbek tilida kiriting:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddDirectionStates.nameUz)


@dp.message_handler(state=AddDirectionStates.nameUz, user_id=ADMINS)
async def add_direction_uz(msg: types.Message, state: FSMContext):
    await state.set_data({'nameUz': msg.text})
    await msg.answer("Ta'lim yo'nalishi nomini rus tilida kiriting:", reply_markup=ReplyKeyboardRemove())
    await AddDirectionStates.next()


@dp.message_handler(state=AddDirectionStates.nameRu, user_id=ADMINS)
async def add_direction_ru(msg: types.Message, state: FSMContext):
    await state.update_data({'nameRu': msg.text})
    data = await state.get_data()
    await db.add_or_set_direction(**data)
    await msg.answer("✅ Ta'lim yo'nalishi qo'shildi", reply_markup=directions_menu_markup)
    await state.finish()


@dp.callback_query_handler(IsPrivate(), directions_callback_data.filter(), user_id=ADMINS)
async def show_direction(call: types.CallbackQuery, callback_data: dict):
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


async def show_direction_of_edu(call, id, *args, **kwargs):
    direction = await db.select_direction(id)
    info = (f"Ta'lim yo'nalishi:\n\n"
            f"uz: {direction[1]}\n"
            f"ru: {direction[2]}")
    await call.message.edit_text(info, reply_markup=await direction_inlines(direction[0]))


async def delete_direction_of_edu(call, id, *args, **kwargs):
    direction = await db.select_direction(id)
    info = (f"Bu ta'lim yo'nalishi o'chirishni tasdiqlang?:\n\n"
            f"uz: {direction[1]}\n"
            f"ru: {direction[2]}")
    await call.message.edit_text(info, reply_markup=await delete_direction_inlines(direction[0]))
