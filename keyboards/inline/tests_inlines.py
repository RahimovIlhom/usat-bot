from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import db


async def all_faculty_inlines_for_test():
    all_directions = await db.select_directions()
    markup = InlineKeyboardMarkup(row_width=1)
    for direction in all_directions:
        markup.insert(
            InlineKeyboardButton(
                text=direction[1],
                callback_data=direction[0]
            )
        )
    markup.insert(
        InlineKeyboardButton(
            text="❌ Yopish",
            callback_data='close'
        )
    )
    return markup


async def all_science_inlines_for_test():
    sciences = await db.select_sciences()
    markup = InlineKeyboardMarkup(row_width=2)
    for sc in sciences:
        markup.insert(
            InlineKeyboardButton(
                text=sc[1],
                callback_data=sc[0]
            )
        )
    markup.row(
        InlineKeyboardButton(
            text="◀️ Orqaga",
            callback_data='back'
        )
    )
    return markup


lang_inlines_for_test = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="O'zbek tili", callback_data='uz'),
            InlineKeyboardButton(text="Русский язык", callback_data='ru')
        ]
    ]
)
