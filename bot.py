from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
from telegram.ext import Application, MessageHandler, filters, CallbackQueryHandler, ContextTypes

TOKEN = "8311824260:AAFeBQwRhoEspYVMOkIaOwKsuuXV4Qfx6JE"   # tumhara token
REQUIRED_CHANNEL = "@UNIH0"   # tumhara channel

# ✅ Jab user group join kare
async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        try:
            chat_member = await context.bot.get_chat_member(REQUIRED_CHANNEL, member.id)
            if chat_member.status not in ["member", "administrator", "creator"]:
                raise Exception("Not a member")
        except:
            # Mute user
            await context.bot.restrict_chat_member(
                chat_id=update.message.chat.id,
                user_id=member.id,
                permissions=ChatPermissions(can_send_messages=False)
            )

            # Send Force Subscribe message
            keyboard = InlineKeyboardMarkup(
                [[InlineKeyboardButton("✅ Joined", callback_data=f"checksub_{member.id}")]]
            )
            await update.effective_chat.send_message(
                text=f"⚠️ Please join {REQUIRED_CHANNEL} to chat in this group.",
                reply_markup=keyboard
            )

# ✅ Jab user button dabaye
async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = int(query.data.split("_")[1])
    await query.answer()

    try:
        chat_member = await context.bot.get_chat_member(REQUIRED_CHANNEL, user_id)
        if chat_member.status in ["member", "administrator", "creator"]:
            # Unmute user
            await context.bot.restrict_chat_member(
                chat_id=query.message.chat.id,
                user_id=user_id,
                permissions=ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_other_messages=True,
                    can_send_polls=True
                )
            )
            await query.edit_message_text("✅ Verified! You can now chat.")
        else:
            await query.answer("❌ You have not joined the channel yet!", show_alert=True)
    except:
        await query.answer("❌ You have not joined the channel yet!", show_alert=True)

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member))
    app.add_handler(CallbackQueryHandler(check_subscription, pattern=r"checksub_\d+"))

    # 🔥 Heroku fix (no "event loop closed" error)
    app.run_polling(close_loop=False)

if __name__ == "__main__":
    main()
