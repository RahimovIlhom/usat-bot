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


test_callback_data = CallbackData('test', 'science', 'test', 'step', 'action', 'do')


async def make_test_callback_data(science, test=0, step=0, action='0', do='0'):
    return test_callback_data.new(science=science, test=test, step=step, action=action, do=do)


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


async def tests_for_science_markup(sc_id):
    CURRENT_STEP = 1
    markup = InlineKeyboardMarkup(row_width=1)
    tests = await db.select_tests_for_science(sc_id)
    for i in range(len(tests)):
        markup.insert(
            InlineKeyboardButton(
                text=f"{i+1}-test: {tests[i][3]}, {tests[i][6]}/{tests[i][2]}",
                callback_data=await make_test_callback_data(sc_id, tests[i][0], CURRENT_STEP+1)
            )
        )
    markup.insert(
        InlineKeyboardButton(
            text='◀️ Orqaga',
            callback_data=await make_test_callback_data(sc_id, step=CURRENT_STEP-1)
        )
    )
    return markup


async def test_markup(test_id):
    CURRENT_STEP = 2
    test = await db.select_test(test_id)
    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(
        InlineKeyboardButton(
            text="🗞 Savollar ro'yxati",
            callback_data=await make_test_callback_data(test[1], test[0], CURRENT_STEP + 1, action='list'),
        )
    )
    markup.insert(
        InlineKeyboardButton(
            text="➕ Savol qo'shish",
            callback_data=await make_test_callback_data(test[1], test[0], CURRENT_STEP + 1, action='add'),
        )
    )
    markup.insert(
        InlineKeyboardButton(
            text="🗑 O'chirish",
            callback_data=await make_test_callback_data(test[1], test[0], CURRENT_STEP + 1, action='delete'),
        )
    )
    markup.insert(
        InlineKeyboardButton(
            text="✏️ Tahrirlash",
            callback_data=await make_test_callback_data(test[1], test[0], CURRENT_STEP + 1, action='edit'),
        )
    )
    markup.row(
        InlineKeyboardButton(
            text="◀️ Orqaga",
            callback_data=await make_test_callback_data(test[1], test[0], CURRENT_STEP - 1),
        )
    )
    return markup


async def question_delete_test_markup(test_id):
    CURRENT_STEP = 3
    test = await db.select_test(test_id)
    markup = InlineKeyboardMarkup(row_width=1)
    markup.insert(
        InlineKeyboardButton(
            text="❌ O'chirish",
            callback_data=await make_test_callback_data(test[1], test[0], CURRENT_STEP + 1, action='delete', do='yes'),
        )
    )
    markup.insert(
        InlineKeyboardButton(
            text="◀️ Orqaga",
            callback_data=await make_test_callback_data(test[1], test[0], CURRENT_STEP - 1),
        )
    )
    return markup
