import os
import json
import fitz  # PyMuPDF برای خوندن PDF
import requests
from googletrans import Translator

# تنظیمات تلگرام
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# بارگذاری شماره صفحه
with open("progress.json", "r") as f:
    progress = json.load(f)
page_num = progress["page"]

# باز کردن PDF
pdf = fitz.open("book.pdf")
if page_num >= len(pdf):
    message = "📕 همه صفحات فرستاده شد!"
else:
    text = pdf[page_num].get_text()

    # ترجمه متن
    translator = Translator()
    translated = translator.translate(text, src="ar", dest="fa").text

    # ساخت پیام
    message = f"📄 صفحه {page_num+1}\n\nمتن اصلی:\n{text}\n\nترجمه فارسی:\n{translated}"

    # ارسال به تلگرام
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})

    # آپدیت شماره صفحه
    progress["page"] = page_num + 1
    with open("progress.json", "w") as f:
        json.dump(progress, f)

pdf.close()

# آپدیت فایل در ریپو
os.system('git config user.name "github-actions"')
os.system('git config user.email "github-actions@github.com"')
os.system('git add progress.json')
os.system('git commit -m "Update progress"')
os.system('git push')
