import logging
from telegram import Bot
from telegram.ext import Updater, CommandHandler
import PyPDF2
from googletrans import Translator
import os

# فعال کردن لاگ برای بررسی خطاها
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# دستور start
def start(update, context):
    update.message.reply_text("سلام! ربات روزانه شروع به کار کرد ✅")

# دستور روزانه
def daily(update, context):
    try:
        # فایل PDF باید توی ریپو آپلود شده باشه (مثلاً با اسم book.pdf)
        with open("book.pdf", "rb") as file:
            reader = PyPDF2.PdfReader(file)
            page = reader.pages[0]  # صفحه اول، میشه بعداً تغییر داد
            text = page.extract_text()

        # ترجمه متن به فارسی
        translator = Translator()
        translated = translator.translate(text, src="ar", dest="fa").text

        # ارسال متن اصلی + ترجمه
        update.message.reply_text("📖 متن اصلی (عربی):\n\n" + text[:1000])  # محدودیت تلگرام
        update.message.reply_text("🇮🇷 ترجمه فارسی:\n\n" + translated[:1000])

    except Exception as e:
        update.message.reply_text("خطا رخ داد ⚠️")
        logger.error(e)

def main():
    # گرفتن توکن از محیط (که توی Secrets ذخیره کردی)
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    bot = Bot(TOKEN)
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("daily", daily))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
