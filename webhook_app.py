from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook

API_TOKEN = ''
WEBHOOK_HOST = '/'
WEBHOOK_PATH = '/'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# Set webhook
async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)


# Remove webhook
async def on_shutdown(dp):
    await bot.delete_webhook()


# Define your handlers
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Hello!")


if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host='0.0.0.0',
        port=3000,
    )
