from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def dtm_markup(lang: str = "uz") -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
    markup.insert(KeyboardButton(text="MAVJUD EMAS" if lang == "uz" else "НЕ СУЩЕСТВУЕТ"))
    return markup
