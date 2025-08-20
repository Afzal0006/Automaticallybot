from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    InlineQueryHandler,
    filters,
)
import uuid

# ===== Bot Token =====
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# ===== Start Command =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! I am your Calculator Bot.\n"
        "Send me a math expression like:\n"
        "`12*5` for 12×5\n"
        "`10/2` for 10÷2\n"
        "I support +, -, *, /, and parentheses.\n"
        "You can also use me inline in any chat: @YourBot 12*5"
    )

# ===== Handle Normal Messages =====
async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    expr = update.message.text
    expr_display = expr.replace("*", "×").replace("/", "÷")
    try:
        result = eval(expr.replace("×", "*").replace("÷", "/"))
        await update.message.reply_text(f"{expr_display} = {result}")
    except Exception:
        await update.message.reply_text("Invalid expression! Please send a valid math formula.")

# ===== Handle Inline Queries =====
async def inline_calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return

    expr_display = query.replace("*", "×").replace("/", "÷")
    try:
        result = eval(query.replace("×", "*").replace("÷", "/"))
        answer_text = f"{expr_display} = {result}"
    except Exception:
        answer_text = "Invalid expression!"

    results = [
        InlineQueryResultArticle(
            id=str(uuid.uuid4()),
            title="Calculator Result",
            input_message_content=InputTextMessageContent(answer_text),
            description=answer_text
        )
    ]
    await update.inline_query.answer(results, cache_time=0)

# ===== Main Application =====
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, calculate))
app.add_handler(InlineQueryHandler(inline_calc))

print("Bot is running...")
app.run_polling()
