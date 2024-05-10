from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Botni ishga tushurish / Запустить бота"),
            types.BotCommand("help", "Yordam / Помощь"),
            types.BotCommand("set_lang", "Tilni o'zgartirish / Изменить язык"),
        ]
    )
