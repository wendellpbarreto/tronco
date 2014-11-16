
/* Functions
 *************************************************************************/

	function lock_screen(){
		$('#page-loading').fadeTo(1, 0.5)
	}

	function unlock_screen(){
		$('#page-loading').fadeOut(500);
	}

	function placeholder(element, value){
		element.val(value);

		element.focus(function(){
			if (this.value == value){
				this.value = '';
			}
		});

		element.blur(function(){
			if (this.value == '') {
				this.value = value;
			}
		})
	}


/* Functions calls
 // *************************************************************************/
	// placeholder($('.new_collectanea_form #id_nome'), 'Nome da Coletânea*');
	// placeholder($('.new_collectanea_form #id_descricao'), 'Descrição*');
	// placeholder($('.new_collectanea_form #id_inicio_exposicao'), 'Data do ínicio da exposição*');
	// placeholder($('.new_collectanea_form #id_fim_exposicao'), 'Data do fim da exposição*');

	
/* Global calls
 *************************************************************************/
 
$(document).on('click', 'a[data-get]', function(e){
	e.preventDefault();

	var el = $(this);
	var href = el.attr('data-get');
	var confirmed = true;

	if(el.attr('data-confirm')){
		alertify.confirm(el.attr('data-confirm'), function (e) {
		    if (e) {
		    	$.get(href, function(data){
		    		if(el.attr('data-target')){
		    			$(el.attr('data-target')).html(data['template']);
		    		}
		    	});

				if(el.attr('data-remove')){
					$(el.attr('data-remove')).fadeOut(1000, function(){ 
			        	$(this).remove();
			      	})
				}

				if(el.attr('data-success')){
					alertify.success(el.attr('data-success'));
				}

		    } else {
		    	confirmed = false;
		    }
		});
	} else {
    	$.get(href, function(data){

    		if(el.attr('data-target')){
    			$(el.attr('data-target')).html(data['template']);
    		}

    		
    	}).complete(function(){
    		if(el.attr('data-callback')){
    			callback = el.attr('data-callback');

    			if (callback == 'atualizar_listagem_de_pecas'){
    				atualizar_listagem_de_pecas();
    			}
    		}
    	})

		if(el.attr('data-remove')){
			$(el.attr('data-remove')).fadeOut(1000, function(){ 
	        	$(this).remove();
	      	})
		}
	}
});

$(document).on('click', 'a[data-post]', function(e){
	e.preventDefault();
	lock_screen();

	var el = $(this);

	if (!el.hasClass("inactive")){
		el.addClass('inactive');		

		var form = $(el.attr('data-post'));
		var href = form.attr('action');

		$.post(href, form.serialize(), function(data){
			if (data['alert-success']){
				alertify.success(data['alert-success']);
			}

			if(data['alert-error']){
				alertify.error(data['alert-error']);
			}

			if (data['redirect']){
				setTimeout(function () {
				   window.location.replace(data['redirect']);
				}, 1000);
			} else{
				el.removeClass('inactive');		
			}	
		}).complete(function(data){
			//unlock_screen();
		});
	} else{
		alertify.error('Espere um pouco, estamos processando sua solicitação.');
	}
})

$(document).on('click', 'a[data-help]', function(e){
	$(document).foundation('joyride', 'start');
})

/* PECA CALLS */
$(document).on('click', 'a.peca', function(e){
	var el = $(this);
	var id = el.attr('data-peca');

	if (el.hasClass('selected')){
		el.removeClass('selected');

		input = $('#new_collectanea_form').find('input[value='+ id +']').remove();
	} else {
		el.addClass('selected');
		
		$('#new_collectanea_form').append("<input class='elemento_peca' type='hidden' name='lista_de_pecas[]' value='" + id + "' >");
	}
});
function atualizar_listagem_de_pecas(){

	$('#new_collectanea_form input.elemento_peca').each(function(index){
		var input = $(this);

		$('#listagem-de-pecas a.peca').each(function(index2){
			var a = $(this);
			if (input.val() == a.attr('data-peca')){
				if (!a.hasClass('selected')){
					a.addClass('selected');
				}
			}
		});
	});
}



$(document).ready(function() {

	/* begin of entrar.html */
	$('#login').submit(function() {
		var resp = false;
		var username = $("#username").val();
		var password = $("#password").val();

		if (username == "" && password == "") {		
			$("span.error").text("Por favor, digite um nome de usuário e senha.").show().fadeOut(800).fadeIn(1000).fadeOut(800);
			$("#username").focus();
		} else if(username == ""){
			$("span.error").text("Por favor, digite um nome de usuário.").show().fadeOut(800).fadeIn(1000).fadeOut(800);
			$("#username").focus();
		} else if(password == ""){
			$("span.error").text("Por favor, digite uma senha.").show().fadeOut(800).fadeIn(1000).fadeOut(800);
			$("#password").focus();
		} else {
			resp = true;
		}
		
		return resp;
	});
	/* end of entrar.html */



	/* smooth scroll */
	function goToByScroll(id){
	    id = id.replace("link_", "");
	    $('html,body').animate({
	        scrollTop: $("#"+id).offset().top},'slow');
	}

	$("#link_contact").click(function(e) { 
	    e.preventDefault(); 
	    goToByScroll($(this).attr("id"));           
	});

	/* selection form focus/blur */
	
});


function salve_coletanea(){
	if ($('#id_nome').val() == 'Nome da Coletânea*' ||
		$('#id_nome').val() == ''){

		$("#id_nome").animate({"opacity" : 1}, 500, function(){  $("#id_nome").addClass("invalid"); })
					 .animate({"opacity" : 1}, 500, function(){  $("#id_nome").removeClass("invalid"); })
					 .animate({"opacity" : 1}, 500, function(){  $("#id_nome").addClass("invalid"); })
					 .animate({"opacity" : 1}, 500, function(){  $("#id_nome").removeClass("invalid"); $("#id_nome").focus(); });
		
	} else if ($('#id_descricao').val() == 'Descrição*' ||
		$('#id_descricao').val() == ''){

		$("#id_descricao").animate({"opacity" : 1}, 500, function(){  $("#id_descricao").addClass("invalid"); })
						  .animate({"opacity" : 1}, 500, function(){  $("#id_descricao").removeClass("invalid"); })
						  .animate({"opacity" : 1}, 500, function(){  $("#id_descricao").addClass("invalid"); })
						  .animate({"opacity" : 1}, 500, function(){  $("#id_descricao").removeClass("invalid"); $("#id_descricao").focus(); });
	} else {

		var resp = confirm("Pressione OK para confirmar a criação.");
		
		if (resp == true) {
			var multipleValues = $("#multiple").val() || [];

			Dajaxice.criacao.salvar_nova_coletanea(Dajax.process,{'nome':$('#id_nome').val(), 'descricao':$('#id_descricao').val(), 'pecas':multipleValues});
		}
	}
}

function salve_coletanea_editada(id, nivel){
	if ($('#id_nome').val() == ''){

		$("#id_nome").animate({"opacity" : 1}, 500, function(){  $("#id_nome").addClass("invalid"); })
					 .animate({"opacity" : 1}, 500, function(){  $("#id_nome").removeClass("invalid"); })
					 .animate({"opacity" : 1}, 500, function(){  $("#id_nome").addClass("invalid"); })
					 .animate({"opacity" : 1}, 500, function(){  $("#id_nome").removeClass("invalid"); $("#id_nome").focus(); });
		
	} else if ($('#id_descricao').val() == ''){

		$("#id_descricao").animate({"opacity" : 1}, 500, function(){  $("#id_descricao").addClass("invalid"); })
						  .animate({"opacity" : 1}, 500, function(){  $("#id_descricao").removeClass("invalid"); })
						  .animate({"opacity" : 1}, 500, function(){  $("#id_descricao").addClass("invalid"); })
						  .animate({"opacity" : 1}, 500, function(){  $("#id_descricao").removeClass("invalid"); $("#id_descricao").focus(); });
	} else {
		var resp = confirm("Pressione OK para confirmar a edição da coletânea ou cancele se não tiver certeza.");
	
		if (resp == true) {
			var multipleValues = $("#multiple").val() || [];

			Dajaxice.criacao.salvar_coletanea_editada(Dajax.process,{'id':id, 'nivel':nivel, 'nome':$('#id_nome').val(), 'descricao':$('#id_descricao').val(), 'pecas':multipleValues});
		
		} 
	}
}

function delete_coletanea(id){
	var resp = confirm("Pressione OK para confirmar a exclusão da coletânea ou cancele se não tiver certeza.");
	
	if (resp == true) {
		Dajaxice.criacao.deletar_coletanea(Dajax.process, {'id':id});	
	} 
}

function salve_noticia(){
	if ($('#id_titulo').val() == ''){
		$("#id_titulo").animate({"opacity" : 1}, 500, function(){  $("#id_titulo").addClass("invalid"); })
					 .animate({"opacity" : 1}, 500, function(){  $("#id_titulo").removeClass("invalid"); })
					 .animate({"opacity" : 1}, 500, function(){  $("#id_titulo").addClass("invalid"); })
					 .animate({"opacity" : 1}, 500, function(){  $("#id_titulo").removeClass("invalid"); $("#id_titulo").focus(); });
		
	} else if ($('#id_descricao_breve').val() == ''){

		$("#id_descricao_breve").animate({"opacity" : 1}, 500, function(){  $("#id_descricao_breve").addClass("invalid"); })
						  .animate({"opacity" : 1}, 500, function(){  $("#id_descricao_breve").removeClass("invalid"); })
						  .animate({"opacity" : 1}, 500, function(){  $("#id_descricao_breve").addClass("invalid"); })
						  .animate({"opacity" : 1}, 500, function(){  $("#id_descricao_breve").removeClass("invalid"); $("#id_descricao_breve").focus(); });
	} else if ($('#id_descricao').val() == ''){

		$("#id_descricao").animate({"opacity" : 1}, 500, function(){  $("#id_descricao").addClass("invalid"); })
						  .animate({"opacity" : 1}, 500, function(){  $("#id_descricao").removeClass("invalid"); })
						  .animate({"opacity" : 1}, 500, function(){  $("#id_descricao").addClass("invalid"); })
						  .animate({"opacity" : 1}, 500, function(){  $("#id_descricao").removeClass("invalid"); $("#id_descricao").focus(); });
	} else {
		var resp = confirm("Pressione OK para confirmar a criação.");
		
		if (resp == true) {
			var multipleValues = $("#multiple").val() || [];

			Dajaxice.criacao.salvar_nova_noticia(Dajax.process,{'titulo':$('#id_titulo').val(), 'descricao_breve':$('#id_descricao_breve').val(), 'descricao':$('#id_descricao').val(), 'pecas':multipleValues});
		}
	}
}

function salve_noticia_editada(id){
	if ($('#id_titulo').val() == ''){

		$("#id_titulo").animate({"opacity" : 1}, 500, function(){  $("#id_titulo").addClass("invalid"); })
					 .animate({"opacity" : 1}, 500, function(){  $("#id_titulo").removeClass("invalid"); })
					 .animate({"opacity" : 1}, 500, function(){  $("#id_titulo").addClass("invalid"); })
					 .animate({"opacity" : 1}, 500, function(){  $("#id_titulo").removeClass("invalid"); $("#id_titulo").focus(); });
		
	} else if ($('#id_descricao_breve').val() == ''){

		$("#id_descricao_breve").animate({"opacity" : 1}, 500, function(){  $("#id_descricao_breve").addClass("invalid"); })
						  .animate({"opacity" : 1}, 500, function(){  $("#id_descricao_breve").removeClass("invalid"); })
						  .animate({"opacity" : 1}, 500, function(){  $("#id_descricao_breve").addClass("invalid"); })
						  .animate({"opacity" : 1}, 500, function(){  $("#id_descricao_breve").removeClass("invalid"); $("#id_descricao_breve").focus(); });
	} else {
		var resp = confirm("Pressione OK para confirmar a edição da notícia ou cancele se não tiver certeza.");
	
		if (resp == true) {
			var multipleValues = $("#multiple").val() || [];

			Dajaxice.criacao.salvar_noticia_editada(Dajax.process,{'id':id, 'titulo':$('#id_titulo').val(), 'descricao_breve':$('#id_descricao_breve').val(), 'descricao':$('#id_descricao').val(), 'pecas':multipleValues});
		
		} 
	}
}


