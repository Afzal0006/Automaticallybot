import aiohttp
import asyncio
import datetime
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "8411607342:AAHSDSB98MDYeuYMZUk6nHqKtZy2zquhVig"  # yaha apna token daalna

# ==== Fetch TON Data ====
async def fetch_ton_data():
    url = "https://api.coingecko.com/api/v3/coins/the-open-network?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=true"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            market = data["market_data"]
            price = market["current_price"]["usd"]
            daily = market["price_change_percentage_24h"]
            weekly = market["price_change_percentage_7d"]
            sparkline = market["sparkline_7d"]["price"]
            return price, daily, weekly, sparkline

# ==== Image Card Create ====
def create_card(price, daily, weekly, sparkline):
    plt.figure(figsize=(6,2))
    plt.plot(sparkline, color="red")
    plt.axis("off")
    plt.savefig("chart.png", transparent=True, bbox_inches='tight', pad_inches=0)
    plt.close()

    img = Image.new("RGB", (1200, 600), (32, 152, 232))  # blue bg
    draw = ImageDraw.Draw(img)
    card = Image.new("RGB", (1100, 500), (0, 0, 0))
    img.paste(card, (50, 50))

    font_big = ImageFont.truetype("arial.ttf", 100)
    draw.text((80, 80), f"${price:.2f}", font=font_big, fill=(0, 200, 255))

    font_mid = ImageFont.truetype("arial.ttf", 50)
    draw.text((80, 250), f"Daily: {daily:.2f}%", font=font_mid, fill=(255, 50, 50))
    draw.text((80, 330), f"Weekly: {weekly:.2f}%", font=font_mid, fill=(255, 50, 50))

    today = datetime.date.today().strftime("%b %d, %Y")
    font_small = ImageFont.truetype("arial.ttf", 40)
    draw.text((80, 420), f"📅 {today}", font=font_small, fill=(200, 200, 200))

    chart = Image.open("chart.png").resize((1000, 200))
    img.paste(chart, (100, 380), chart)

    img.save("ton_price.png")
    return "ton_price.png"

# ==== /ton Command ====
async def ton_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price, daily, weekly, sparkline = await fetch_ton_data()
    path = create_card(price, daily, weekly, sparkline)
    await update.message.reply_photo(photo=open(path, "rb"), caption="📊 Toncoin Price Update")

# ==== Bot Start ====
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("ton", ton_handler))
    print("🤖 Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
