from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


language_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="O'zbek tili"),
            KeyboardButton(text="Русский язык"),
        ],
    ],
    resize_keyboard=True
)
