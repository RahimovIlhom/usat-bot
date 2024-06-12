from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

accept_app_callback_data = CallbackData('accept_applicant', 'applicant_id', 'status')


async def make_applicant_callback_data(applicant_id, status):
    return accept_app_callback_data.new(applicant_id=applicant_id, status=status)


async def accept_applicant_inline(applicant_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.insert(
        InlineKeyboardButton(
            text="✅ Arizani qabul qilish",
            callback_data=await make_applicant_callback_data(applicant_id, 'ACCEPTED'),
        )
    )
    markup.insert(
        InlineKeyboardButton(
            text="❌ Arizani rad qilish",
            callback_data=await make_applicant_callback_data(applicant_id, 'REJECTED'),
        )
    )
    return markup
