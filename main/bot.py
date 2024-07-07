# telegram_bot.py
import asyncio
from telegram import Bot
from telegram.constants import ParseMode

API_TOKEN = '7114193945:AAGA7iaEbIBZowqB4iN6S_fn2sv-iwaNR4c'
CHANNEL_ID = '@tech_news_uz_official'

bot = Bot(token=API_TOKEN)

async def send_message(message, image_url=None):
    if image_url:
        await bot.send_photo(chat_id=CHANNEL_ID, photo=image_url, caption=message, parse_mode=ParseMode.HTML)
    else:
        await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode=ParseMode.HTML)

def send_message_sync(message, image_url=None):
    asyncio.run(send_message(message, image_url))
