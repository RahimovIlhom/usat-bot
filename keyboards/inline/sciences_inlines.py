from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from loader import db

science_callback_data = CallbackData('science', 'id', 'step', 'action', 'do')


async def make_science_callback(id, step=0, action='0', do='0'):
    return science_callback_data.new(id=id, step=step, action=action, do=do)


async def science_list_markup():
    sciences = await db.select_sciences()
    CURRENT_STEP = 0
    markup = InlineKeyboardMarkup(row_width=2)
    for sc in sciences:
        markup.insert(
            InlineKeyboardButton(
                text=sc[1],
                callback_data=await make_science_callback(sc[0], CURRENT_STEP+1)
            )
        )
    markup.row(
        InlineKeyboardButton(
            text="❌ Yopish",
            callback_data=await make_science_callback(0, CURRENT_STEP-1)
        )
    )
    return markup


async def science_show_markup(sc_id):
    CURRENT_STEP = 1
    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(
        InlineKeyboardButton(
            text="🗑 O'chirish",
            callback_data=await make_science_callback(sc_id, CURRENT_STEP+1, action='delete'),
        )
    )
    markup.insert(
        InlineKeyboardButton(
            text="✏️ Tahrirlash",
            callback_data=await make_science_callback(sc_id, CURRENT_STEP+1, action='edit'),
        )
    )
    markup.row(
        InlineKeyboardButton(
            text="◀️ Orqaga",
            callback_data=await make_science_callback(sc_id, CURRENT_STEP-1),
        )
    )
    return markup


async def request_deletion_markup(sc_id):
    CURRENT_STEP = 2
    markup = InlineKeyboardMarkup(row_width=1)
    markup.insert(
        InlineKeyboardButton(
            text="❌ O'chirish",
            callback_data=await make_science_callback(sc_id, CURRENT_STEP, action='delete', do='yes'),
        )
    )
    markup.row(
        InlineKeyboardButton(
            text="◀️ Orqaga",
            callback_data=await make_science_callback(sc_id,  CURRENT_STEP, action='delete', do='no'),
        )
    )
    return markup
