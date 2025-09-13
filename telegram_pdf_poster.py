# telegram_pdf_poster.py
import os
from datetime import datetime, date
from telegram import Bot
from PyPDF2 import PdfReader
from deep_translator import GoogleTranslator

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
PDF_PATH = os.getenv("PDF_PATH", "book.pdf")
START_DATE = os.getenv("START_DATE")
LANG_SRC = os.getenv("LANG_SRC", "ar")
LANG_DST = os.getenv("LANG_DST", "fa")

bot = Bot(token=BOT_TOKEN)

def read_page_text(pdf_path, page_index):
    reader = PdfReader(pdf_path)
    if page_index < 0 or page_index >= len(reader.pages):
        return None
    page = reader.pages[page_index]
    text = page.extract_text()
    return text or ""

def compute_page_index(start_date_str):
    if not start_date_str:
        return 0
    start = datetime.fromisoformat(start_date_str).date()
    today = date.today()
    delta = today - start
    return delta.days

def translate_text(text, src="ar", dst="fa"):
    try:
        translated = GoogleTranslator(source=src, target=dst).translate(text)
        return translated
    except Exception as e:
        return f"[❌ ترجمه ناموفق: {e}]"

def main():
    page_idx = compute_page_index(START_DATE)
    text_ar = read_page_text(PDF_PATH, page_idx)
    if text_ar is None:
        bot.send_message(chat_id=CHAT_ID, text="✅ همه صفحات PDF ارسال شد.")
        return

    text_fa = translate_text(text_ar, src=LANG_SRC, dst=LANG_DST)

    message = f"📚 صفحه {page_idx+1}\n\n📖 متن عربی:\n{text_ar}\n\n🇮🇷 ترجمه فارسی:\n{text_fa}"

    bot.send_message(chat_id=CHAT_ID, text=message)

if __name__ == "__main__":
    main()
