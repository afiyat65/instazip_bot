import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# توکن خودتو اینجا بذار
BOT_TOKEN = "7821450813:AAGFeKaWDXyUqWeZRFqwDsDaqrx__FNUwAA"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# شروع ربات
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! 👋 لینک پست یا ریلز اینستاگرام رو برام بفرست تا دانلود کنم.")

# دریافت لینک از کاربر
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if "instagram.com" not in url:
        await update.message.reply_text("⚠️ لطفاً فقط لینک اینستاگرام بفرست.")
        return

    api_url = f"https://insta-saver-api.vercel.app/api/?url={url}"
    try:
        r = requests.get(api_url).json()
        if r.get("media"):
            for item in r["media"]:
                await update.message.reply_video(item) if ".mp4" in item else await update.message.reply_photo(item)
        else:
            await update.message.reply_text("😕 نتونستم چیزی پیدا کنم. لینک شاید اشتباهه.")
    except Exception as e:
        await update.message.reply_text("❌ مشکلی پیش اومد. بعداً امتحان کن.")

# اجرای ربات
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
