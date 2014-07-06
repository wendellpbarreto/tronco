var validado = false;

function mascaraTelefone(t, mask) {
	var i = t.value.length;
	var saida = mask.substring(1,0);
	var texto = mask.substring(i)
	if (texto.substring(0,1) != saida){
		t.value += texto.substring(0,1); 
	}
}

function validacaoTelefone(){
	field = document.getElementById("id_telefone");
	if (field.value.trim().length < 8){
		alert("Digite um telefone válido (com DDD).");
		return false;
	}else{
		return true;
	}
}

function validacaoNome() {
	field = document.getElementById("id_nome");
	if (field.value.trim().length < 2){
		alert("Digite um nome válido.");
	}
}

function validacaoTexto() {
	field = document.getElementById("id_descricao");
	if (field.value.trim().length < 2){
		alert("Digite um texto válido.");
	}

}

function validacaoEmail() {
	field = document.getElementById("id_email");
	usuario = field.value.substring(0, field.value.indexOf("@")); 
	dominio = field.value.substring(field.value.indexOf("@")+ 1, field.value.length);

	if (!((usuario.length >=1) && 
		(dominio.length >=3) && 
		(usuario.search("@")==-1) && 
		(dominio.search("@")==-1) && 
		(usuario.search(" ")==-1) && 
		(dominio.search(" ")==-1) && 
		(dominio.search(".")!=-1) && 
		(dominio.indexOf(".") >=1)&& 
		(dominio.lastIndexOf(".") < dominio.length - 1)
		)) { 
		alert("E-mail inválido! Por favor, corrija o seu e-mail.");
	}  
}

function teste(){
alert("Teste"); 
}

function validacaoFinal() {
	if(validacaoTelefone()){
		document.getElementById("send").disabled=false;
	}else{
		document.getElementById("send").disabled=true;
	}
}

