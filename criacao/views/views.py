#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.template.loader import render_to_string
from django.views.generic import View

#
# Dumps and loads JSON
#

def render_to_json(request, template, context_data):
	response = {}

	try:
		return context_data['file']
	except:
		pass

	try:
		response['template'] = render_to_string(template, context_data['template'], context_instance=RequestContext(request))
	except:
		pass

	try:
		for key, value in context_data['leftover'].items():
			response[key] = value
	except:
		pass

	return HttpResponse(json.dumps(response), mimetype='application/json')

def load_json(request):

	return json.loads(request)

#
# Generic View
#

class GenericView(View):
	def post(self, request, *args, **kwargs):

		if request.is_ajax():

			return render_to_json(request, self.get_template_name(request), self.get_context_data(request))
		else:
			context_data = self.get_context_data(request)

			try:
				template_data = context_data['template']
			except:
				template_data = None

			try:
				return context_data['file']
			except:
				return render_to_response(self.get_template_name(request), template_data, context_instance=RequestContext(request))

	def get(self, request, *args, **kwargs):

		if request.is_ajax():

			return render_to_json(request, self.get_template_name(request), self.get_context_data(request))
		else:
			context_data = self.get_context_data(request)

			try:
				template_data = context_data['template']
			except:
				template_data = None

			try:
				return context_data['file']
			except:
				return render_to_response(self.get_template_name(request), template_data, context_instance=RequestContext(request))

	def get_template_name(self, request):
		self.debug_request(request)

		page_name = request.resolver_match.url_name

		if request.is_ajax():

			path = 'criacao/' + page_name + '/ajax/'
		else:
			path = 'criacao/' + page_name + '/'

		try:
			slug = str(self.kwargs['slug'])

			path = path + slug + '.html'

			try:
				template = loader.get_template(path)

				return path
			except:
				return 'criacao/404.html'
		except:
			return 'criacao/404.html'

	def debug_request(self, request):
		try:
			print "SLUG: " + str(self.kwargs['slug'])
		except:
			pass

		try:
			print "KEY: " + str(self.kwargs['key'])
		except:
			pass

		if request.method == 'GET':
			print '>> request.GET'

		if request.method == 'POST':
			print '>> request.POST'

		if request.FILES:
			print '>> request.FILES'

#
# Default pages
#

def entrar(request):
	museu, museu_nome = UTIL_informacoes_museu()

	if request.user.is_authenticated():

		return render_to_response('criacao/inicio.html', locals(), context_instance=RequestContext(request))
	elif request.method == 'POST':
		return UTIL_autenticar(request)
	else:

		return render_to_response('criacao/entrar.html', locals(), context_instance=RequestContext(request))

def entrar_excecao(request, erro):
	museu, museu_nome = UTIL_informacoes_museu()

	return render_to_response('criacao/entrar.html', locals(), context_instance=RequestContext(request))


def sair(request):
	logout(request)

	return HttpResponseRedirect('/criacao/')

@login_required
def inicio(request):
	museu, museu_nome = UTIL_informacoes_museu()

	return render_to_response('criacao/inicio.html', locals(), context_instance=RequestContext(request))



from criacao.forms import *
from criacao.models import *
from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models.query import EmptyQuerySet
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from gerenciamento.models import Peca, Autor, Funcionario, Imagem, Video, Audio
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout







# Visualização de notícias e CRUD
@login_required
def noticias(request):
	app_nome = request.resolver_match.app_name
	pagina_nome = request.resolver_match.url_name

	museu, museu_nome = UTIL_informacoes_museu()

	noticias = UTIL_buscar_noticias()

	return render_to_response(app_nome + '/pagina.html', locals(),context_instance=RequestContext(request))

@login_required
def ver_noticia(request, id_noticia):
	app_nome = request.resolver_match.app_name
	pagina_nome = request.resolver_match.url_name

	museu, museu_nome = UTIL_informacoes_museu()

	noticia = Noticia.objects.get(id=id_noticia)
	pecas = noticia.pecas.all()

	for peca in pecas:
		peca.imagem = Imagem.objects.filter(peca=peca)[0].imagem

	noticia.lista_pecas = pecas

	return render_to_response(app_nome + '/pagina.html', locals(), context_instance=RequestContext(request))


# #						  #
# # Funções úteis/auxiliares #
# #						  #



def UTIL_informacoes_museu():
	try:
		museu = InformacoesMuseu.objects.get(id=1)
	except ObjectDoesNotExist:
		museu = None

	if museu:
		museu_nome = museu.nome
	else:
		museu_nome = 'Virtual'

	return (museu, museu_nome)

def UTIL_autenticar(request):
	usuario = None
	senha = None

	if request.method == 'POST':
		if 'usuario' in request.POST and request.POST['usuario']:
			usuario = request.POST['usuario']
		if 'senha' in request.POST and request.POST['senha']:
			senha = request.POST['senha']

		if usuario != None and senha != None:
			usuario_autenticado = authenticate(username=usuario, password=senha)
			if usuario_autenticado is not None:
				if usuario_autenticado.is_active:
					login(request, usuario_autenticado)
					return inicio(request)
				else:
					return entrar_excecao(request, 001)
			else:
				return entrar_excecao(request, 002)
		else:
			return entrar_excecao(request, 003)
	else:
		return entrar_excecao(request, 405)

def UTIL_buscar_coletaneas():
	try:
		coletanea_principal = Coletanea.objects.filter(nivel = 0)[0]
	except:
		coletanea_principal = None

	if not coletanea_principal:
		print "Não existe"
		u = User.objects.get(username__exact='admin')

		coletanea_principal = Coletanea(nome='Principal', descricao='Esta é a coletânea principal.', nivel=0, funcionario=u)
		coletanea_principal.save()

	coletaneas = Coletanea.objects.filter(nivel = 1)

	for coletanea in coletaneas:
		try:
			coletanea.peca = coletanea.pecas.all()[0]
		except:
			pass
	# TODO
	# A função a cima de criação de coletânea inicial/principal precisa ser alterada e esta função
	# deve ir para a parte de banco de dados

	return coletanea_principal, coletaneas

def UTIL_buscar_noticias():

	try:
		noticias = Noticia.objects.all()
	except ObjectDoesNotExist:
		noticias = None


def UTIL_pecas():
	pecas = Peca.objects.all()

	for peca in pecas:
		peca.imagem = Imagem.objects.filter(peca=peca)[0].imagem

	return pecas

def UTIL_pecas_por_coletanea(coletanea_id):
	coletanea = Coletanea.objects.get(id=coletanea_id)

	return coletanea.pecas.all
