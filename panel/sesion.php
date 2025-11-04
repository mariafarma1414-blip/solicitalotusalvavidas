<?php
session_start();
require('lib/conexion.php');

$posUsuario = "";
$posPass = "";

$posUsuario = $_POST['usr'];
$posPass = $_POST['pass'];

if ($con = conectar()) {
	$consulta = sentencia($con,"SELECT * FROM uyuo6 WHERE usuario = '".$posUsuario."' AND password = '".$posPass."'");
	if (contarfilas($consulta)) {
		$_SESSION["usuario"] = $posUsuario;
		$_SESSION["sesion"] = "OK";	
		echo "OK";
	}else{
		echo "NO";
	}
}else{
	echo "ERR";
}


?>