import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatPermissions
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import json

# Bot Token and Webhook URLs
BOT_TOKEN = "7225931117:AAFP4haOX6lHuTFvsElH-KhzYRNC53noF_M"  # Replace with your bot's token
BOT_USERNAME = "VaultSignalBot"  # Replace with your bot's username, without '@'
SUPPORT_ADMINS = [7753388625]  # Replace with Telegram user IDs of your support team

USER_JOINED_WEBHOOK = "https://hook.us2.make.com/7vhbgvnaseruqs9uuf244yfkqqgx9vuq"
START_COMMAND_WEBHOOK = "https://hook.us2.make.com/1i7p27dunhnpint7bouo92ocm4hwsf5p"


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
    except Exception as e:
        print(f"Error triggering webhook: {e}")


# Function: Trigger webhook for /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id

    await context.bot.send_message(chat_id=chat_id, text="👋 Welcome! I am processing your details...")

    payload = {
        "user_id": user.id,
        "username": user.username or "Anonymous",
        "first_name": user.first_name,
        "last_name": user.last_name or "",
        "chat_id": chat_id,
    }
    try:
        requests.post(START_COMMAND_WEBHOOK, json=payload, timeout=10)
    except Exception as e:
        print(f"Error triggering webhook: {e}")

    await context.bot.send_message(chat_id=chat_id, text="✅ Done! You can start interacting with me now.")


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
