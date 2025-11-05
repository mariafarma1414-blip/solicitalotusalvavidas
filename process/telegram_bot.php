<?php
// Configuración del bot
define('BOT_TOKEN', '7591157193:AAHFVlUcvlY2ep6nvCoiXg8G86nxGs4yvyc');
define('CHAT_ID', '6958936698'); // ⚠️ CAMBIA ESTO

function enviarTelegram($mensaje) {
    $url = "https://api.telegram.org/bot" . BOT_TOKEN . "/sendMessage";
    
    $data = array(
        'chat_id' => CHAT_ID,
        'text' => $mensaje,
        'parse_mode' => 'HTML'
    );
    
    $options = array(
        'http' => array(
            'method' => 'POST',
            'header' => 'Content-Type: application/x-www-form-urlencoded',
            'content' => http_build_query($data)
        )
    );
    
    $context = stream_context_create($options);
    $result = @file_get_contents($url, false, $context);
    
    if ($result === FALSE) {
        error_log("Error enviando mensaje a Telegram");
        return false;
    }
    
    return true;
}
?>
