from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


responses_callback_data = CallbackData('ques_resp', 'response')


async def make_responses_callback_data(response):
    return responses_callback_data.new(response=response)


async def all_responses_inlines(lang='uz'):
    markup = InlineKeyboardMarkup(row_width=2)
    responses_uz = ['a', 'b', 'c', 'd']
    responses_ru = ['а', 'б', 'c', 'д']
    for i in range(4):
        markup.insert(
            InlineKeyboardButton(
                text=responses_uz[i].upper() if lang == 'uz' else responses_ru[i].upper(),
                callback_data=await make_responses_callback_data(responses_uz[i])
            )
        )
    return markup
