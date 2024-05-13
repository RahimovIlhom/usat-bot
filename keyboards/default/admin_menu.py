from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


admin_menu_markup_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Arizalar bo'limi"),
            KeyboardButton(text="Imtihon bo'limi"),
        ],
        [
            KeyboardButton(text="Yo'nalishlar bo'limi"),
            KeyboardButton(text="Ta'lim turlari bo'limi"),
        ],
        [
            KeyboardButton(text="Kontrakt summalari"),
        ],
    ],
    resize_keyboard=True
)


applications_menu_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Ariza yuborganlar"),
            KeyboardButton(text="Arizasi tasdiqlanganlar"),
        ],
        [
            KeyboardButton(text="◀️ Orqaga"),
        ],
    ],
    resize_keyboard=True
)

exams_menu_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Testlar")
        ],
        [
            KeyboardButton(text="◀️ Orqaga"),
        ],
    ],
    resize_keyboard=True
)

directions_menu_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Barcha yo'nalishlar"),
            KeyboardButton(text="Yo'nalish qo'shish"),
        ],
        [
            KeyboardButton(text="◀️ Orqaga"),
        ],
    ],
    resize_keyboard=True
)

types_of_education_menu_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Barcha ta'lim turlari"),
            KeyboardButton(text="Ta'lim turi qo'shish"),
        ],
        [
            KeyboardButton(text="◀️ Orqaga"),
        ],
    ],
    resize_keyboard=True
)

contract_menu_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Yo'nalishlar bo'yicha kontrakt summalari"),
        ],
        [
            KeyboardButton(text="Kontrakt summasini kiritish"),
        ],
        [
            KeyboardButton(text="◀️ Orqaga"),
        ],
    ],
    resize_keyboard=True
)
