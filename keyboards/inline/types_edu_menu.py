from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import db

types_callback_data = CallbackData('type_of_edu', 'id', 'action', 'do')


async def make_types_callback_data(id, action='0', do='0'):
    return types_callback_data.new(id=id, action=action, do=do)


async def all_types_of_edu_inlines():
    all_types = await db.select_types_of_education()
    markup = InlineKeyboardMarkup(row_width=1)
    for type_of_edu in all_types:
        markup.insert(
            InlineKeyboardButton(
                text=f"{type_of_edu[1]}: {'♻️ active' if type_of_edu[3] else '🚫 no active'}",
                callback_data=await make_types_callback_data(type_of_edu[0], 'read')
            )
        )
    markup.insert(
        InlineKeyboardButton(
            text="❌ Yopish",
            callback_data=await make_types_callback_data('close')
        )
    )
    return markup


async def type_of_edu_inlines(id):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(InlineKeyboardButton(
        text="🚫 Aktivsizlash",
        callback_data=await make_types_callback_data(id, 'deactivate')
    ))
    markup.insert(InlineKeyboardButton(
        text="♻️ Aktivlashtirish",
        callback_data=await make_types_callback_data(id, 'activate')
    ))
    markup.insert(InlineKeyboardButton(
        text="🗑 O'chirish",
        callback_data=await make_types_callback_data(id, 'delete')
    ))
    markup.insert(InlineKeyboardButton(
        text="✏️ Tahrirlash",
        callback_data=await make_types_callback_data(id, 'edit')
    ))
    markup.insert(InlineKeyboardButton(
        text="◀️ Orqaga",
        callback_data=await make_types_callback_data(id, 'back')
    ))
    return markup


async def delete_type_of_edu_inlines(id):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(InlineKeyboardButton(
        text="❌ O'chirish",
        callback_data=await make_types_callback_data(id, 'delete', 'yes')
    ))
    markup.insert(InlineKeyboardButton(
        text="◀️ Orqaga",
        callback_data=await make_types_callback_data(id, 'delete', 'no')
    ))
    return markup
