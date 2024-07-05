from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def no_olympian_markup(lang):
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Mavjud emas" if lang == 'uz' else "Не имеется")
            ]
        ],
        resize_keyboard=True
    )
