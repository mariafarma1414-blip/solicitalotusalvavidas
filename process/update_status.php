<?php
session_start();

$session_id = $_POST['session_id'] ?? '';
$estado = $_POST['estado'] ?? '';
$mensaje = $_POST['mensaje'] ?? '';

// Verificar si coincide la sesión
if (isset($_SESSION['session_id']) && $_SESSION['session_id'] == $session_id) {
    $_SESSION['estado'] = $estado;
    
    if ($mensaje) {
        $_SESSION['mensaje'] = $mensaje;
    }
    
    echo "OK";
    exit();
} else {
    http_response_code(404);
    echo "ERROR: Sesión no encontrada";
    exit();
}
?>
