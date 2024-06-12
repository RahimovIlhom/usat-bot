from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

ready_callback_data = CallbackData('ready', 'do', 'lang')


async def make_callback_ready(do=True, lang='uz'):
    return ready_callback_data.new(do=do, lang=lang)


async def ready_inline_button(language):
    markup = InlineKeyboardMarkup(row_width=1)
    if language == 'uz':
        markup.insert(
            InlineKeyboardButton(
                text="✅ Tayyorman",
                callback_data=await make_callback_ready(lang='uz')
            ))
    else:
        markup.insert(
            InlineKeyboardButton(
                text="✅ Я готов",
                callback_data=await make_callback_ready(lang='ru')
            )
        )
    return markup
