from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu_markup_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Universitetga hujjat topshirish"),
        ],
        [
            KeyboardButton(text="Imtihon topshirish"),
        ],
        [
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
        ],
        [
            KeyboardButton(text="Admin bilan bog'lanish"),
        ],
        [
            KeyboardButton(text="Universitet ma'muriyatiga murojaat yuborish"),
        ],
    ],
    resize_keyboard=True
)


menu_markup_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Подать документы в университет"),
        ],
        [
            KeyboardButton(text="Сдать экзамен"),
        ],
        [
            KeyboardButton(text="Получить контракт"),
        ],
        [
            KeyboardButton(text="Информация об университете"),
        ],
        [
            KeyboardButton(text="Образовательные направления в университете"),
        ],
        [
            KeyboardButton(text="Суммы контрактов"),
        ],
        [
            KeyboardButton(text="Связаться с администратором"),
        ],
        [
            KeyboardButton(text="Отправить обращение в ректорат университета"),
        ],
    ],
    resize_keyboard=True
)
