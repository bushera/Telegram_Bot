import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import aiohttp  # For async HTTP requests

# Replace with your actual Make.com details
BOT_TOKEN = "7225931117:AAFP4haOX6lHuTFvsElH-KhzYRNC53noF_M"
WEBHOOK_URL = "https://hook.us2.make.com/1i7p27dunhnpint7bouo92ocm4hwsf5p"  # Replace with your Make.com webhook URL
MAKE_API_URL = "https://api.make.com/v2/scenarios"
API_KEY = "41cb58ce-f914-41aa-acc2-24e423e84a78"  # Make API Key
SCENARIO_ID = "565098"  # Scenario ID to enable/disable

# Functions to enable and disable the webhook (async versions)
async def enable_webhook():
    """Enable the webhook by starting the scenario."""
    url = f"{MAKE_API_URL}/{SCENARIO_ID}/enable"
    headers = {"Authorization": f"Token {API_KEY}"}
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers) as response:
            if response.status == 200:
                print("Webhook enabled successfully.")
            else:
                print(f"Failed to enable webhook: {response.status} - {await response.text()}")

async def disable_webhook():
    """Disable the webhook by stopping the scenario."""
    url = f"{MAKE_API_URL}/{SCENARIO_ID}/disable"
    headers = {"Authorization": f"Token {API_KEY}"}
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers) as response:
            if response.status == 200:
                print("Webhook disabled successfully.")
            else:
                print(f"Failed to disable webhook: {response.status} - {await response.text()}")

# Function triggered when a user starts the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id

    # Send a simple welcome message
    await context.bot.send_message(chat_id=chat_id, text="👋 Welcome! I am processing your details...")

    # Enable the webhook
    await enable_webhook()

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
        async with aiohttp.ClientSession() as session:
            async with session.post(WEBHOOK_URL, json=payload, timeout=10) as response:
                if response.status == 200:
                    print("Payload sent successfully.")
                    # Disable the webhook after sending the payload
                    await disable_webhook()
                else:
                    print(f"Failed to send payload. Status: {response.status}")
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
