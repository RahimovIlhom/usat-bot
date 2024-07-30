from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def no_olympian_markup(lang):
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="MAVJUD EMAS" if lang == 'uz' else "НЕ ИМЕЕТСЯ")
            ]
        ],
        resize_keyboard=True
    )
