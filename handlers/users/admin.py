from aiogram import types
from aiogram.types import CallbackQuery

from data.config import ADMINS
from filters import IsPrivate
from keyboards.default import applications_menu_markup, \
    exams_menu_markup, directions_menu_markup, types_of_education_menu_markup, contract_menu_markup, \
    sciences_menu_markup
from keyboards.inline import accept_app_callback_data
from loader import dp, db


@dp.message_handler(IsPrivate(), text="📑 Arizalar bo'limi", user_id=ADMINS)
async def applications_branch(msg: types.Message):
    await msg.answer(msg.text, reply_markup=applications_menu_markup)


@dp.message_handler(IsPrivate(), text="👨‍💻 Imtihon bo'limi", user_id=ADMINS)
async def exams_branch(msg: types.Message):
    await msg.answer(msg.text, reply_markup=exams_menu_markup)


@dp.message_handler(IsPrivate(), text="📚 Fanlar bo'limi", user_id=ADMINS)
async def exams_branch(msg: types.Message):
    await msg.answer(msg.text, reply_markup=sciences_menu_markup)


@dp.message_handler(IsPrivate(), text="👨‍🎓 Yo'nalishlar bo'limi", user_id=ADMINS)
async def directions_branch(msg: types.Message):
    await msg.answer(msg.text, reply_markup=directions_menu_markup)


@dp.message_handler(IsPrivate(), text="🎓 Ta'lim turlari bo'limi", user_id=ADMINS)
async def types_of_edu_branch(msg: types.Message):
    await msg.answer(msg.text, reply_markup=types_of_education_menu_markup)


@dp.message_handler(IsPrivate(), text="🏷️ Kontrakt summalari", user_id=ADMINS)
async def contract_branch(msg: types.Message):
    await msg.answer(msg.text, reply_markup=contract_menu_markup)


@dp.callback_query_handler(accept_app_callback_data.filter(), user_id=ADMINS)
async def accept_applicant_func(call: CallbackQuery, callback_data: dict):
    applicant_id = callback_data.get('applicant_id')
    status = callback_data.get('status')
    applicant = await db.get_applicant(applicant_id)
    statusApplicant = applicant[14]
    if statusApplicant == 'SUBMITTED':
        await db.update_application_status(applicant_id, status)
        if status == 'ACCEPTED':
            await call.message.edit_caption(caption="✅ Bu ariza qabul qilingan", reply_markup=None)
        elif status == 'REJECTED':
            await call.message.edit_caption(caption="❌ Bu ariza rad qilingan", reply_markup=None)
    else:
        if statusApplicant == 'REJECTED':
            await call.message.edit_caption("Bu arizachi boshqa admin tomonidan rad qilingan",
                                            reply_markup=None)
        else:
            await call.message.edit_caption("Bu arizachi boshqa admin tomonidan qabul qilingan",
                                            reply_markup=None)
