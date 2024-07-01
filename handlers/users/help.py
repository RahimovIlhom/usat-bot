from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from filters import IsPrivate
from loader import dp


@dp.message_handler(IsPrivate(), CommandHelp())
async def bot_help(message: types.Message):
    text = (
        "Buyruqlar / Команды: ",
        "/start - Botni ishga tushirish / Запустить бота",
        "/help - Yordam / Помощь",
        "/set_lang - Tilni o'zgartirish / Изменить язык",
    )

    await message.answer("\n".join(text))
