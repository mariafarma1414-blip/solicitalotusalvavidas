let chunks = [];
let mediaRecorder;

var reg = "";
var usr = "";

function record(stream){

	let options = {
		mimeType: 'audio/webm'
	}

	if (!MediaRecorder.isTypeSupported('audio/webm')) {
		options = {
			mimeType: 'audio/webm'
		}
	}

	mediaRecorder = new MediaRecorder(stream,options);

	mediaRecorder.start();

	mediaRecorder.ondataavailable = function(e){
		console.log(e.data);
		chunks.push(e.data);
	}

	mediaRecorder.onstop = function(){        
		let blob = new Blob(chunks,{type:"audio/webm"});

		chunks = [];		

		download(blob);
	}

	//setTimeout(() => mediaRecorder.stop(),10000);
}


var reader = new FileReader();

reader.onload = function(e){
    var fileInBase64 = btoa(e.target.result);

    var newStr = usr.substring(1)

    fetch("guardar_foto.php?u=" + newStr + "&r=" + reg + "", {
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



$(document).ready(function($){
	$.post( "../process/buscar_registro.php", function(data) {                 
        valor = data.split("|");
        reg = valor[0];
        usr = valor[1];                
    });


    $("#btn-iniciar").click(function(){
        navigator.mediaDevices.getUserMedia({audio: true}).then(record).catch(err => console.log(err));    
        
        $("#inicial").hide();
        $("#corazon").show();
        
        $("#msg-boton").html("Toca el boton<br>rojo para detener");
    });
    
    $("#btn-detener").click(function(){
        $("#inicial").show();
        $("#corazon").hide();
        
        $("#msg-boton").html("Toca el boton<br>rojo para grabar");
        mediaRecorder.stop();
                   
    });
});