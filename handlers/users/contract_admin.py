from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from data.config import ADMINS
from filters import IsPrivate
from keyboards.default import directions_menu_markup, types_of_education_menu_markup, contract_menu_markup
from keyboards.inline import all_directions_inlines, directions_callback_data, all_types_of_edu_inlines, \
    types_callback_data, type_of_edu_inlines, delete_type_of_edu_inlines, direction_inlines, delete_direction_inlines, \
    contracts_callback_data, all_types_for_contract_inlines, all_contract_prices_inlines, detail_contract_inlines, \
    delete_contract_inlines
from keyboards.inline import all_directions_for_contract_inlines
from loader import dp, db
from states import AddDirectionStates, TypesOfEduStates, AddContractSumma


@dp.message_handler(IsPrivate(), text="Barcha yo'nalishlar", user_id=ADMINS)
async def all_directions_branch(msg: Union[types.Message, types.CallbackQuery], delete: bool = False):
    if isinstance(msg, types.CallbackQuery):
        call = msg
        if delete:
            await call.message.answer("Barcha yo'nalishlar", reply_markup=await all_directions_inlines())
        else:
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
            await all_directions_branch(call, True)
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
async def all_types_branch(msg: Union[types.Message, types.CallbackQuery], delete: bool = False):
    if isinstance(msg, types.CallbackQuery):
        call = msg
        if delete:
            await call.message.answer("Barcha ta'lim turlari", reply_markup=await all_types_of_edu_inlines())
        else:
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
            await all_types_branch(call, True)
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


@dp.message_handler(IsPrivate(), text="Yo'nalishlar bo'yicha kontrakt summalari", user_id=ADMINS)
async def contract_for_directions(msg: Union[types.Message, types.CallbackQuery]):
    if isinstance(msg, types.CallbackQuery):
        call = msg
        await call.message.edit_text("Qaysi yo'nalish bo'yicha kontrakt summasini ko'rmoqchisiz?",
                                     reply_markup=await all_directions_for_contract_inlines())
    else:
        await msg.answer("Qaysi yo'nalish bo'yicha kontrakt summasini ko'rmoqchisiz?",
                         reply_markup=await all_directions_for_contract_inlines())


@dp.message_handler(IsPrivate(), text="Kontrakt summasini kiritish", user_id=ADMINS)
async def add_contract_for_direction(msg: Union[types.Message, types.CallbackQuery]):
    if isinstance(msg, types.CallbackQuery):
        call = msg
        await call.message.edit_text("Qaysi yo'nalish bo'yicha kontrakt summa qo'shmoqchisiz?",
                                     reply_markup=await all_directions_for_contract_inlines(action='add'))
    else:
        await msg.answer("Qaysi yo'nalish bo'yicha kontrakt summa qo'shmoqchisiz?",
                         reply_markup=await all_directions_for_contract_inlines(action='add'))


@dp.callback_query_handler(IsPrivate(), contracts_callback_data.filter(), user_id=ADMINS)
async def select_func(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    direction_id = callback_data.get('direction_id')
    type_id = callback_data.get('type_id')
    contract_id = callback_data.get('contract_id')
    action = callback_data.get('action')
    do = callback_data.get('do')
    if direction_id == 'close':
        await call.message.delete()
    elif action == 'add':
        if type_id == 'back':
            await add_contract_for_direction(call)
        elif type_id == '0':
            await add_contract_for_type(call, direction_id)
        else:
            await add_contract_summa(call, direction_id, type_id, state)
    elif action == 'read':
        if type_id == 'back':
            await contract_for_directions(call)
        elif type_id == '0':
            await show_contract_prices(call, direction_id)
        elif contract_id != '0':
            await show_one_contract_price(call, direction_id, type_id, contract_id)
    elif action == 'back':
        await show_contract_prices(call, direction_id)
    elif action == 'delete':
        if do == 'yes':
            await db.delete_contract_price(direction_id, type_id)
            await call.message.edit_text("✅ Kontrakt miqdori muvaffaqiyatli o'chirildi!")
            await show_contract_prices(call, direction_id, True)
        elif do == 'no':
            await show_one_contract_price(call, direction_id, type_id, contract_id)
        else:
            await delete_contract_price(call, direction_id, type_id, contract_id)
    elif action == 'edit':
        await edit_contract_price(call, direction_id, type_id, contract_id, state)


async def add_contract_for_type(call, direction_id):
    direction = await db.select_direction(direction_id)
    await call.message.edit_text(f"{direction[1]} ta'lim yo'nalishining qaysi ta'lim turiga qo'shmoqchisiz?",
                                 reply_markup=await all_types_for_contract_inlines(direction_id, 'add'))


async def add_contract_summa(call, direction_id, type_id, state):
    direction = await db.select_direction(direction_id)
    type_of_edu = await db.select_type_of_education(type_id)
    info = (f"Ta'lim yo'nalishi:\n"
            f"{direction[1]}\n\n"
            f"Ta'lim turi:\n"
            f"{type_of_edu[1]}")
    await call.message.edit_text(info, reply_markup=None)
    await call.message.answer("Kontrakt summa miqdorini kiriting: ", reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddContractSumma.summa)
    await state.set_data({
        'direction_id': direction_id,
        'type_id': type_id
    })


@dp.message_handler(state=AddContractSumma.summa, user_id=ADMINS)
async def contract_summa(msg: types.Message, state: FSMContext, set_summa: bool = False):
    data = await state.get_data()
    summa = msg.text
    if summa.isdigit():
        resp = await db.add_or_set_contract_price(int(summa), **data)
        if resp == 'set':
            answer_text = "✅ Kontrakt summasi muvaffaqiyatli o'zgartirildi"
        else:
            answer_text = "✅ Kontrakt summasi muvaffaqiyatli qo'shildi"
        await msg.answer(answer_text, reply_markup=contract_menu_markup)
        await state.reset_data()
        await state.finish()
    else:
        await msg.answer("Kontrakt miqdori xato, qayta kiriting:")


async def show_contract_prices(call, direction_id, deleted=False):
    direction = await db.select_direction(direction_id)
    if deleted:
        await call.message.answer(f"<b>{direction[1]}</b> ta'lim yo'nalishi bo'yicha kontrakt narxlari:",
                                  reply_markup=await all_contract_prices_inlines(direction_id))
    else:
        await call.message.edit_text(f"<b>{direction[1]}</b> ta'lim yo'nalishi bo'yicha kontrakt narxlari:",
                                     reply_markup=await all_contract_prices_inlines(direction_id))


async def show_one_contract_price(call: Union[types.Message, types.CallbackQuery], direction_id, type_id, contract_id):
    contract = await db.select_contact_price(direction_id, type_id)
    type_of_edu = await db.select_type_of_education(type_id)
    direction = await db.select_direction(direction_id)
    info_text = (f"Ta'lim yo'nalishi:\n"
                 f"uz: {direction[1]}\n"
                 f"ru: {direction[2]}\n\n"
                 f"Ta'lim turi:\n"
                 f"uz: {type_of_edu[1]}\n"
                 f"ru: {type_of_edu[2]}\n\n"
                 f"Kontrakt miqdori: {contract[1]}")
    if isinstance(call, types.Message):
        await call.answer(info_text, reply_markup=await detail_contract_inlines(direction_id, type_id, contract_id))
    else:
        await call.message.edit_text(info_text,
                                     reply_markup=await detail_contract_inlines(direction_id, type_id, contract_id))


async def delete_contract_price(call, direction_id, type_id, contract_id):
    contract = await db.select_contact_price(direction_id, type_id)
    type_of_edu = await db.select_type_of_education(type_id)
    direction = await db.select_direction(direction_id)
    question_text = (f"Rostdan ham quyidagi kontrakt miqdorini o'chirmoqchimisiz?\n\n"
                     f"Ta'lim yo'nalishi:\n"
                     f"uz: {direction[1]}\n\n"
                     f"Ta'lim turi:\n"
                     f"uz: {type_of_edu[1]}\n\n"
                     f"Kontrakt miqdori: {contract[1]}")
    await call.message.edit_text(question_text,
                                 reply_markup=await delete_contract_inlines(direction_id, type_id, contract_id))


async def edit_contract_price(call, direction_id, type_id, contract_id, state):
    direction = await db.select_direction(direction_id)
    type_of_edu = await db.select_type_of_education(type_id)
    info = (f"Ta'lim yo'nalishi:\n"
            f"{direction[1]}\n\n"
            f"Ta'lim turi:\n"
            f"{type_of_edu[1]}")
    await call.message.edit_text(info, reply_markup=None)
    await call.message.answer("O'zgartirish uchun kontrakt summa miqdorini kiriting: ",
                              reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddContractSumma.summa)
    await state.set_data({
        'direction_id': direction_id,
        'type_id': type_id
    })
