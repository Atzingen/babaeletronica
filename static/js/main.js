function atualiza(data) {
	console.log('success',data);
	// Apaga os valores da tela (visual)
	$('#temperatura-cpu').hide().delay(300).slideDown(300);
	$('#ram_livre').hide().delay(300).slideDown(300);
	$('#texto-ram').hide().delay(300).slideDown(300);
	$('#ram_usada').hide().delay(300).slideDown(300);
	$('#sd_livre').hide().delay(300).slideDown(300);
	$('#texto-sd').hide().delay(300).slideDown(300);
	$('#sd_usado').hide().delay(300).slideDown(300);
	$('#texto-darkice').hide().delay(300).slideDown(300);
	$('#texto-icecast').hide().delay(300).slideDown(300);
	$('#texto-temp-dth22').hide().delay(300).slideDown(300);
	$('#texto-bmp108').hide().delay(300).slideDown(300);
	// Alterando os valores
	$('#temperatura-cpu-val').html(data.result.temp_cpu);
	$('#ram_livre').css("width",(100*data.result.ram_livre/data.result.ram_total).toString()+"%");
	$('#texto-ram').text("Livre: " + data.result.ram_livre/1000+ "MB" + "   |  Usada: " + data.result.ram_usada/1000 + "MB");
	$('#ram_usada').css("width",(100*data.result.ram_usada/data.result.ram_total).toString()+"%");
	$('#sd_livre').css("width",(data.result.sd_livre*100/data.result.sd_total).toString()+"%");
	$('#texto-sd').text("Livre: " + data.result.sd_livre/100000000000 + "GB" + "   |  Usada: " + data.result.sd_usado/100000000000 + "GB");
	$('#sd_usado').css("width",(data.result.sd_usado*100/data.result.sd_total).toString()+"%");
	$('#resolucao_video').selectpicker('val',data.result.resolucao_video);
	$('#resolucao_foto').selectpicker('val',data.result.resolucao_foto);
	if (Number(data.result.leds) == 1 ){
		$('#led_habilitado').prop('checked',true);
	}else{
		$('#led_desabilitado').prop('checked',true);
	}
	$('#FrameRate').selectpicker('val',data.result.FrameRate.toString());
	$('#rotacao').selectpicker('val',data.result.Rotacao);
	if (Number(data.result.flipH) == 1 ){
		$('#flipH_habilitado').prop('checked',true);
	}else{
		$('#flipH_desabilitado').prop('checked',true);
	}
	if (Number(data.result.flipV) == 1 ){
		$('#flipV_habilitado').prop('checked',true);
	}else{
		$('#flipV_desabilitado').prop('checked',true);
	}
	$('#tempo_preview').selectpicker('val',data.result.tempo_preview);
	$('#tempo_desligar').selectpicker('val',data.result.tempo_desligar);
	if ( data.result.darkice == 1){
		$('#texto-darkice').html('<span class="glyphicon glyphicon-thumbs-up" aria-hidden="true"> Ligado');
	}else{
		$('#texto-darkice').html('<span class="glyphicon glyphicon-thumbs-down" aria-hidden="true"> Desligado');
	}
	if ( data.result.icecast == 1){
		$('#texto-icecast').html('<span class="glyphicon glyphicon-thumbs-up" aria-hidden="true"> Ligado');
	}else{
		$('#texto-icecast').html('<span class="glyphicon glyphicon-thumbs-down" aria-hidden="true"> Desligado');
	}
	$('#texto-temp-dth22').html('<span class="glyphicon glyphicon-fire" aria-hidden="true">' + data.result.dth22_temp + ' | ' + data.result.dth22_umidade + '%' + '</span>');
	$('#texto-bmp108').html('<span class="glyphicon glyphicon-cloud" aria-hidden="true"></span>' + '&nbsp&nbsp' + data.result.bmp_pressao + ' Pa  ' + '<span class="glyphicon glyphicon-fire" aria-hidden="true">' + data.result.bmp_temperatura + '</span>');
}

$(function (){
	$('#Bteste').on('click', function(){
		$.ajax({
			type: 'GET',
			url: '/teste',
			success: atualiza,
			error: function(){
				alert('erro no jquery');
			}
		});
	});
});

$(function() {
	$('.selectpicker').on('change', function(){
		var valor = $(this).find("option:selected").val();
		var botaoId = $(this).attr('data-id');
		var dados = {
			id: botaoId,
			valor: valor,
		};
		//alert(valor + ' - ' + botaoId);
		$.ajax({
			type: 'POST',
			url: '/ajustes',
			data: dados,
			success: function(resposta){
				$('#resposta').html("<button type=\"button\" class=\"btn btn-success\">POST efetuado </button>");
				$('#resposta').show().hide(5000);
				atualiza(resposta);
			},
			error: function(){
				alert("erro select");
			}
		});
	});
});

$(function() {
	$('.radio-inline').on('change', function(){
		var botaoId = $(this).attr('data-id');
		var dados = {
			id: botaoId,
		};
		$.ajax({
			type: 'POST',
			url: '/ajustes',
			data: dados,
			success: function(resposta){
				$('#resposta').html("<button type=\"button\" class=\"btn btn-success\">POST efetuado </button>");
				$('#resposta').show().hide(5000);
				atualiza(resposta);
			},
			error: function(){
				alert("erro select");
			}
		});
	});
});

$(function(){
	$('.botao').on('click',function(){
		var botaoId = $(this).attr('data-id');
		var valor = 0;
		if (botaoId == 'envia-comando'){
			var	texto = $('#usr').val();
		}else{
			var texto = '';
		}
		var dados = {
			id: botaoId,
			texto: texto,
		};
		$.ajax({
			type: 'POST',
			url: '/ajustes',
			data: dados,
			success: function(resposta){
				$('#resposta').html("<button type=\"button\" class=\"btn btn-success\">POST efetuado </button>");
				$('#resposta').show().hide(5000);
				atualiza(resposta);
			},
			error: function(){
				alert("erro");
			}
		});
	});
});


$(document).ready(function(e) {
	$('.selectpicker').selectpicker();
});
