from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from loader import db

contracts_callback_data = CallbackData('contract', 'direction_id', 'type_id', 'contract_id', 'action', 'do')


async def make_contracts_callback_data(direction_id, type_id='0', contract_id='0', action='0', do='0'):
    return contracts_callback_data.new(direction_id=direction_id, type_id=type_id, contract_id=contract_id,
                                       action=action, do=do)


async def all_directions_for_contract_inlines(action='read'):
    all_directions = await db.select_directions()
    markup = InlineKeyboardMarkup(row_width=1)
    for direction in all_directions:
        markup.insert(
            InlineKeyboardButton(
                text=f'{direction[1]}: {"♻️ active" if direction[3] else "🚫 no active"}',
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


async def all_types_for_contract_inlines(direction_id, action='read'):
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


async def all_contract_prices_inlines(direction_id, action='read'):
    all_contracts = await db.select_contract_prices_for_direction(direction_id)
    markup = InlineKeyboardMarkup(row_width=1)
    for contract in all_contracts:
        markup.insert(InlineKeyboardButton(
            text=f"{contract[3]} - {contract[2]}",
            callback_data=await make_contracts_callback_data(direction_id, contract[1], contract[0], action=action)
        ))
    markup.insert(InlineKeyboardButton(
        text="◀️ Orqaga",
        callback_data=await make_contracts_callback_data(direction_id, type_id='back', action=action)
    ))
    return markup


async def detail_contract_inlines(direction_id, type_id, contract_id):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(InlineKeyboardButton(
        text="🗑 O'chirish",
        callback_data=await make_contracts_callback_data(direction_id, type_id, contract_id, action='delete')
    ))
    markup.insert(InlineKeyboardButton(
        text="✏️ Tahrirlash",
        callback_data=await make_contracts_callback_data(direction_id, type_id, contract_id, action='edit')
    ))
    markup.insert(InlineKeyboardButton(
        text="◀️ Orqaga",
        callback_data=await make_contracts_callback_data(direction_id, action='back')
    ))
    return markup


async def delete_contract_inlines(direction_id, type_id, contract_id):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(InlineKeyboardButton(
        text="❌ O'chirish",
        callback_data=await make_contracts_callback_data(direction_id, type_id, contract_id, 'delete', 'yes')
    ))

    markup.insert(InlineKeyboardButton(
        text="◀️ Orqaga",
        callback_data=await make_contracts_callback_data(direction_id, type_id, contract_id, 'delete', 'no')
    ))
    return markup
