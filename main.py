from flask import Flask
import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("FOLLOWPANNEL_API_KEY")
API_URL = "https://followpannel.com/api/v2"

@app.route("/")
def home():
    return "Boost With Jay Bot Online"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 Boost With Jay\n\nUse /services to view available services."
    )

async def services(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = requests.post(API_URL, data={
            "key": API_KEY,
            "action": "services"
        })

        services = response.json()

        if not services:
            await update.message.reply_text("No services found.")
            return

        msg = "📋 Services (50% markup applied)\n\n"

        for service in services[:10\]:
            try:
                provider_price = float(service["rate"])
                sell_price = round(provider_price * 1.5, 4)

                msg += (
                    f"{service['name']}\n"
                    f"Price: {sell_price}\n\n"
                )
            except:
                pass

        await update.message.reply_text(msg)

    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

telegram_app = Application.builder().token(BOT_TOKEN).build()
telegram_app.add_handler(ommandHandler("start", start))
telegram_app.add_handler(CommandHandler("services", services))

if __name__ == "__main__":
    telegram_app.run_polling()
