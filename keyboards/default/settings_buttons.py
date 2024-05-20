from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


settings_markup_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🌐 Tilni o'zgartirish")
        ],
        [
            KeyboardButton(text="◀️ Orqaga"),
        ],
    ],
    resize_keyboard=True
)


settings_markup_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🌐 Изменение языка")
        ],
        [
            KeyboardButton(text="◀️ Orqaga"),
        ],
    ],
    resize_keyboard=True
)
