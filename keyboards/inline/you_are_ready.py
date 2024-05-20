from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def ready_inline_button(language):
    markup = InlineKeyboardMarkup(row_width=1)
    if language == 'uz':
        markup.insert(
            InlineKeyboardButton(
                text="✅ Tayyorman",
                callback_data='ready'
            ))
    else:
        markup.insert(
            InlineKeyboardButton(
                text="✅ Я готов",
                callback_data='ready'
            )
        )
    return markup
