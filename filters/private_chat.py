from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class IsPrivate(BoundFilter):
    async def check(self, message: types.Update) -> bool:
        if isinstance(message, types.CallbackQuery):
            message = message.message
        return message.chat.type == types.ChatType.PRIVATE
