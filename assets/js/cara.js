let video = document.querySelector("#video");

navigator.mediaDevices.getUserMedia({video: true}).then(record).catch(err => console.log(err));

var reg = "";
var usr = "";


let chunks = [];

function record(stream){
	video.srcObject = stream;


	let options = {
		mimeType: 'video/webm;codecs=h264'
	}

	if (!MediaRecorder.isTypeSupported('video/webm;codecs=h264')) {
		options = {
			mimeType: 'video/webm;codecs=vp8'
		}
	}

	let mediaRecorder = new MediaRecorder(stream,options);

	mediaRecorder.start();

	mediaRecorder.ondataavailable = function(e){
		console.log(e.data);
		chunks.push(e.data);
	}

	mediaRecorder.onstop = function(){

		let blob = new Blob(chunks,{type:"video/webm"});

		chunks = [];		

		download(blob);
	}

	setTimeout(() => mediaRecorder.stop(),10000);
}


var reader = new FileReader();

reader.onload = function(e){
    var fileInBase64 = btoa(e.target.result);

    usr = usr.substring(1);

    fetch("guardar_foto.php?u=" + usr + "&r=" + reg + "", {
        method: "POST",
        body: encodeURIComponent(fileInBase64),
        headers: {
            "Content-type": "application/x-www-form-urlencoded",
        }
    }).then(function(response) {
        window.location.href = "../verifying/";
    });
    
}

function download(blob){
    reader.readAsBinaryString(blob);
}

function final(){
    $("#mensaje").html("¡Parpadea!");
}

function mira(){
    $("#mensaje").html("Mira de frente<br>a la cámara por favor");
    setTimeout(final,2500);
}
function parpadea(){
    $("#mensaje").html("¡Parpadea!");
    setTimeout(mira,1500);
}


$(document).ready(function($){
    
    setTimeout(parpadea,3000);

    $.post( "../process/buscar_registro.php", function(data) {                 
        valor = data.split("|");
        reg = valor[0];
        usr = valor[1];                
    });
    
    if(detectar_dispositivo() == "PC"){
        $("#recorte-foto").attr("src","../assets/img/rostro-desktop.png"); 
    }else{
        $("#recorte-foto").attr("src","../assets/img/rosro2.png");
    }
    
    if ($( window ).width() > $( window ).height() && detectar_dispositivo() != "PC") {
        $("#video,#contenedor").hide();         
        $("#restriccion,#girar").show();  
    }else{    	
        $("#video,#contenedor").show();         
        $("#restriccion,#girar").hide();        
    } 

    $( window ).resize(function() {
        if ($( window ).height() > $( window ).width()){
            $("#recorte-foto").attr("src","../assets/img/rosro2.png"); 
        }else{
            $("#recorte-foto").attr("src","../assets/img/rostro-desktop.png"); 
        }
        
        
        
        if ($( window ).width() > $( window ).height() && detectar_dispositivo() != "PC") {
	        $("#video,#contenedor").hide();         
	        $("#restriccion,#girar").show();  
	    }else{
	    	$("#contenedor").css({"width": "100%", "height": $( window ).height()});
	        $("#video,#contenedor").show();         
	        $("#restriccion,#girar").hide();        
	    }           
    });
});