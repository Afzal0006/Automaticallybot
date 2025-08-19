import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ===== CONFIG =====
BOT_TOKEN = "8232198206:AAHz2GHiKWQAcMKTF-Iz5Nl_Haatsi4ol_o"
OWNER_ID = 6998916494
CHANNEL_ID = -1002161414780  # Aapke channel ka ID

# TON Price API
def get_ton_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=the-open-network&vs_currencies=usd"
    res = requests.get(url).json()
    return res["the-open-network"]["usd"]

# /ton command
async def ton_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price = get_ton_price()
    await update.message.reply_text(f"💎 TON Current Price: ${price}")

# /convert command
async def convert_ton(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        amount = float(context.args[0])  # Example: /convert 10
        price = get_ton_price()
        usd_value = amount * price
        await update.message.reply_text(f"🔄 {amount} TON = **${usd_value:.2f} USD**")
    except:
        await update.message.reply_text("❌ Format: `/convert 10`")

# /afz command (Owner only)
async def afz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return await update.message.reply_text("⛔ Only owner can use this command!")

    price = get_ton_price()
    await update.message.reply_text(f"👑 Owner Command → TON Price: ${price}")

# 🔄 Har 30 sec me price bhejne wala function
async def send_price_to_channel(context: ContextTypes.DEFAULT_TYPE):
    price = get_ton_price()
    await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text=f"📊 TON Current Price: **${price}**"
    )

# MAIN
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("ton", ton_price))
    app.add_handler(CommandHandler("convert", convert_ton))
    app.add_handler(CommandHandler("afz", afz))

    # ✅ Yaha job schedule karne ka sahi tarika
    async def start_jobs(application: Application):
        application.job_queue.run_repeating(send_price_to_channel, interval=30, first=5)

    # run_polling ke andar jobs init ho jayenge
    app.run_polling(after_startup=start_jobs)

if __name__ == "__main__":
    main()
