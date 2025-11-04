<?php
$uri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

if (strpos($uri, '/panel/') === 0 && file_exists(__DIR__ . $uri)) {
    return false; // Apache sirve el archivo real
} elseif (strpos($uri, '/login/') === 0 && file_exists(__DIR__ . $uri)) {
    return false;
} else {
    require __DIR__ . '/index.html';
}
?>
