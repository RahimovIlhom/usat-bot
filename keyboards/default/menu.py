from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu_markup_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📰 Universitetga hujjat topshirish"),
        ],
        [
            KeyboardButton(text="🧑‍💻 Imtihon topshirish"),
        ],
        [
            KeyboardButton(text="⚙️ Sozlamalar"),
            KeyboardButton(text="👤 Profilim"),
        ],
        [
            KeyboardButton(text="📥 Shartnomani olish"),
            KeyboardButton(text="ℹ️ Ma'lumotlar"),
        ],
        [
            KeyboardButton(text="🔗 Admin bilan bog'lanish"),
        ],
        [
            KeyboardButton(text="✉️ Universitet ma'muriyatiga murojaat yuborish"),
        ],
    ],
    resize_keyboard=True
)

sub_menu_markup_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🏢 Universitet haqida ma'lumot"),
        ],
        [
            KeyboardButton(text="👨‍🎓 Universitetdagi ta'lim yo'nalishlari"),
        ],
        [
            KeyboardButton(text="🏷️ Kontrakt summalari"),
        ],
        [
            KeyboardButton(text="◀️ Orqaga"),
        ],
    ],
    resize_keyboard=True
)

profile_menu_markup_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="ℹ️ Ma'lumotlarim"),
            KeyboardButton(text="📄 Arizalarim")
        ],
        [
            KeyboardButton(text="📊 Imtihon natijam"),
        ],
        [
            KeyboardButton(text="◀️ Orqaga"),
        ],
    ],
    resize_keyboard=True
)


menu_markup_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📰 Подать документы в университет"),
        ],
        [
            KeyboardButton(text="🧑‍💻 Сдать экзамен"),
        ],
        [
            KeyboardButton(text="⚙️ Настройки"),
            KeyboardButton(text="👤 Мой профиль"),
        ],
        [
            KeyboardButton(text="📥 Получить контракт"),
            KeyboardButton(text="ℹ️ Информация"),
        ],
        [
            KeyboardButton(text="🔗  Связаться с администратором"),
        ],
        [

            KeyboardButton(text="✉️ Отправить обращение в ректорат университета"),
        ],
    ],
    resize_keyboard=True
)


sub_menu_markup_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🏢 Информация об университете"),
        ],
        [
            KeyboardButton(text="👨‍🎓 Направления обучения в университете"),
        ],
        [
            KeyboardButton(text="🏷️ Суммы контрактов"),
        ],
        [
            KeyboardButton(text="◀️ Назад"),
        ]
    ],
    resize_keyboard=True
)

profile_menu_markup_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="ℹ️ Мои данные"),
            KeyboardButton(text="📄 Мои заявки")
        ],
        [
            KeyboardButton(text="📊 Мои результаты экзамена"),
        ],
        [
            KeyboardButton(text="◀️ Назад"),
        ],
    ],
    resize_keyboard=True
)
