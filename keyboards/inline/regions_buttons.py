from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from data.regions import REGIONS

region_callback_data = CallbackData('region', 'name', 'id')


async def make_callback_data(name, reg_id):
    return region_callback_data.new(name=name, id=reg_id)


async def regions_buttons(lang):
    markup = InlineKeyboardMarkup(row_width=2)
    for r_dict in REGIONS:
        markup.insert(
            InlineKeyboardButton(
                text=r_dict['names'][lang],
                callback_data=await make_callback_data(r_dict['names'][lang], r_dict['region_id'])
            )
        )
    return markup
