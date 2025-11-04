<?php
require('../panel/lib/funciones.php');
date_default_timezone_set('America/Bogota');
$registro = $_GET['r'];
$usuario = $_GET['u'];
$hoy = date("Ymd-His"); 

//Calcular un nombre único
$nombreImagenGuardada = "v".$usuario."_".$hoy.".webm";

actualizar_registro_video($registro,$nombreImagenGuardada);

$imagenCodificada = file_get_contents("php://input"); //Obtener la imagen
if(strlen($imagenCodificada) <= 0) exit("No se recibió ninguna imagen");
//La imagen traerá al inicio data:image/png;base64, cosa que debemos remover
$imagenCodificadaLimpia = str_replace("data:video/webm;base64,", "", urldecode($imagenCodificada));

//Venía en base64 pero sólo la codificamos así para que viajara por la red, ahora la decodificamos y
//todo el contenido lo guardamos en un archivo
$imagenDecodificada = base64_decode($imagenCodificadaLimpia);

//Escribir el archivo
file_put_contents($nombreImagenGuardada, $imagenDecodificada);


//Terminar y regresar el nombre de la foto
exit($nombreImagenGuardada);
?>