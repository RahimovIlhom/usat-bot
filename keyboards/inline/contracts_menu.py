from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import db

contracts_callback_data = CallbackData('contract', 'direction_id', 'type_id', 'contract_id', 'action')


async def make_contracts_callback_data(direction_id, type_id='0', contract_id='0', action='0'):
    return contracts_callback_data.new(direction_id=direction_id, type_id=type_id, contract_id=contract_id,
                                       action=action)


async def all_directions_for_contract_inlines(action='0'):
    all_directions = await db.select_directions()
    markup = InlineKeyboardMarkup(row_width=1)
    for direction in all_directions:
        markup.insert(
            InlineKeyboardButton(
                text=direction[1],
                callback_data=await make_contracts_callback_data(direction[0], action=action)
            )
        )
    markup.insert(
        InlineKeyboardButton(
            text="❌ Yopish",
            callback_data=await make_contracts_callback_data('close')
        )
    )
    return markup


async def all_types_for_contract_inlines(direction_id, action='0'):
    all_types = await db.select_types_of_education()
    markup = InlineKeyboardMarkup(row_width=1)
    for type_of_edu in all_types:
        markup.insert(
            InlineKeyboardButton(
                text=type_of_edu[1],
                callback_data=await make_contracts_callback_data(direction_id, type_of_edu[0], action=action)
            )
        )
    markup.insert(
        InlineKeyboardButton(
            text="◀️ Orqaga",
            callback_data=await make_contracts_callback_data(direction_id, type_id='back', action=action)
        )
    )
    return markup
