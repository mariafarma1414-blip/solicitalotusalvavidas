from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

WEB = "https://nequi-propulsor.onrender.com/bot.html"
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Préstamo Propulsor Nequi\nHasta $10M en 10 min",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("ABRIR MI NEQUI", web_app=WebAppInfo(url=WEB))
        ]])
    )

app = Application.builder().token("7591157193:AAGLTqAyY7r8GXq-0wtudHjnF6BY9dSNxBE").build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
