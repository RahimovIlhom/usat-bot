from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import WrongFileIdentifier, BadRequest

from filters import IsPrivate
from keyboards.default import sub_menu_markup_uz, sub_menu_markup_ru
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

    info_text = {
        'uz': ("🏢 Fan va texnologiyalari universiteti haqida ma'lumot:\n\n"
               "🔗 [Rasmiy sayt](https://usat.uz)\n"
               "📝 [Universitetga hujjat topshirish](https://qabul.usat.uz) yoki [@usat_bot](https://t.me/usat_bot)\n"
               "📞 Call-center: +99878-888-38-88\n\n"
               "USAT Universiteti O'zbekistondagi yetakchi oliy ta'lim muassasalaridan biri bo'lib, zamonaviy va innovatsion ta'lim dasturlarini taklif etadi. "
               "Universitet fan va texnologiyalar bo'yicha ko'plab yo'nalishlarda ta'lim beradi. Kurslar quyidagi shakllarda o'tkaziladi: kunduzgi, kechki va sirtqi ta'lim.\n\n"
               "📍 Manzil: Toshkent shahri, Algoritm dahasi, Diydor ko'chasi 71-uy\n"
               "📢 Telegram kanalimiz: [@usatuzb](https://t.me/usatuzb)"),
        'ru': ("🏢 Информация об университете наук и технологий:\n\n"
               "🔗 [Официальный сайт](https://usat.uz)\n"
               "📝 [Подача документов в университет](https://qabul.usat.uz) или [@usat_bot](https://t.me/usat_bot)\n"
               "📞 Колл-центр: +99878-888-38-88\n\n"
               "Университет USAT является одним из ведущих высших учебных заведений в Узбекистане, предлагая современные и инновационные образовательные программы. "
               "Университет предоставляет обучение по многим направлениям науки и технологий. Курсы проводятся в дневной, вечерней и заочной формах обучения.\n\n"
               "📍 Адрес: город Ташкент, район Алгоритм, улица Дийдор, дом 71\n"
               "📢 Наш Telegram канал: [@usatuzb](https://t.me/usatuzb)")
    }

    image_url = 'https://qabul.usat.uz/img/about_usat.83a3c120.png'
    try:
        await msg.answer_photo(photo=image_url, caption=info_text[lang], parse_mode=types.ParseMode.MARKDOWN)
    except (WrongFileIdentifier, BadRequest, ValueError, Exception):
        await msg.answer(info_text[lang], parse_mode=types.ParseMode.MARKDOWN)


@dp.message_handler(IsPrivate(),
                    text=["👨‍🎓 Universitetdagi ta'lim yo'nalishlari", "👨‍🎓 Направления обучения в университете"])
async def direction_of_education_information(msg: types.Message):
    lang = 'uz' if msg.text == "👨‍🎓 Universitetdagi ta'lim yo'nalishlari" else 'ru'

    # Define a function to execute the query and fetch results
    async def select_active_directions():
        query = "SELECT id, nameUz, nameRu FROM educational_areas WHERE active = TRUE;"
        return await db.execute_query(query, fetchall=True)

    # Fetch active directions
    directions = await select_active_directions()

    if not directions:
        no_directions_text = {
            'uz': "Hozirda hech qanday ta'lim yo'nalishlari mavjud emas.",
            'ru': "На данный момент нет направлений обучения."
        }
        await msg.answer(no_directions_text[lang])
        return

    response_text = {
        'uz': "👨‍🎓 Universitetdagi ta'lim yo'nalishlari:\n\n",
        'ru': "👨‍🎓 Направления обучения в университете:\n\n"
    }

    for direction in directions:
        direction_id, name_uz, name_ru = direction
        response_text['uz'] += f"🔹 {name_uz}\n"
        response_text['ru'] += f"🔹 {name_ru}\n"

    await msg.answer(response_text[lang])


# Function to fetch and show directions with inline buttons
async def show_directions(msg: types.Message, lang: str):
    directions = await db.select_directions()
    if not directions:
        no_contracts_text = {
            'uz': "Hozirda hech qanday kontrakt summasi mavjud emas.",
            'ru': "На данный момент нет сумм контрактов."
        }
        await msg.answer(no_contracts_text[lang])
        return

    # Create inline keyboard with directions
    keyboard = InlineKeyboardMarkup()
    for direction in directions:
        direction_id, name_uz, name_ru, active = direction
        if active:
            keyboard.add(InlineKeyboardButton(
                text=f"🔹 {name_uz}" if lang == 'uz' else f"🔹 {name_ru}",
                callback_data=f"direction_{direction_id}_{lang}"
            ))

    # Add Close button
    keyboard.add(InlineKeyboardButton(
        text="✖️ Yopish" if lang == 'uz' else "✖️ Закрыть",
        callback_data=f"close_{lang}"
    ))
    try:
        await msg.edit_text(
            text="👨‍🎓 Qaysi ta'lim yo'nalishi bo'yicha kontrakt summasini ko'rmoqchisiz?"
            if lang == 'uz' else "👨‍🎓 По какому направлению вы хотите узнать суммы контрактов?",
            reply_markup=keyboard
        )
    except BadRequest:
        await msg.answer(
            text="👨‍🎓 Qaysi ta'lim yo'nalishi bo'yicha kontrakt summasini ko'rmoqchisiz?"
            if lang == 'uz' else "👨‍🎓 По какому направлению вы хотите узнать суммы контрактов?",
            reply_markup=keyboard
        )


# Function to display contract prices for a selected direction
async def show_contract_prices(callback_query: types.CallbackQuery, lang: str, direction_id: int):
    contracts = await db.select_contract_prices_for_direction(direction_id)
    if not contracts:
        no_contracts_text = {
            'uz': "Hozirda hech qanday kontrakt summasi mavjud emas.",
            'ru': "На данный момент нет сумм контрактов."
        }
        await callback_query.message.edit_text(no_contracts_text[lang])
        return

    # Create response text with contract prices
    response_text = {
        'uz': "🏷️ Kontrakt summalari:\n\n",
        'ru': "🏷️ Суммы контрактов:\n\n"
    }
    for contract in contracts:
        _, _, amount, name_uz, name_ru = contract
        formatted_amount = f"{int(amount):,}".replace(",", " ")  # Format amount with spaces
        response_text['uz'] += f"🔹 {name_uz}: {formatted_amount} so'm\n"
        response_text['ru'] += f"🔹 {name_ru}: {formatted_amount} сум\n"

    # Create inline keyboard with Back and Close buttons
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(
        text="⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад",
        callback_data=f"back_{lang}"
    ))
    keyboard.add(InlineKeyboardButton(
        text="✖️ Yopish" if lang == 'uz' else "✖️ Закрыть",
        callback_data=f"close_{lang}"
    ))

    await callback_query.message.edit_text(response_text[lang], reply_markup=keyboard)


# Function to handle back button press
async def handle_back(callback_query: types.CallbackQuery, lang: str):
    await show_directions(callback_query.message, lang)


# Function to handle close button press
async def handle_close(callback_query: types.CallbackQuery):
    await callback_query.message.delete()


# Registering the callback query handlers
@dp.callback_query_handler(lambda c: c.data.startswith('direction_'))
async def process_direction_callback(callback_query: types.CallbackQuery):
    data = callback_query.data.split('_')
    direction_id = int(data[1])
    lang = data[2]
    await show_contract_prices(callback_query, lang, direction_id)


@dp.callback_query_handler(lambda c: c.data.startswith('back_'))
async def process_back_callback(callback_query: types.CallbackQuery):
    lang = callback_query.data.split('_')[1]
    await handle_back(callback_query, lang)


@dp.callback_query_handler(lambda c: c.data.startswith('close_'))
async def process_close_callback(callback_query: types.CallbackQuery):
    await handle_close(callback_query)


# Main handler for contract information
@dp.message_handler(IsPrivate(), text=["🏷️ Kontrakt summalari", "🏷️ Суммы контрактов"])
async def contract_information(msg: types.Message):
    lang = 'uz' if msg.text == "🏷️ Kontrakt summalari" else 'ru'
    await show_directions(msg, lang)
