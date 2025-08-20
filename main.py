from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
from telegram.ext import Application, CommandHandler, ChatMemberHandler, CallbackQueryHandler, ContextTypes
import logging

logging.basicConfig(level=logging.INFO)

TOKEN = "8311824260:AAFeBQwRhoEspYVMOkIaOwKsuuXV4Qfx6JE"

REQUIRED_TEXT = "@UNIH0"

# ✅ Jab user group join kare
async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.chat_member.new_chat_members:
        bio = (await context.bot.get_chat(member.id)).bio or ""

        if REQUIRED_TEXT not in bio:
            # mute user
            await context.bot.restrict_chat_member(
                chat_id=update.chat_member.chat.id,
                user_id=member.id,
                permissions=ChatPermissions(can_send_messages=False)
            )

            # send warning with button
            keyboard = InlineKeyboardMarkup(
                [[InlineKeyboardButton("✅ Done", callback_data=f"checkbio_{member.id}")]]
            )
            await context.bot.send_message(
                chat_id=update.chat_member.chat.id,
                text="Please use @UNIH0 this in your Bio",
                reply_markup=keyboard
            )


# ✅ Jab user Done button dabaye
async def check_bio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = int(query.data.split("_")[1])
    await query.answer()

    bio = (await context.bot.get_chat(user_id)).bio or ""

    if REQUIRED_TEXT in bio:
        # unmute user
        await context.bot.restrict_chat_member(
            chat_id=query.message.chat.id,
            user_id=user_id,
            permissions=ChatPermissions(can_send_messages=True,
                                        can_send_media_messages=True,
                                        can_send_polls=True,
                                        can_send_other_messages=True,
                                        can_add_web_page_previews=True,
                                        can_change_info=False,
                                        can_invite_users=True,
                                        can_pin_messages=False)
        )
        await query.edit_message_text("✅ Verified! User unmuted.")
    else:
        await query.answer("❌ Bio me @UNIH0 nahi mila!", show_alert=True)


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(ChatMemberHandler(new_member, ChatMemberHandler.CHAT_MEMBER))
    app.add_handler(CallbackQueryHandler(check_bio, pattern=r"checkbio_\d+"))

    app.run_polling()


if __name__ == "__main__":
    main()
