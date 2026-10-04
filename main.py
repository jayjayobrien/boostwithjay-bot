from flask import Flask
import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("FOLLOWPANNEL_API_KEY")
API_URL = "https://followpannel.com/api/v2"

app = Flask(__name__)

@app.route("/")
def home():
    return "Boost With Jay Bot Online"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 Boost With Jay\n\nUse /services to view available services."
    )

async def services(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = requests.post(
            API_URL,
            data={
                "key": API_KEY,
                "action": "services"
            },
            timeout=30
        )

        data = response.json()

        if not isinstance(data, list):
            await update.message.reply_text("API returned an unexpected response.")
            return

        msg = "📋 Available Services\n\n"

        for service in data[:10]:
            try:
                provider_price = float(service["rate"])
                sell_price = round(provider_price * 1.5, 4)

                msg += (
                    f"{service['name']}\n"
                    f"Price: {sell_price}\n\n"
                )
            except Exception:
                continue

        await update.message.reply_text(msg)

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

telegram_app = Application.builder().token(BOT_TOKEN).build()
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("services", services))
telegram_app.add_handler(CommandHandler("balance", balance))

Python
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = requests.post(
            API_URL,
            data={
                "key": API_KEY,
                "action": "balance"
            },
            timeout=30
        )

        data = response.json()

        await update.message.reply_text(
            f"💰 Provider Balance\n\n"
            f"Balance: ${data['balance']}\n"
            f"Currency: {data['currency']}"
        )

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

import threading

def run_bot():
    telegram_app.run_polling(stop_signals=None)

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
