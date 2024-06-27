from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from data.data_texts import DIRECTIONS_EDU


async def directions_uz_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    for direction in DIRECTIONS_EDU['uz']:
        markup.insert(KeyboardButton(text=direction))
    markup.insert(KeyboardButton(text="⬅️ Orqaga"))
    return markup


async def directions_ru_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    for direction in DIRECTIONS_EDU['ru']:
        markup.insert(KeyboardButton(text=direction))
    markup.insert(KeyboardButton(text="⬅️ Назад"))
    return markup
