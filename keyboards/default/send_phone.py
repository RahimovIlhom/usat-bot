from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


phone_markup_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="☎️ Kontaktni yuborish", request_contact=True),
        ],
    ],
    resize_keyboard=True
)

phone_markup_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="☎️ Отправить контакт", request_contact=True),
        ],
    ],
    resize_keyboard=True
)
