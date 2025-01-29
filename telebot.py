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
BOT_TOKEN = "7938484585:AAEuGma-9awLS1RyZGSTiagP_SEc8JChAwk"  # Replace with your bot's token
BOT_USERNAME = "VaultSiBot"  # Replace with your bot's username, without '@'
SUPPORT_ADMINS = ["1578128439","7753388625"]  # Replace with Telegram user IDs of your support team

USER_JOINED_WEBHOOK = "https://hook.us2.make.com/7vhbgvnaseruqs9uuf244yfkqqgx9vuq"
MESSAGE_WEBHOOK = "https://hook.us2.make.com/g4hce715tvne6qvc5tpjw1b3nf73f0ah"  # Replace with your webhook URL


# Function: Trigger webhook for new user joins
async def user_joined(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.new_chat_members[0]
    payload = {
        "user_id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name or "",
        "full_name": f"{user.first_name} {user.last_name or ''}",
        "chat_id": update.message.chat.id,
        "language_code": user.language_code,
        "is_bot": user.is_bot,
        "bio": getattr(user, "bio", "No bio available"),
    }
    try:
        response = requests.post(USER_JOINED_WEBHOOK, json=payload, timeout=10)
        if response.status_code == 200:
            print("User join webhook triggered successfully")
        else:
            print(f"Failed to trigger webhook: {response.status_code}")
            print(f"Error response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error triggering webhook: {str(e)}")



# Function: Trigger webhook for messages (text, media, etc.)
async def trigger_message_webhook(update: Update):
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

    # Capture any media inputs (audio, video, document, etc.) along with text
    if message.audio:
        payload['message']['audio'] = message.audio.to_dict()
    if message.video:
        payload['message']['video'] = message.video.to_dict()
    if message.document:
        payload['message']['document'] = message.document.to_dict()
    if message.photo:
        payload['message']['photo'] = [photo.to_dict() for photo in message.photo]
    if message.voice:
        payload['message']['voice'] = message.voice.to_dict()
    if message.video_note:
        payload['message']['video_note'] = message.video_note.to_dict()

    try:
        response = requests.post(MESSAGE_WEBHOOK, json=payload, timeout=10)
        if response.status_code == 200:
            print("Message webhook triggered successfully")
        else:
            print(f"Failed to trigger webhook: {response.status_code}")
    except Exception as e:
        print(f"Error triggering webhook: {e}")

# Function: Start Command Handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the `/start` command and sends a default welcome message."""
    user = update.effective_user

    if update.message:
        # Default welcome message for `/start` command
        await update.message.reply_text(
            f"Hello {user.first_name}! SiVi here, Join the Next Gen all-in-one (crypto, ai, gaming) community : [TSV Community](https://t.me/TheSignal_Vault1) ! You can use any of these commands to find your way around:\n\n"
            "/getonboarded - Use this to gain full chat access to the community\n\n"
            "/bookcall - Book a call\n"
            "/feedback - Send feedback\n"
            "/help - Get help\n"
            "/support - Talk to a support member\n\n"
            'Or simply send me a personalized message with `@SiVi "your message"` and I will reply to you.\n\n'
            "Don't forget to Network with 50,000+ crypto enthusiasts worldwide. Join Here: [TSV Community](https://t.me/TheSignal_Vault1).",
            parse_mode="Markdown",
        )

# Function: Get Onboarded Command Handler
async def get_onboarded(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the `/getonboarded` command and sends the onboarding message."""
    user = update.effective_user

    onboarding_url = f"https://airtable.com/appXp6xdpgGsIcpf0/shr5klSqw2R3Cipfo?prefill_User%20ID={user.id}"
    keyboard = [[InlineKeyboardButton("Get Onboarded", url=onboarding_url)]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "To get access to the SignalVaut trade insights community. Just click the button below and start earning with our experts trade points and insights",
        reply_markup=reply_markup,
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
	    "onboarding" : get_onboarded,
        }
        if command_text in command_map:
            await command_map[command_text](update, context)

# Function: Book a call
async def book_call(update: Update, context: ContextTypes.DEFAULT_TYPE):
    web_app_url = "http://t.me/VaultSiBot/BookCall"
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
    support_message = " ".join(context.args) if context.args else None

    if not support_message:
        await update.message.reply_text("Please drop your request for support. Example: /support Great bot!")
        return

    await update.message.reply_text("A support member will reach out to you shortly, replies usually takes less than 24hrs. You'll be notified once you get a reply, keep enjoying the SignalVault group experience.")
    admin_message = (
        f"🔔 **New Support Request** 🔔\n\n"
        f"👤 **User Contact**: @{user.username if user.username else 'No username'}\n"
        f"🆔 **User ID**: {user.id}\n"
	f"📩 **Support Request**: {support_message}\n"
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
    message = update.message
    # Trigger the webhook for any kind of message (text, media, etc.)
    await trigger_message_webhook(update)

    # Check if the message contains specific commands or keywords (optional)
    intents = {
        "book_call": ["book a call", "schedule a call"],
        "feedback": ["give feedback", "feedback"],
        "help": ["help", "assist"],
        "support": ["talk to support", "get support"],
	"onboarding": ["how to start", "get onboarded", "start"],
    }

    # Process text messages for specific commands (optional)
    if message.text:
        if any(keyword in message.text.lower() for keyword in intents["book_call"]):
            await redirect_to_private(update, context, "bookcall")
        elif any(keyword in message.text.lower() for keyword in intents["feedback"]):
            await redirect_to_private(update, context, "feedback")
        elif any(keyword in message.text.lower() for keyword in intents["help"]):
            await redirect_to_private(update, context, "help")
        elif any(keyword in message.text.lower() for keyword in intents["support"]):
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
    application.add_handler(CommandHandler("help", lambda u, c: redirect_to_private(u, c, "onboarding")))
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, user_joined))
    application.add_handler(MessageHandler(filters.TEXT, detect_intent))
    application.add_handler(MessageHandler(filters.ALL, detect_intent))  # For all message types

    application.run_polling()

if __name__ == '__main__':
    main()
