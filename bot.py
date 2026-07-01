from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from groq import Groq
from flask import Flask
import os
import threading

# ---------------- TOKENS ----------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

# ---------------- MESSAGES ----------------
WELCOME = """👋 Welcome to Study AI Bot!

📚 Main aapka AI Study Assistant hoon.

✍️ Ab apna question bhejiye."""
✅ Kisi bhi study question ka answer dunga.
✅ Hindi aur English dono me explain karunga.
✅ Step-by-step solution dunga.


SYSTEM = (
    "You are a helpful study assistant. Answer only educational questions. "
    "If unrelated, refuse politely. Explain in simple Hindi + English."
)

# ---------------- TELEGRAM BOT ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME)

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.message.text

    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": q}
        ]
    )

    await update.message.reply_text(resp.choices[0].message.content)

def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("🤖 Bot is running...")
    app.run_polling()

# ---------------- FLASK SERVER (RENDER FIX) ----------------
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "Bot is alive!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)

# ---------------- START BOTH ----------------
if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    run_web()