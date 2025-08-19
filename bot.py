import asyncio
import aiohttp
from pyrogram import Client, filters

# ==== CONFIG ====
API_ID = 24024383
API_HASH = "e4defcf520c9333e56196378440e990c"
BOT_TOKEN = "8411607342:AAHSDSB98MDYeuYMZUk6nHqKtZy2zquhVig"

app = Client("TonPriceBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# 🔹 TON Price Fetch Function
async def get_ton_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=the-open-network&vs_currencies=usd"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            return data["the-open-network"]["usd"]

# 🔹 /price command
@app.on_message(filters.command("price"))
async def price_handler(client, message):
    price = await get_ton_price()
    await message.reply_text(f"💎 Current TON Price: **${price} USD**")

print("🤖 Bot is running...")
app.run()
