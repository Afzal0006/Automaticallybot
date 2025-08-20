from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
from telegram.ext import Application, MessageHandler, filters, CallbackQueryHandler, ContextTypes

# 👉 Tumhara token yaha daalo
TOKEN = "8311824260:AAFeBQwRhoEspYVMOkIaOwKsuuXV4Qfx6JE"
# 👉 Tumhara channel username
REQUIRED_CHANNEL = "@UNIH0"

# ✅ Jab user group join kare
async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        try:
            # check membership
            chat_member = await context.bot.get_chat_member(REQUIRED_CHANNEL, member.id)
            if chat_member.status not in ["member", "administrator", "creator"]:
                raise Exception("Not a member")
        except:
            # mute user
            await context.bot.restrict_chat_member(
                chat_id=update.message.chat.id,
                user_id=member.id,
                permissions=ChatPermissions(can_send_messages=False)
            )

            # send force subscribe msg
            keyboard = InlineKeyboardMarkup(
                [[InlineKeyboardButton("✅ Joined", callback_data=f"checksub_{member.id}")]]
            )
            await context.bot.send_message(
                chat_id=update.message.chat.id,
                text=f"⚠️ Please join {REQUIRED_CHANNEL} to chat in this group.",
                reply_markup=keyboard
            )

# ✅ Button press → re-check
async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = int(query.data.split("_")[1])
    await query.answer()

    try:
        chat_member = await context.bot.get_chat_member(REQUIRED_CHANNEL, user_id)
        if chat_member.status in ["member", "administrator", "creator"]:
            # unmute user
            await context.bot.restrict_chat_member(
                chat_id=query.message.chat.id,
                user_id=user_id,
                permissions=ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_polls=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True,
                    can_invite_users=True
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

    app.run_polling()


if __name__ == "__main__":
    main()
