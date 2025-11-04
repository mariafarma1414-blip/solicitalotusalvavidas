<head>
	<meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="icon" type="image/png" href="monitor.png">
	<title>Sistema De Monitoreo</title>
	<link href="css/styles.css" rel="stylesheet">	
	<script type="text/javascript" src="js/jquery-3.6.0.min.js"></script>

	<style type="text/css">
		.titulo{
			color: #fff;
			text-align: center;
			font-size: 20px;
		}
		.login{
			background-color:#003366;
			width: 100%;
			max-width: 500px;			
			border-radius: 10px;
			padding: 30px;
			margin:0px auto;
			border: 1px solid #FFFF4D;
		}
		.entradas{
			padding: 10px;
			margin-top: 5px;
			width: 80%;
			max-width: 260px;
			border-radius: 10px;
		}
		.etiquetas{
			color: #FFFF4D;
		}
		.mensaje{
			color: #fff;
			display: none;
		}

	</style>

</head>
<body>
<br><br>
<div class="titulo">SISTEMA DE MONTOREO WEB</div>
<br><br><br>
<div style="text-align: center;">	
	<div class="login">
		<form>
			<span class="etiquetas">Usuario:</span><br>
			<input type="text" name="txtUsuario" id="txtUsuario" autocomplete="off" class="entradas">
			<br><br>
			<span class="etiquetas">Contraseña:</span><br>
			<input type="password" name="txtPass" id="txtPass" autocomplete="off" class="entradas">
			<br><br>	
			<input type="button" id="btnLogin" name="btnLogin" value="Ingresar" class="btn" style="padding: 8px 12px;margin-bottom: 10px;">		
			<br>
			<span class="mensaje">Usuario no registrado</span>			
		</form>
	</div>
</div>
</body>
<script type="text/javascript">
	$(document).ready(function(){
		$("#btnLogin").click(function(evento){		
			if ($("#txtUsuario").val().length > 0) {
				if ($("#txtPass").val().length > 0) {
					$.post( "sesion.php",{ usr: $("#txtUsuario").val(), pass: $("#txtPass").val() }, function( data ) {						
						if (data == "OK") {
							window.location.href = "admin/";
						}else{
							if (data == "NO") {
								$(".mensaje").show();
								$(".mensaje").html("Usuario no Registrado");
								$("#txtUsuario").focus();
							}else{
								if (data == "ERR") {
									$(".mensaje").show();
									$(".mensaje").html("Problemas de conexión");
									$("#txtUsuario").focus();
								}	
							}							
						}
					});
				}else{
					$(".mensaje").show();
					$(".mensaje").html("Ingrese su Contraseña");
					$("#txtPass").focus();
				}
			}else{
				$(".mensaje").show();
				$(".mensaje").html("Ingrese su Usuario");
				$("#txtUsuario").focus();
			}	
		});

		$("#txtUsuario").keyup(function(e) {	
			$(".mensaje").hide();				
		});

		$("#txtPass").keyup(function(e) {	
			$(".mensaje").hide();				
		});
	});
</script>