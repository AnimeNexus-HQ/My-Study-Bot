import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import google.generativeai as genai

# إعداد الـ API الخاص بجيمناي
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً بك! أنا مساعدك الدراسي. أرسل لي سؤالك وسأجيبك فوراً.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    response = model.generate_content(user_text)
    await update.message.reply_text(response.text)

if __name__ == '__main__':
    # البوت يقرأ التوكن من إعدادات السيرفر
    token = os.environ.get("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(token).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    app.run_polling()
