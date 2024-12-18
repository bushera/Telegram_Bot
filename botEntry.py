import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Replace these placeholders with your actual values
BOT_TOKEN = "7225931117:AAFP4haOX6lHuTFvsElH-KhzYRNC53noF_M"
WEBHOOK_URL = "https://hook.us2.make.com/1i7p27dunhnpint7bouo92ocm4hwsf5p"  # Replace with your Make.com webhook URL

# Function triggered when a user starts the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id

    # Send a simple welcome message
    await context.bot.send_message(chat_id=chat_id, text="👋 Welcome! I am processing your details...")

    # Trigger the Make.com webhook with user data
    try:
        payload = {
            "user_id": user.id,
            "username": user.username or "Anonymous",
            "first_name": user.first_name,
            "last_name": user.last_name or "",
            "chat_id": chat_id
        }
        # Send POST request to Make webhook
        requests.post(WEBHOOK_URL, json=payload, timeout=10)
    except Exception as e:
        print(f"Error triggering webhook: {e}")

    # Confirmation message
    await context.bot.send_message(chat_id=chat_id, text="✅ Done! You can start interacting with me now.")

# Main function to start the bot
def main():
    # Initialize the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add the /start command handler
    application.add_handler(CommandHandler("start", start))

    # Start polling for updates
    print("Bot is running and listening for /start...")
    application.run_polling()

if __name__ == "__main__":
    main()
