import asyncio
from telegram import Bot

# --- CONFIGURATION ---
TOKEN = "8549909073:AAGxUsmhVsYg1eZCeimGXV-nwrRl-nc080E"
# ---------------------

async def set_hook():
    print("--- Omni Bot Webhook Setup ---")
    vercel_url = input("Enter your Vercel Deployment URL (e.g., https://my-bot.vercel.app): ").strip()
    
    if not vercel_url.startswith("http"):
        print("Error: URL must start with https://")
        return

    # Ensure URL ends with /api/webhook
    webhook_url = f"{vercel_url.rstrip('/')}/api/webhook"
    
    bot = Bot(TOKEN)
    print(f"Setting webhook to: {webhook_url}...")
    
    await bot.set_webhook(webhook_url)
    print("✅ Webhook set successfully! Your bot is live.")
    
    info = await bot.get_webhook_info()
    print(f"Current Webhook Info: {info}")

if __name__ == "__main__":
    try:
        asyncio.run(set_hook())
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure 'python-telegram-bot' is installed.")
