import os
import requests
from pyrogram import Client, filters

# ===== CONFIG =====
API_ID = int(os.getenv("API_ID", "26014459"))  # Apna API_ID
API_HASH = os.getenv("API_HASH", "34b8791089c72367a5088f96d925f989")  # Apna API_HASH
BOT_TOKEN = os.getenv("BOT_TOKEN", "8232198206:AAHz2GHiKWQAcMKTF-Iz5Nl_Haatsi4ol_o")
OWNER_ID = int(os.getenv("OWNER_ID", "6998916494"))

# TON Price API
def get_ton_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=the-open-network&vs_currencies=usd"
    res = requests.get(url).json()
    return res["the-open-network"]["usd"]

# ===== BOT =====
app = Client("ton_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# /ton command
@app.on_message(filters.command("ton"))
async def ton_price(client, message):
    price = get_ton_price()
    await message.reply_text(f"💎 TON Current Price: **${price}**")

# /convert command
@app.on_message(filters.command("convert"))
async def convert_ton(client, message):
    try:
        args = message.text.split()
        amount = float(args[1])  # Example: /convert 10
        price = get_ton_price()
        usd_value = amount * price
        await message.reply_text(f"🔄 {amount} TON = **${usd_value:.2f} USD**")
    except:
        await message.reply_text("❌ Format: `/convert 10`")

# /afz command (Owner only)
@app.on_message(filters.command("afz"))
async def owner_cmd(client, message):
    if message.from_user.id != OWNER_ID:
        return await message.reply_text("⛔ Only owner can use this command!")
    
    price = get_ton_price()
    await message.reply_text(f"👑 Owner Command → TON Price: **${price}**")

# Run bot
app.run()
