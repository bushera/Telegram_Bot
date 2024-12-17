from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# Bot username
BOT_USERNAME = "@VaultSignalBot"  # Replace with your bot's username

# Function to redirect users to private chat
async def redirect_to_private(update: Update, context: ContextTypes.DEFAULT_TYPE, command_text: str):
    if update.message.chat.type != "private":  # Only trigger redirection in group chats
        button = [[InlineKeyboardButton("Click here to chat with me privately 🤖", url=f"https://t.me/{BOT_USERNAME}?start=start")]]
        reply_markup = InlineKeyboardMarkup(button)
        await update.message.reply_text(
            f"Please start a private chat with me to use the `{command_text}` command. Click below 👇:",
            reply_markup=reply_markup
        )
    else:
        # If the user is already in private chat, execute the command
        if command_text == "bookcall":
            await book_call(update, context)
        elif command_text == "feedback":
            await feedback(update, context)
        elif command_text == "support":
            await support(update, context)
        elif command_text == "help":
            await help(update, context)


# List of group admins or support team members
SUPPORT_ADMINS = [7753388625]  # Replace with Telegram user IDs of your support team

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! Use the following commands:\n\n"
        "/bookcall - Book a call\n"
        "/feedback - Send feedback\n"
        "/help - Get help\n"
        "/support - Talk to a support member"
    )

# Command: /bookcall
async def book_call(update: Update, context: ContextTypes.DEFAULT_TYPE):
    web_app_url = "https://t.me/VaultSignalBot/Sigvault"  # Replace with your URL
    keyboard = [[InlineKeyboardButton("Book a Call", url=web_app_url)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Click below to book a call:", reply_markup=reply_markup)


# Command: /feedback
async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.chat  # Get user details
    username = user.username  # Username of the user
    user_id = user.id  # Telegram user ID
    
    # Generate the direct link to the user's profile
    if username:
        user_link = f"https://t.me/{username}"  # Direct link if the user has a username
    else:
        user_link = f"tg://user?id={user_id}"  # Fallback for users without a username

    # Feedback message from the user
    feedback_message = " ".join(context.args)
    
    if feedback_message:
        # Acknowledge the feedback
        await update.message.reply_text("Thank you for your feedback! Your input is valuable to us.")

        # Message to notify support admins
        admin_notification = (
            f"🔔 **New Feedback Submitted** 🔔\n\n"
            f"👤 **User Contact**: @{username if username else 'No username'}\n"
            f"🆔 **User ID**: {user_id}\n"
            f"🔗 **Direct Chat**: [Open Chat]({user_link})\n"
            f"📩 **Feedback**: {feedback_message}\n\n"
            f"Please follow up if needed."
        )
        
        # Notify all admins directly via DM
        for admin_id in SUPPORT_ADMINS:
            try:
                await context.bot.send_message(
                    chat_id=admin_id,
                    text=admin_notification,
                    parse_mode="Markdown",
                    disable_web_page_preview=True  # Ensures links don't expand into previews
                )
            except Exception as e:
                # Log or print error if message fails to send
                print(f"Error sending feedback to admin {admin_id}: {e}")
    else:
        # Ask user to provide feedback if none is supplied
        await update.message.reply_text(
            "Please provide feedback after the command. Example: /feedback Great bot!"
        )



# Command: /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Need help? Use:\n"
        "/bookcall - To book a call\n"
        "/feedback - To send feedback\n"
        "/support - To talk to a human support member"
    )



# Command: /support
async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.chat  # Get the user details
    username = user.username  # Username of the user
    user_id = user.id  # Telegram user ID
    user_message = update.message.text  # Get the user's message

    # Generate the direct link to the user's profile
    if username:
        user_link = f"https://t.me/{username}"  # Direct link if the user has a username
    else:
        user_link = f"tg://user?id={user_id}"  # Fallback for users without a username

    # Message to be sent to the user
    support_message = (
        "Connecting you to a support member. Please wait...\n"
        "A support member will reach out to you shortly."
    )
    await update.message.reply_text(support_message)

    # Message to be sent to the support team
    admin_notification = (
        f"🔔 **New Support Request** 🔔\n\n"
        f"👤 **User Contact**: @{username if username else 'No username'}\n"
        f"🆔 **User ID**: {user_id}\n"
        f"🔗 **Direct Chat**: [Open Chat]({user_link})\n"
        f"📩 **Message**: {user_message}\n\n"
        f"Please respond promptly."
    )

    # Notify all admins directly via DM
    for admin_id in SUPPORT_ADMINS:
        try:
            await context.bot.send_message(
                chat_id=admin_id,
                text=admin_notification,
                parse_mode="Markdown",
                disable_web_page_preview=True  # Ensures links don't expand into previews
            )
        except Exception as e:
            # Log or print error if message fails to send
            print(f"Error sending message to admin {admin_id}: {e}")


# Modified Handlers
async def handle_book_call(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await redirect_to_private(update, context, "bookcall")

async def handle_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await redirect_to_private(update, context, "feedback")

async def handle_support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await redirect_to_private(update, context, "support")

async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await redirect_to_private(update, context, "help")



# Intent detection from user messages
async def detect_intent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Convert the user's message to lowercase
    message = update.message.text.lower()
    
    # Define keywords for each intent
    intents = {
        "book_call": ["book a call", "schedule a call"],
        "feedback": ["give feedback", "feedback", "send feedback"],
        "help": ["help", "need help", "assist"],
        "support": ["talk to support", "customer service", "get support"]
    }
    
    # Check for each intent
    if any(keyword in message for keyword in intents["book_call"]):
        await book_call(update, context)
    elif any(keyword in message for keyword in intents["feedback"]):
        await feedback(update, context)
    elif any(keyword in message for keyword in intents["help"]):
        await help_command(update, context)
    elif any(keyword in message for keyword in intents["support"]):
        await support(update, context)
    

# Main function to run the bot
def main():
    TOKEN = "7225931117:AAFP4haOX6lHuTFvsElH-KhzYRNC53noF_M"  # Replace with your bot's token

    # Create the application
    application = Application.builder().token(TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("bookcall", book_call))
    application.add_handler(CommandHandler("feedback", feedback))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("support", support))

    # Add message handler for intent detection
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, detect_intent))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
