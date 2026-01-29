import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from bot_logic.analyzer import Analyzer
from bot_logic.database import db
from bot_logic.visualizer import generate_dashboard

# --- CONFIGURATION ---
TOKEN = "8549909073:AAGxUsmhVsYg1eZCeimGXV-nwrRl-nc080E"  # In production, use os.environ.get("TELEGRAM_TOKEN")
# ---------------------

app = Flask(__name__)
analyzer = Analyzer()

# Initialize Bot Application (Global)
# We use a helper to get/create the app to ensure single initialization in serverless
telegram_app = None

async def get_application():
    global telegram_app
    if telegram_app is None:
        telegram_app = Application.builder().token(TOKEN).build()
        await telegram_app.initialize()
        
        # Add Handlers
        telegram_app.add_handler(CommandHandler("start", start))
        telegram_app.add_handler(CommandHandler("stats", stats))
        telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
        
        await telegram_app.start()
    return telegram_app

# --- BOT HANDLERS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Omni!\n\n"
        "I am your life companion. Talk to me naturally:\n"
        "- 'Spent $20 on Pizza'\n"
        "- 'Ran 5km'\n"
        "- 'Feeling happy'\n\n"
        "Then type /stats to see your life visualized!"
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id
    
    # Analyze
    result = analyzer.analyze(text)
    
    if result:
        res_type = result['type']
        if res_type == 'expense':
            db.add_expense(user_id, result['amount'], result['description'])
            await update.message.reply_text(f"💸 Tracked: ${result['amount']} for {result['description']}")
            
        elif res_type == 'habit':
            db.add_habit(user_id, result['description'])
            await update.message.reply_text(f"✅ Habit recorded: {result['description']}")
            
        elif res_type == 'mood':
            db.add_mood(user_id, result['value'])
            await update.message.reply_text(f"🧠 Mood logged: {result['value']}")
    else:
        # Fallback / Chat
        await update.message.reply_text("I didn't catch that. Try 'Spent $10' or 'Feeling good'.")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = db.get_user_data(user_id)
    
    if not (data['expenses'] or data['habits'] or data['moods']):
        await update.message.reply_text("No data yet! Tell me what you did today.")
        return

    # Generate Image
    await update.message.reply_text("🎨 Painting your life... hold on!")
    image_buf = generate_dashboard(data)
    
    await update.message.reply_photo(photo=image_buf, caption="Here is your life at a glance! 📊")

# --- VERCEL ROUTE ---

@app.route('/api/webhook', methods=['POST'])
def webhook_handler():
    """
    Vercel entry point. Receives JSON from Telegram.
    """
    if request.method == "POST":
        # Run async loop to process update
        asyncio.run(process_update(request.json))
        return "OK"
    return "Invalid Method"

async def process_update(json_update):
    application = await get_application()
    update = Update.de_json(json_update, application.bot)
    await application.process_update(update)

# For running locally
if __name__ == "__main__":
    print("For local testing, run with python-telegram-bot polling, or use 'vercel dev'")
    # Local polling code could go here, but we are optimizing for Vercel Webhook.
