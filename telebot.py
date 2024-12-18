import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# Bot Token and Webhook URLs
BOT_TOKEN = "7225931117:AAFP4haOX6lHuTFvsElH-KhzYRNC53noF_M"  # Replace with your bot's token
BOT_USERNAME = "VaultSignalBot"  # Replace with your bot's username, without '@'
WEBHOOK_URL = "https://hook.us2.make.com/1i7p27dunhnpint7bouo92ocm4hwsf5p"
SUPPORT_ADMINS = [7753388625]  # Replace with Telegram user IDs of your support team
USER_JOINED_WEBHOOK = "https://hook.us2.make.com/7vhbgvnaseruqs9uuf244yfkqqgx9vuq"

# Function: Trigger webhook for specific messages
async def trigger_webhook(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    payload = {
        "update_id": update.update_id,
        "message": {
            "message_id": message.message_id,
            "from": {
                "id": message.from_user.id,
                "is_bot": message.from_user.is_bot,
                "first_name": message.from_user.first_name,
                "last_name": message.from_user.last_name or "",
                "username": message.from_user.username,
                "language_code": message.from_user.language_code,
            },
            "chat": {
                "id": message.chat.id,
                "first_name": getattr(message.chat, "first_name", None),
                "last_name": getattr(message.chat, "last_name", None),
                "username": getattr(message.chat, "username", None),
                "type": message.chat.type,
                "title": getattr(message.chat, "title", None),
            },
            "date": message.date.isoformat(),
            "text": message.text,
            "entities": [entity.to_dict() for entity in message.entities] if message.entities else None,
            "photo": [photo.to_dict() for photo in message.photo] if message.photo else None,
            "audio": message.audio.to_dict() if message.audio else None,
            "document": message.document.to_dict() if message.document else None,
            "video": message.video.to_dict() if message.video else None,
            "video_note": message.video_note.to_dict() if message.video_note else None,
            "voice": message.voice.to_dict() if message.voice else None,
            "sticker": message.sticker.to_dict() if message.sticker else None,
            "contact": message.contact.to_dict() if message.contact else None,
            "dice": message.dice.to_dict() if message.dice else None,
            "poll": message.poll.to_dict() if message.poll else None,
            "venue": message.venue.to_dict() if message.venue else None,
            "location": message.location.to_dict() if message.location else None,
            "new_chat_members": [member.to_dict() for member in message.new_chat_members] if message.new_chat_members else None,
            "left_chat_member": message.left_chat_member.to_dict() if message.left_chat_member else None,
            "pinned_message": message.pinned_message.to_dict() if message.pinned_message else None,
            "caption": message.caption if message.caption else None,
            "reply_to_message": message.reply_to_message.to_dict() if message.reply_to_message else None,
        },
    }
    try:
        response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        if response.status_code == 200:
            print("Webhook triggered successfully")
        else:
            print(f"Failed to trigger webhook: {response.status_code}")
    except Exception as e:
        print(f"Error triggering webhook: {e}")

# Handler for filtering messages
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    # Ignore command messages or /start explicitly
    if message.entities:
        for entity in message.entities:
            if entity.type == "bot_command":
                return

    # Trigger webhook if message matches criteria
    if (
        message.text and not message.text.startswith("/start") and (
            message.text.startswith("/SiVi") or  # Message starts with /SiVi
            message.photo or message.audio or message.sticker or not message.entities
        )
    ):
        await trigger_webhook(update, context)

# Function: Start Command Handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if update.message:
        await update.message.reply_text(
            f"Hello {user.first_name}! SiVi here, your best AI assistant! You can use any of these commands to find your way around:\n\n"
            "/getonboarded - Use this to get access to the Signal Vault discussion group\n\n"
            "/bookcall - Book a call\n"
            "/feedback - Send feedback\n"
            "/help - Get help\n"
            "/support - Talk to a support member\n\n"
            'Or simply send me a personalized message with `/SiVi "your message"` and I will reply to you.\n\n'
            "Always join the great and brilliant minds @ the discussion group whenever: [Group Discussion Here](https://t.me/beastvault).",
            parse_mode="Markdown",
        )

# Function: Redirect to private chat if needed
async def redirect_to_private(update: Update, context: ContextTypes.DEFAULT_TYPE, command_text: str):
    if update.message.chat.type != "private":
        button = [
            [InlineKeyboardButton(f"Talk to SiVi", url=f"https://t.me/{BOT_USERNAME}?start=start{command_text}")]
        ]
        reply_markup = InlineKeyboardMarkup(button)
        await update.message.reply_text(
            f"For `{command_text}`, chat with SiVi directly.",
            reply_markup=reply_markup,
        )
    else:
        command_map = {
            "bookcall": book_call,
            "feedback": feedback,
            "support": support,
            "help": help_command,
            "start": start,
        }
        if command_text in command_map:
            await command_map[command_text](update, context)

# Function: Book a call
async def book_call(update: Update, context: ContextTypes.DEFAULT_TYPE):
    web_app_url = "https://t.me/VaultSignalBot/Sigvault"
    keyboard = [[InlineKeyboardButton("Book a Call", url=web_app_url)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Click below to book a call:", reply_markup=reply_markup)

# Function: Feedback
async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.chat
    feedback_message = " ".join(context.args) if context.args else None

    if not feedback_message:
        await update.message.reply_text("Please provide feedback after the command. Example: /feedback Great bot!")
        return

    await update.message.reply_text("Thank you for your feedback! Your input is valuable to us.")
    admin_message = (
        f"🔔 **New Feedback Submitted** 🔔\n\n"
        f"👤 **User Contact**: @{user.username if user.username else 'No username'}\n"
        f"🆔 **User ID**: {user.id}\n"
        f"📩 **Feedback**: {feedback_message}\n"
    )
    for admin_id in SUPPORT_ADMINS:
        try:
            await context.bot.send_message(chat_id=admin_id, text=admin_message)
        except Exception as e:
            print(f"Error notifying admin {admin_id}: {e}")

# Function: Support
async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.chat
    await update.message.reply_text("A support member will reach out to you shortly. Please hold on.")
    admin_message = (
        f"🔔 **New Support Request** 🔔\n\n"
        f"👤 **User Contact**: @{user.username if user.username else 'No username'}\n"
        f"🆔 **User ID**: {user.id}\n"
    )
    for admin_id in SUPPORT_ADMINS:
        try:
            await context.bot.send_message(chat_id=admin_id, text=admin_message)
        except Exception as e:
            print(f"Error notifying admin {admin_id}: {e}")

# Function: Help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Need help? Use:\n"
        "/bookcall - Book a call\n"
        "/feedback - Send feedback\n"
        "/support - Talk to support"
    )

# Function: Detect intent based on user messages
async def detect_intent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text.lower()
    intents = {
        "book_call": ["book a call", "schedule a call"],
        "feedback": ["give feedback", "feedback"],
        "help": ["help", "assist"],
        "support": ["talk to support", "get support"],
    }
    if any(keyword in message for keyword in intents["book_call"]):
        await redirect_to_private(update, context, "bookcall")
    elif any(keyword in message for keyword in intents["feedback"]):
        await redirect_to_private(update, context, "feedback")
    elif any(keyword in message for keyword in intents["help"]):
        await redirect_to_private(update, context, "help")
    elif any(keyword in message for keyword in intents["support"]):
        await redirect_to_private(update, context, "support")

# Main function
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("getonboarded", get_onboarded))
    application.add_handler(CommandHandler("bookcall", lambda u, c: redirect_to_private(u, c, "bookcall")))
    application.add_handler(CommandHandler("feedback", lambda u, c: redirect_to_private(u, c, "feedback")))
    application.add_handler(CommandHandler("support", lambda u, c: redirect_to_private(u, c, "support")))
    application.add_handler(CommandHandler("help", lambda u, c: redirect_to_private(u, c, "help")))
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, user_joined))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, detect_intent))

    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
