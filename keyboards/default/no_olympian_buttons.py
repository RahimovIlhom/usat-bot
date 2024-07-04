from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def no_olympian_markup():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Mavjud emas")
            ]
        ],
        resize_keyboard=True
    )
