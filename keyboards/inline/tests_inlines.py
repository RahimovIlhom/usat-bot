from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import db


async def all_science_inlines_for_test():
    sciences = await db.select_sciences()
    markup = InlineKeyboardMarkup(row_width=2)
    for sc in sciences:
        markup.insert(
            InlineKeyboardButton(
                text=sc[1],
                callback_data=sc[0]
            )
        )
    markup.row(
        InlineKeyboardButton(
            text="❌ Yopish",
            callback_data='close'
        )
    )
    return markup


lang_inlines_for_test = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="O'zbek tili", callback_data='uz'),
            InlineKeyboardButton(text="Русский язык", callback_data='ru')
        ]
    ]
)


test_callback_data = CallbackData('test', 'science', 'test', 'step', 'action')


async def make_test_callback_data(science, test=0, step=0, action='0'):
    return test_callback_data.new(science=science, test=test, step=step, action=action)


async def all_sciences_markup():
    CURRENT_STEP = 0
    sciences = await db.select_sciences()
    markup = InlineKeyboardMarkup(row_width=2)
    for sc in sciences:
        markup.insert(
            InlineKeyboardButton(
                text=sc[1],
                callback_data=await make_test_callback_data(sc[0], step=CURRENT_STEP+1),
            )
        )
    markup.row(
        InlineKeyboardButton(
            text="❌ Yopish",
            callback_data=await make_test_callback_data(0, step=CURRENT_STEP-1)
        )
    )
    return markup
