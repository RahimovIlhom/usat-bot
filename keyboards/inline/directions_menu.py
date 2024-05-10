from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import db

directions_callback_data = CallbackData('direction', 'id', 'action', 'do')


async def make_directions_callback_data(id, action='0', do='0'):
    return directions_callback_data.new(id=id, action=action, do=do)


async def all_directions_inlines():
    all_directions = await db.select_directions()
    markup = InlineKeyboardMarkup(row_width=1)
    for direction in all_directions:
        markup.insert(
            InlineKeyboardButton(
                text=direction[1],
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
        text="🗑 O'chirish",
        callback_data=await make_directions_callback_data(id, 'delete')
    ))
    markup.insert(InlineKeyboardButton(
        text="✏️ tahrirlash",
        callback_data=await make_directions_callback_data(id, 'edit')
    ))
    markup.insert(InlineKeyboardButton(
        text="◀️ Orqaga",
        callback_data=await make_directions_callback_data(id, 'back')
    ))
    return markup


async def delete_direction_inlines(id):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(InlineKeyboardButton(
        text="❌ O'chirish",
        callback_data=await make_directions_callback_data(id, 'delete', 'yes')
    ))
    markup.insert(InlineKeyboardButton(
        text="◀️ Orqaga",
        callback_data=await make_directions_callback_data(id, 'delete', 'no')
    ))
    return markup
