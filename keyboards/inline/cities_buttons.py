from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from data.regions import CITIES

city_callback_data = CallbackData('city', 'name', 'id')


async def make_callback_data(name, city_id):
    return city_callback_data.new(name=name, id=city_id)


async def cities_buttons(reg_id, lang):
    markup = InlineKeyboardMarkup(row_width=2)
    cities_for_reg = filter(lambda city: str(city['region_id']) == str(reg_id), CITIES)
    for city_dict in cities_for_reg:
        markup.insert(
            InlineKeyboardButton(
                text=city_dict['names'][lang],
                callback_data=await make_callback_data(city_dict['names'][lang], city_dict['city_id'])
            )
        )
    markup.row(InlineKeyboardButton(
        text="◀️ Orqaga" if lang == 'uz' else "◀️ Назад",
        callback_data=await make_callback_data("back", 'back')
    ))
    return markup
