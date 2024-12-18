from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Bot username
BOT_USERNAME = "VaultSignalBot"  # Replace with your bot's username, without '@'

# List of group admins or support team members
SUPPORT_ADMINS = [7753388625]  # Replace with Telegram user IDs of your support team


# Function to redirect users to private chat
async def redirect_to_private(update: Update, context: ContextTypes.DEFAULT_TYPE, command_text: str):
    """Redirect users to private chat if command is triggered in a group."""
    if update.message.chat.type != "private":  # Triggered in a group
        # Create an inline keyboard with a link to the bot's private chat
        button = [
            [InlineKeyboardButton(f"Talk to SiVi", url=f"https://t.me/{BOT_USERNAME}?start=start{command_text}")]
        ]
        reply_markup = InlineKeyboardMarkup(button)
        await update.message.reply_text(
            f" For `{command_text}` , Chat SiVi Directly",
            reply_markup=reply_markup
        )
        
    else:
        # Execute the appropriate command if already in private chat
        if command_text == "bookcall":
            await book_call(update, context)
        elif command_text == "feedback":
            await feedback(update, context)
        elif command_text == "support":
            await support(update, context)
        elif command_text == "help":
            await help_command(update, context)


# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome message and command list."""
    await update.message.reply_text(
        "Welcome! Use the following commands:\n\n"
        "/bookcall - Book a call\n"
        "/feedback - Send feedback\n"
        "/help - Get help\n"
        "/support - Talk to a support member"
    )


# Command: /bookcall
async def book_call(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Provide a booking link."""
    web_app_url = "https://t.me/VaultSignalBot/Sigvault"  # Replace with your URL
    keyboard = [[InlineKeyboardButton("Book a Call", url=web_app_url)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Click below to book a call:", reply_markup=reply_markup)


# Command: /feedback
async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user feedback and notify support admins."""
    user = update.message.chat
    username = user.username
    user_id = user.id
    feedback_message = " ".join(context.args)  # Extract user feedback

    if not feedback_message:
        await update.message.reply_text("Please provide feedback after the command. Example: /feedback Great bot!")
        return

    # Send confirmation to the user
    await update.message.reply_text("Thank you for your feedback! Your input is valuable to us.")

    # Notify support admins
    admin_message = (
        f"🔔 **New Feedback Submitted** 🔔\n\n"
        f"👤 **User Contact**: @{username if username else 'No username'}\n"
        f"🆔 **User ID**: {user_id}\n"
        f"📩 **Feedback**: {feedback_message}\n\n"
    )

    for admin_id in SUPPORT_ADMINS:
        try:
            await context.bot.send_message(chat_id=admin_id, text=admin_message)
        except Exception as e:
            print(f"Error notifying admin {admin_id}: {e}")


# Command: /support
async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Connect user with support and notify admins."""
    user = update.message.chat
    username = user.username
    user_id = user.id
    await update.message.reply_text("A support member will reach out to you shortly. Please hold on.")

    # Notify admins
    admin_message = (
        f"🔔 **New Support Request** 🔔\n\n"
        f"👤 **User Contact**: @{username if username else 'No username'}\n"
        f"🆔 **User ID**: {user_id}\n"
    )
    for admin_id in SUPPORT_ADMINS:
        try:
            await context.bot.send_message(chat_id=admin_id, text=admin_message)
        except Exception as e:
            print(f"Error notifying admin {admin_id}: {e}")


# Command: /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Provide help information."""
    await update.message.reply_text(
        "Need help? Use:\n"
        "/bookcall - Book a call\n"
        "/feedback - Send feedback\n"
        "/support - Talk to support"
    )


# Command Handlers (with redirection logic)
async def handle_book_call(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await redirect_to_private(update, context, "bookcall")


async def handle_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await redirect_to_private(update, context, "feedback")


async def handle_support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await redirect_to_private(update, context, "support")


async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await redirect_to_private(update, context, "help")


# Intent detection handler
async def detect_intent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Detect user intents based on message content."""
    message = update.message.text.lower()

    intents = {
        "book_call": ["book a call", "schedule a call"],
        "feedback": ["give feedback", "feedback"],
        "help": ["help", "assist"],
        "support": ["talk to support", "get support"],
    }

    if any(keyword in message for keyword in intents["book_call"]):
        await handle_book_call(update, context)
    elif any(keyword in message for keyword in intents["feedback"]):
        await handle_feedback(update, context)
    elif any(keyword in message for keyword in intents["help"]):
        await handle_help(update, context)
    elif any(keyword in message for keyword in intents["support"]):
        await handle_support(update, context)


# Main function
def main():
    TOKEN = "7225931117:AAFP4haOX6lHuTFvsElH-KhzYRNC53noF_M"  # Replace with your bot's token
    application = Application.builder().token(TOKEN).build()

    # Command Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("bookcall", handle_book_call))
    application.add_handler(CommandHandler("feedback", handle_feedback))
    application.add_handler(CommandHandler("support", handle_support))
    application.add_handler(CommandHandler("help", handle_help))

    # Message Handler for intent detection
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, detect_intent))

    # Start the bot
    application.run_polling()


if __name__ == "__main__":
    main()
