import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from telegram import ChatPermissions
import json


# Your webhook URL
WEBHOOK_URL = "https://hook.us2.make.com/7vhbgvnaseruqs9uuf244yfkqqgx9vuq"

# Function to call the webhook when a new user joins
async def user_joined(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get the new user's ID and username
    user = update.message.new_chat_members[0]
    user_id = user.id
    username = user.username
    first_name = user.first_name
    last_name = user.last_name if user.last_name else ""
    full_name = f"{first_name} {last_name}"
    language_code = user.language_code
    is_bot = user.is_bot
    bio = user.bio if hasattr(user, 'bio') else "No bio available"
    
    
    # Create the payload to send to the webhook
    payload = {
        "user_id": user_id,
        "username": username,
        "first_name": first_name,
        "last_name": last_name,
        "full_name": full_name,
        "chat_id": update.message.chat.id,
        "language_code": language_code,
        "is_bot": is_bot,
        "bio": bio
       
    }

    # Send a POST request to the webhook URL
    response = requests.post(WEBHOOK_URL, json=payload)

    if response.status_code == 200:
        print("Webhook triggered successfully")
    else:
        print(f"Failed to trigger webhook. Status code: {response.status_code}")

# Main function to run the bot
def main():
    TOKEN = "7669480378:AAHu1Q3mW-RqifFbOIuG1cxZpFvkK9EROMs"  # Replace with your bot's token

    # Create the application
    application = Application.builder().token(TOKEN).build()

    # Add handler for new users joining
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, user_joined))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
