from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class AdminFilter(BoundFilter):
    async def check(self, message: types.Update) -> bool:
        if isinstance(message, types.CallbackQuery):
            message = message.message
        member = await message.chat.get_member(message.from_user.id)
        return member.is_chat_admin()
