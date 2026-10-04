from flask import Flask
import os
import requests
import threading

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("FOLLOWPANNEL_API_KEY")
API_URL = "https://followpannel.com/api/v2"

app = Flask(__name__)


@app.route("/")
def home():
    return "Boost With Jay Bot Online"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        ["🚀 New Order", "💰 Add Funds"],
        ["👤 My Account", "📦 Order History"],
        ["🔍 Track Order", "🎧 Support"]
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

    await update.message.reply_text(
        "🚀 Boost With Jay\n\nChoose an option below:",
        reply_markup=reply_markup
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
            await update.message.reply_text(
                "API returned an unexpected response."
            )
            return

        msg = "📋 Available Services\n\n"

        for service in data[:10\]:
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
        await update.message.reply_text(
            f"Error: {e}"
        )


async def menu_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if text == "🚀 New Order":

        keyboard = [
            ["📘 Facebook", "📸 Instagram"],
            ["🎵 TikTok", "📨 Telegram"],
            ["▶️ YouTube", "💎 Diamond League (🚧 Soon)"],
            ["❤️ TikTok Likes + Views 🇰🇭 (🚧 Soon)", "👑 Gemini Premium (🚧 Soon)"],
            ["🎯 TikTok Likes 🇰🇭 (🚧 Soon)", "🎬 CapCut Pro (🚧 Soon)"],
            ["🎨 Canva Pro (🚧 Soon)"],
            ["❌ Cancel"]
        ]

        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )

        await update.message.reply_text(
            "🚀 Please select a service category:",
            reply_markup=reply_markup
        )

    elif text in [
        "💎 Diamond League(🚧 Soon)",
        "❤️ TikTok Likes + Views 🇰🇭 (🚧 Soon)",
        "👑 Gemini Premium (🚧 Soon)",
        "🎯 TikTok Likes 🇰🇭 (🚧 Soon)",
        "🎬 CapCut Pro (🚧 Soon)",
        "🎨 Canva Pro (🚧 Soon)"
    ]:

        await update.message.reply_text(
            "🚧 Coming Soon"
        )

    elif text == "❌ Cancel":

        keyboard = [
            ["🚀 New Order", "💰 Add Funds"],
            ["👤 My Account", "📦 Order History"],
            ["🔍 Track Order", "🎧 Support"]
        ]

        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )

        await update.message.reply_text(
            "Main Menu",
            reply_markup=reply_markup
        )

    elif text in [
        "📘 Facebook",
        "📸 Instagram",
        "🎵 TikTok",
        "📨 Telegram",
        "▶️ YouTube"
    ]:

        await update.message.reply_text(
            f"{text}\n\nCategories coming next."
        )


telegram_app = Application.builder().token(BOT_TOKEN).build()

telegram_app.add_handler(
    CommandHandler("start", start)
)

telegram_app.add_handler(
    CommandHandler("services", services)
)

telegram_app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        menu_buttons
    )
)


def run_bot():
    telegram_app.run_polling(
        stop_signals=None
    )


if __name__ == "__main__":

    threading.Thread(
        target=run_bot,
        daemon=True
    ).start()

    port = int(
        os.environ.get("PORT", 10000)
    )

    app.run(
        host="0.0.0.0",
        port=port
    )
