from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import db

directions_callback_data = CallbackData('direction', 'id', 'action', 'do', 'science_id')


async def make_directions_callback_data(id, action='0', do='0', science_id=0):
    return directions_callback_data.new(id=id, action=action, do=do, science_id=science_id)


async def all_directions_inlines():
    all_directions = await db.select_directions()
    markup = InlineKeyboardMarkup(row_width=1)
    for direction in all_directions:
        markup.insert(
            InlineKeyboardButton(
                text=f'{direction[1]}: {"♻️ active" if direction[3] else "🚫 no active"}',
                callback_data=await make_directions_callback_data(direction[0], 'read')
            )
        )
    markup.insert(
        InlineKeyboardButton(
            text="❌ Yopish",
            callback_data=await make_directions_callback_data('close')
        )
    )
    return markup


async def direction_inlines(id):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(InlineKeyboardButton(
        text="🚫 Aktivsizlash",
        callback_data=await make_directions_callback_data(id, 'deactivate')
    ))
    markup.insert(InlineKeyboardButton(
        text="♻️ Aktivlashtirish",
        callback_data=await make_directions_callback_data(id, 'activate')
    ))
    markup.insert(InlineKeyboardButton(
        text="🗑 O'chirish",
        callback_data=await make_directions_callback_data(id, 'delete')
    ))
    markup.insert(InlineKeyboardButton(
        text="✏️ Tahrirlash",
        callback_data=await make_directions_callback_data(id, 'edit')
    ))
    markup.insert(InlineKeyboardButton(
        text="➖ Fan o'chirish",
        callback_data=await make_directions_callback_data(id, action='delete_sc', do='list')
    ))
    markup.insert(InlineKeyboardButton(
        text="➕ Fan qo'shish",
        callback_data=await make_directions_callback_data(id, action='add_sc', do='list')
    ))
    markup.row(InlineKeyboardButton(
        text="◀️ Orqaga",
        callback_data=await make_directions_callback_data(id, 'back')
    ))
    return markup


async def delete_direction_inlines(id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.insert(InlineKeyboardButton(
        text="❌ O'chirish",
        callback_data=await make_directions_callback_data(id, 'delete', 'yes')
    ))
    markup.insert(InlineKeyboardButton(
        text="◀️ Orqaga",
        callback_data=await make_directions_callback_data(id, 'delete', 'no')
    ))
    return markup


async def delete_sc_for_dr_inlines(dr_id):
    markup = InlineKeyboardMarkup(row_width=1)
    sciences = await db.get_sciences_for_direction(dr_id)
    for sc in sciences:
        markup.insert(
            InlineKeyboardButton(
                text=f"{sc[1]}",
                callback_data=await make_directions_callback_data(dr_id, 'delete_sc', 'yes', science_id=sc[0])
            )
        )
    markup.insert(InlineKeyboardButton(
        text="◀️ Orqaga",
        callback_data=await make_directions_callback_data(dr_id, 'read')
    ))
    return markup


async def add_sc_for_dr_inlines(dr_id):
    markup = InlineKeyboardMarkup(row_width=1)
    sciences = await db.get_sciences_not_for_direction(dr_id)
    for sc in sciences:
        markup.insert(
            InlineKeyboardButton(
                text=f"{sc[1]}",
                callback_data=await make_directions_callback_data(dr_id, 'add_sc', 'yes', science_id=sc[0])
            )
        )
    markup.insert(InlineKeyboardButton(
        text="◀️ Orqaga",
        callback_data=await make_directions_callback_data(dr_id, 'read')
    ))
    return markup
