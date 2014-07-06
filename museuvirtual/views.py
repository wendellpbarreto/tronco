#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponse

from museuvirtual.settings import MEDIA_ROOT

from datetime import datetime

from gerenciamento.models import *
from criacao.models import *
from apresentacao.models import *
from django.core.exceptions import ObjectDoesNotExist 

from django.test.client import Client

def preencher(request):
	
	quantidade = 30
	
		
	# Função do autor	
	funcao_autor = FuncaoAutor()
	funcao_autor.nome = "Pintor"
	try:
		funcao_autor.save()	
	except Exception:
		funcao_autor = FuncaoAutor.objects.get(nome="Pintor")
	
	# Autor	
	autor = Autor()
	autor.nome = "Pedro Bandeira de Carvalho"
	autor.funcao_autor = funcao_autor
	autor.save()

	# Objeto	
	objeto = Objeto()
	objeto.nome = "Quadro"
	try:
		objeto.save()
	except Exception:
		objeto = Objeto.objects.get(nome="Quadro")
	
	conversao_feita = False
	
	data_criacao = DataFormatada(data_especifica = datetime.now(), decada_ano = '2012', seculo = 'XXX', periodo = 'PERIODO')
	data_criacao.save()

	for i in range(1,quantidade+1,1):
		peca = Peca()
		peca.numero_registro = "MV-2013-AZ-00%d" %i
		peca.titulo = "Obra de arte número %d" %i
		peca.objeto = objeto
		peca.autor = autor
		peca.descricao = "Esta é uma obra de arte exemplo para testes do Museu Virtual."
		peca.data_criacao = data_criacao
		
		try:
			peca.save()
		except Exception:
			peca = Peca.objects.get(numero_registro="MV-2013-AZ-00%d" %i)
		
		
		# Imagens

		
		imagem1 = Imagem()
		imagem2 = Imagem()
		imagem1.peca = peca
		imagem2.peca = peca
		
		if i%2 == 0:
			imagem1.imagem = "escultura.jpg"
			imagem2.imagem = "totem.jpg"
		else:
			imagem2.imagem = "escultura.jpg"
			imagem1.imagem = "totem.jpg"
			
		imagem1.save()
		imagem2.save()
		
		#if not conversao_feita:
		#	criar_outras_imagens(Imagem,imagem1)
		#	criar_outras_imagens(Imagem,imagem2)
		#	conversao_feita = True
		
		
		# Audios
		
		audio1 = Audio()
		audio2 = Audio()
		audio1.peca = peca
		audio2.peca = peca
		
		if i%2 == 0:		
			audio1.audio = "entrevista-jorge-barreto.mp3"
			audio2.audio = "entrevista-pedro-bandeira.mp3"
		else:
			audio2.audio = "entrevista-jorge-barreto.mp3"
			audio1.audio = "entrevista-pedro-bandeira.mp3"
		
		audio1.save()
		audio2.save()
		
		
		# Vídeos
		
				
		video1 = Video()
		video2 = Video()
		video1.peca = peca
		video2.peca = peca
		if i%2 == 0:
			video1.video = "phoenix.mp4"
			video2.video = "museum-philadelphia.mp4"
		else:
			video2.video = "phoenix.mp4"
			video1.video = "museum-philadelphia.mp4"
		
		video1.save()
		video2.save()
		
		# Documentos
		
		documento1 = Documento()
		documento2 = Documento()
		documento1.peca = peca
		documento2.peca = peca
		
		if i%2 == 0:
			documento1.documento = "history.pdf"
			documento2.documento = "memory-distortion.pdf"
		else:
			documento2.documento = "history.pdf"
			documento1.documento = "memory-distortion.pdf"
		

		documento1.save()
		documento2.save()	
	
	
	for i in range(1,quantidade/2 + 1,1):
		coletanea = Coletanea()
		coletanea.nome = "Coletanea %d" %i
		coletanea.descricao = "Esta é uma coletânea de demonstração."
		coletanea.nivel = 1
		coletanea.status = True
		coletanea.save()
		for j in range(i, quantidade+1, 1):
			coletanea.pecas.add(Peca.objects.get(id=i))
			coletanea.save()
		
	# Tema
	
	tema = Tema()
	tema.nome = "Principal"
	try:
		tema.save()
	except Exception:
		tema = Tema.objects.get(nome="Principal")
	
	# Informações do Museu
	
	
	informacoes_museu = InformacoesMuseu()
	informacoes_museu.nome= "Drawing"
	informacoes_museu.data_fundacao = datetime.now()
	
	informacoes_museu.apresentacao = """
	
	Museu não é "coisa de museu" O
	riundo de um projeto de extensão, coordenado pelo Núcleo de Arte e Cultura da UFRN, 
	o Museu de Arte Abraham Palatnik se instaura a partir da pesquisa e catalogação do 
	acervo de arte multimídia do artista Jota Medeiros e do acervo de Artes Visuais da UFRN.
	
	Constitui-se em uma ambiência virtual que se inscreve como deflagradora de ações de ensino, 
	pesquisa e extensão. O Museu de Arte Abraham Palatnik homenageia o artista norte-riograndense 
	que se projetou internacionalmente, a partir da 1ª Bienal de São Paulo (1951), com seu trabalho 
	artístico associado à ciência e à tecnologia.
	
	"""
	
	informacoes_museu.concepcao = 	"""
	O Museu de Arte Abraham Palatnik conta com o acervo de artes visuais da Universidade Federal do Rio Grande do Norte e com o acervo de arte multimídia pertencente ao artista visual Jota Medeiros, abrangendo as mais diversas modalidades da arte contemporânea, como arte correio que conta com mais de 500 trabalhos já catalogados; poesia visual; xerografia; video arte entre outros.

	Funciona de forma interativa, proporcionando o acesso a consultas e/ou pesquisas sobre arte multimídia em geral.
	
	A idéia do Museu foi apresentada a Direção do Núcleo de Arte e Cultura da UFRN no ano de 2005, sendo aprovado como Projeto Permanente do NAC.
	
	Em outubro de 2011, o Museu de Arte Abraham Palatnik foi apresentado a comunidade universitária durante a XVII CIENTEC pela Reitora da UFRN.
	"""
	
	informacoes_museu.missao = """
	O Museu de Arte Abraham Palatnik tem como missão fomentar atividades por meio de novas intervenções e investigações experimentais nas mais diversas áreas do conhecimento.
	"""
	
	informacoes_museu.objetivos = """
	Documentar, preservar e divulgar os acervos de Artes Visuais da UFRN e Multimídia "Jota Medeiros", proporcionando o acesso as mais variadas linguagens da contemporaneidade, atendendo aos seus objetivos pedagógicos e de ação cultural junto aos cursos de graduação e pós-graduação como possibilidades de articulação entre o ensino, a pesquisa e a extensão.
	"""
	
	informacoes_museu.descricao_tecnica = """
	O Acervo de Artes Visuais da Universidade Federal do Rio Grande do Norte, começou a se formar na década de 1960, com obras dos artistas Leopoldo Nelson e Manxa.

	Nas décadas seguintes, este Acervo foi ampliado a partir de aquisições e doações voluntárias de artistas brasileiros e estrangeiros, de nomes como Dorian Gray, Thomé Filgueira, Raul Córdula Filho, Zaira Caldas, Flávio Tavares, Jota Medeiros, Flávio Freitas, Socorro Evangelista, Akbar Behkalam, Trak Wendisch, Ítalo Trindade, Isaias Ribeiro, Marlene Almeida, Maurício Castro, Dieter Ruckaberle, Picasso, entre outros, totalizando aproximadamente 300 obras catalogadas.
	"""
	
	informacoes_museu.caracteristicas_acervo = """
	O Museu do Futebol não é um museu de coleções, mas de experiências. Seu acervo tem como principal característica a imaterialidade, ou seja, baseia-se nas representações das memórias e dos acontecimentos que marcaram a história do futebol brasileiro.
	Uma das formas de narrar esses acontecimentos é a partir de vídeos, fotos e experiências sensoriais. A exposição de longa duração do Museu do Futebol conta com mais de 1.500 imagens fotográficas e 5 horas de vídeos.
	Além disso, o Museu do Futebol vem trabalhando no mapeamento e catalogação de práticas e coleções. Essa pesquisa integrará um inventário digital de referências sobre futebol.
	Em breve, todo o acervo estará disponível para consulta pela internet, por meio do CRFB .
	Informamos que parte do material exposto não é de propriedade do Museu, mas, licenciados de outras instituições. Por esse motivo, o Museu do Futebol não cede quaisquer imagens pertencentes a terceiros que estão presentes em seu acervo expositivo.
	"""
	
	informacoes_museu.tema = tema

	informacoes_museu.save()
	

	
	return HttpResponse("Preenchimento realizado com sucesso! :)")
	# titulo, objeto, [imagem1, imagem2, imagem3], [videp]
	