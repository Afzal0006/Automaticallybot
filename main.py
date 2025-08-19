import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ===== CONFIG =====
BOT_TOKEN = "8232198206:AAHz2GHiKWQAcMKTF-Iz5Nl_Haatsi4ol_o"
OWNER_ID = 6998916494

# TON Price API
def get_ton_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=the-open-network&vs_currencies=usd"
    res = requests.get(url).json()
    return res["the-open-network"]["usd"]

# /ton command
async def ton_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price = get_ton_price()
    await update.message.reply_text(f"💎 TON Current Price: **${price}**")

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
    await update.message.reply_text(f"👑 Owner Command → TON Price: **${price}**")

# MAIN
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("ton", ton_price))
    app.add_handler(CommandHandler("convert", convert_ton))
    app.add_handler(CommandHandler("afz", afz))

    # ye line event loop ko safe tarike se handle karti hai
    app.run_polling()

if __name__ == "__main__":
    main()
