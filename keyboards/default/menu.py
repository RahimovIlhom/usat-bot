from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


manu_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Universitetga hujjat topshirish"),
        ],
        [
            KeyboardButton(text="Imtihon topshirish"),
            KeyboardButton(text="Shartnomani olish"),
        ],
        [
            KeyboardButton(text="Universitet haqida ma'lumot"),
        ],
        [
            KeyboardButton(text="Universitetdagi ta'lim yo'nalishlari"),
        ],
        [
            KeyboardButton(text="Kontrakt summalari"),
            KeyboardButton(text="Admin bilan bog'lanish"),
        ],
        [
            KeyboardButton(text="Universitet ma'muriyatiga murojaat yuborish"),
        ],
    ],
    resize_keyboard=True
)
