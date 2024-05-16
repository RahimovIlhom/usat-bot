from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import db

application_callback_data = CallbackData('application', 'direction_id', 'type_id', 'edu_language', 'level')


async def make_application_callback_data(direction_id, type_id='0', edu_language='0', level=0):
    return application_callback_data.new(direction_id=direction_id, type_id=type_id, edu_language=edu_language,
                                         level=level)


async def all_faculties_inlines(lang='uz'):
    CURRENT_LEVEL = 0
    all_directions = await db.select_directions()
    markup = InlineKeyboardMarkup(row_width=1)
    for direction in all_directions:
        markup.insert(
            InlineKeyboardButton(
                text=direction[1] if lang == 'uz' else direction[2],
                callback_data=await make_application_callback_data(direction[0], level=CURRENT_LEVEL + 1)
            )
        )
    return markup


async def types_and_contracts(direction_id, lang='uz'):
    CURRENT_LEVEL = 1
    all_contracts = await db.select_contract_prices_for_direction(direction_id)
    markup = InlineKeyboardMarkup(row_width=1)
    for type_and_contract in all_contracts:
        price = f"{type_and_contract[2]:,.2f}".replace(",", " ")
        markup.insert(
            InlineKeyboardButton(
                text=f"{type_and_contract[3]} - kontrakt: {price}" if lang == 'uz' else f"{type_and_contract[4]} - контракт: {price}",
                callback_data=await make_application_callback_data(direction_id, type_and_contract[1], level=CURRENT_LEVEL+1),
            )
        )

    markup.insert(InlineKeyboardButton(
        text="◀️ Orqaga" if lang == 'uz' else "◀️ Назад",
        callback_data=await make_application_callback_data(direction_id, level=CURRENT_LEVEL - 1)
    ))
    return markup


async def choices_e_edu_language(direction_id, type_id, lang='uz'):
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup(row_width=1)
    markup.insert(
        InlineKeyboardButton(
            text="O'zbek tili" if lang == 'uz' else "Узбекский язык",
            callback_data=await make_application_callback_data(direction_id, type_id, 'uz', level=CURRENT_LEVEL+1)
        )
    )
    markup.insert(
        InlineKeyboardButton(
            text="Rus tili" if lang == 'uz' else "Русский язык",
            callback_data=await make_application_callback_data(direction_id, type_id, 'ru', level=CURRENT_LEVEL+1)
        )
    )

    markup.insert(InlineKeyboardButton(
        text="◀️ Orqaga" if lang == 'uz' else "◀️ Назад",
        callback_data=await make_application_callback_data(direction_id, level=CURRENT_LEVEL - 1)
    ))
    return markup
