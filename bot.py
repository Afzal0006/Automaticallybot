import aiohttp
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# === CONFIG ===
BOT_TOKEN = "8409625869:AAEpysnBH7MXtL508kxa5XfSpNkvK8jlvFg"

# === Fetch TON Price ===
async def get_ton_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=the-open-network&vs_currencies=usd&include_24hr_change=true"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            price = data["the-open-network"]["usd"]
            change = data["the-open-network"]["usd_24h_change"]
            return price, change

# === /ton Command ===
async def ton_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price, change = await get_ton_price()
    msg = f"💎 TON Price: **${price:.2f}**\n📉 24h Change: {change:.2f}%"
    await update.message.reply_text(msg, parse_mode="Markdown")

# === /convert Command ===
async def convert_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not context.args:
            await update.message.reply_text("⚠️ Usage: /convert {amount}\nExample: /convert 10")
            return
        
        amount = float(context.args[0])
        price, _ = await get_ton_price()
        usd_value = amount * price
        msg = f"🔄 {amount} TON ≈ **${usd_value:.2f} USD**"
        await update.message.reply_text(msg, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text("❌ Error: Please enter a valid number.\nExample: /convert 10")

# === Main ===
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("ton", ton_handler))
    app.add_handler(CommandHandler("convert", convert_handler))
    app.run_polling()

if __name__ == "__main__":
    main()
