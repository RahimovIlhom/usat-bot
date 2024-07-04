from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import WrongFileIdentifier, BadRequest

from data.data_texts import INFORMATION_TEXTS, DIRECTIONS_EDU_INFO_UZ, DIRECTIONS_EDU_INFO_RU, CONTRACT_INFO_UZ, \
    CONTRACT_INFO_RU
from filters import IsPrivate
from keyboards.default import sub_menu_markup_uz, sub_menu_markup_ru, directions_uz_markup, directions_ru_markup
from loader import dp, db


@dp.message_handler(IsPrivate(), text="ℹ️ Ma'lumotlar")
async def other_information(msg: types.Message):
    await msg.answer(msg.text, reply_markup=sub_menu_markup_uz)


@dp.message_handler(IsPrivate(), text="ℹ️ Информация")
async def other_information(msg: types.Message):
    await msg.answer(msg.text, reply_markup=sub_menu_markup_ru)


@dp.message_handler(IsPrivate(), text=["🏢 Universitet haqida ma'lumot", "🏢 Информация об университете"])
async def other_information(msg: types.Message):
    lang = 'uz' if msg.text == "🏢 Universitet haqida ma'lumot" else 'ru'
    image_url = 'https://telegra.ph//file/cef381153d9f64cb45b12.jpg'
    try:
        await msg.answer_photo(photo=image_url, caption=INFORMATION_TEXTS[lang], parse_mode=types.ParseMode.MARKDOWN)
    except (WrongFileIdentifier, BadRequest, ValueError, Exception):
        await msg.answer(INFORMATION_TEXTS[lang], parse_mode=types.ParseMode.MARKDOWN)


@dp.message_handler(IsPrivate(),
                    text=["👨‍🎓 Universitetdagi ta'lim yo'nalishlari", "👨‍🎓 Направления обучения в университете"])
async def direction_of_education_information(msg: types.Message):
    lang = 'uz' if msg.text == "👨‍🎓 Universitetdagi ta'lim yo'nalishlari" else 'ru'

    response_text = {
        'uz': "👨‍🎓 Universitetdagi ta'lim yo'nalishlari.\nBatafsil ma'lumot olish uchun ta'lim yo'nalishini tanlang.",
        'ru': "👨‍🎓 Направления обучения в университете\nДля получения дополнительной информации выберите "
              "направление обучения."
    }
    markup = await directions_uz_markup() if lang == 'uz' else await directions_ru_markup()

    await msg.answer(response_text[lang], reply_markup=markup)


@dp.message_handler(IsPrivate(), text=DIRECTIONS_EDU_INFO_UZ.keys())
async def direction_info_uz(msg: types.Message):
    direction = msg.text
    info = DIRECTIONS_EDU_INFO_UZ[direction]

    response = (
        f"📝 Yo'nalish: {direction}\n\n"
        f"ℹ️ Yo’nalish haqida ma’lumot:\n{info['Yo’nalish haqida ma’lumot']}\n\n"
        f"🎓 2024/2025-yil uchun qabul kvotasi:\n{info['2024/2025-yil uchun qabul kvotasi']}\n\n"
        f"📋 Ushbu yo'nalish bo'yicha imtihonda tushadigan fanlar kesimidagi savollar soni va baholash mezoni:"
        f"\n{info['Qabul qilinish talablari']}"
    )
    try:
        await msg.answer_photo(photo=info['image'])
    except BadRequest:
        pass

    await msg.answer(response)


@dp.message_handler(IsPrivate(), text=DIRECTIONS_EDU_INFO_RU.keys())
async def direction_info_ru(msg: types.Message):
    direction = msg.text
    info = DIRECTIONS_EDU_INFO_RU[direction]

    response = (
        f"📝 Направление: {direction}\n\n"
        f"ℹ️ Информация о направлении:\n{info['Информация о направлении']}\n\n"
        f"🎓 Квота на 2024/2025 год:\n{info['Квота на 2024/2025 год']}\n\n"
        f"📋 Требования к поступлению:\n{info['Требования к поступлению']}"
    )
    try:
        await msg.answer_photo(photo=info['image'])
    except BadRequest:
        pass

    await msg.answer(response)


@dp.message_handler(IsPrivate(), text=["🏷️ Kontrakt summalari", "🏷️ Суммы контрактов"])
async def contract_information(msg: types.Message):
    lang = 'uz' if msg.text == "🏷️ Kontrakt summalari" else 'ru'

    if lang == 'uz':
        contract_info = CONTRACT_INFO_UZ
        response = "📋 Barcha yo'nalishlar bo'yicha o'qish davomiyligi va kontrakt summalari:\n\n"
    else:
        contract_info = CONTRACT_INFO_RU
        response = "📋 Продолжительность обучения и суммы контрактов по всем направлениям:\n\n"

    for direction, info in contract_info.items():
        response += f"🔹 {direction}\n"
        for form, price in info.items():
            response += f"   {form}: {price}\n"
        response += "\n"

    await msg.answer(response)


# # Function to fetch and show directions with inline buttons
# async def show_directions(msg: types.Message, lang: str):
#     directions = await db.select_directions()
#     if not directions:
#         no_contracts_text = {
#             'uz': "Hozirda hech qanday kontrakt summasi mavjud emas.",
#             'ru': "На данный момент нет сумм контрактов."
#         }
#         await msg.answer(no_contracts_text[lang])
#         return
#
#     # Create inline keyboard with directions
#     keyboard = InlineKeyboardMarkup()
#     for direction in directions:
#         direction_id, name_uz, name_ru, active = direction
#         if active:
#             keyboard.add(InlineKeyboardButton(
#                 text=f"🔹 {name_uz}" if lang == 'uz' else f"🔹 {name_ru}",
#                 callback_data=f"direction_{direction_id}_{lang}"
#             ))
#
#     # Add Close button
#     keyboard.add(InlineKeyboardButton(
#         text="✖️ Yopish" if lang == 'uz' else "✖️ Закрыть",
#         callback_data=f"close_{lang}"
#     ))
#     try:
#         await msg.edit_text(
#             text="👨‍🎓 Qaysi ta'lim yo'nalishi bo'yicha kontrakt summasini ko'rmoqchisiz?"
#             if lang == 'uz' else "👨‍🎓 По какому направлению вы хотите узнать суммы контрактов?",
#             reply_markup=keyboard
#         )
#     except BadRequest:
#         await msg.answer(
#             text="👨‍🎓 Qaysi ta'lim yo'nalishi bo'yicha kontrakt summasini ko'rmoqchisiz?"
#             if lang == 'uz' else "👨‍🎓 По какому направлению вы хотите узнать суммы контрактов?",
#             reply_markup=keyboard
#         )
#
#
# # Function to display contract prices for a selected direction
# async def show_contract_prices(callback_query: types.CallbackQuery, lang: str, direction_id: int):
#     contracts = await db.select_contract_prices_for_direction(direction_id)
#     if not contracts:
#         no_contracts_text = {
#             'uz': "Hozirda hech qanday kontrakt summasi mavjud emas.",
#             'ru': "На данный момент нет сумм контрактов."
#         }
#         await callback_query.message.edit_text(no_contracts_text[lang])
#         return
#
#     # Create response text with contract prices
#     response_text = {
#         'uz': "🏷️ Kontrakt summalari:\n\n",
#         'ru': "🏷️ Суммы контрактов:\n\n"
#     }
#     for contract in contracts:
#         _, _, amount, name_uz, name_ru = contract
#         formatted_amount = f"{int(amount):,}".replace(",", " ")  # Format amount with spaces
#         response_text['uz'] += f"🔹 {name_uz}: {formatted_amount} so'm\n"
#         response_text['ru'] += f"🔹 {name_ru}: {formatted_amount} сум\n"
#
#     # Create inline keyboard with Back and Close buttons
#     keyboard = InlineKeyboardMarkup()
#     keyboard.add(InlineKeyboardButton(
#         text="⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад",
#         callback_data=f"back_{lang}"
#     ))
#     keyboard.add(InlineKeyboardButton(
#         text="✖️ Yopish" if lang == 'uz' else "✖️ Закрыть",
#         callback_data=f"close_{lang}"
#     ))
#
#     await callback_query.message.edit_text(response_text[lang], reply_markup=keyboard)
#
#
# # Function to handle back button press
# async def handle_back(callback_query: types.CallbackQuery, lang: str):
#     await show_directions(callback_query.message, lang)
#
#
# # Function to handle close button press
# async def handle_close(callback_query: types.CallbackQuery):
#     await callback_query.message.delete()
#
#
# # Registering the callback query handlers
# @dp.callback_query_handler(lambda c: c.data.startswith('direction_'))
# async def process_direction_callback(callback_query: types.CallbackQuery):
#     data = callback_query.data.split('_')
#     direction_id = int(data[1])
#     lang = data[2]
#     await show_contract_prices(callback_query, lang, direction_id)
#
#
# @dp.callback_query_handler(lambda c: c.data.startswith('back_'))
# async def process_back_callback(callback_query: types.CallbackQuery):
#     lang = callback_query.data.split('_')[1]
#     await handle_back(callback_query, lang)
#
#
# @dp.callback_query_handler(lambda c: c.data.startswith('close_'))
# async def process_close_callback(callback_query: types.CallbackQuery):
#     await handle_close(callback_query)
#
#
# # Main handler for contract information
# @dp.message_handler(IsPrivate(), text=["🏷️ Kontrakt summalari", "🏷️ Суммы контрактов"])
# async def contract_information(msg: types.Message):
#     lang = 'uz' if msg.text == "🏷️ Kontrakt summalari" else 'ru'
#     await show_directions(msg, lang)
