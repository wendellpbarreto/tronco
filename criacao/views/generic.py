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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.template.loader import render_to_string
from django.views.generic import View

from criacao.models import *

def render_to_json(request, template, context_data):
	'''
	Render the template and context data to JSON object
	'''
	response = {}	

	try: 
		return context_data['file']
	except:
		pass
	
	try:
		template_data = context_data['template']
	except Exception, e:
		logger.warning('Variable context_data[template] aren\'t defined! Raised: ' + str(e))

		template_data = None

	try:
		leftover_data = context_data['leftover']
	except:
		leftover_data = None

	try:
		response['template'] = render_to_string(template, template_data, context_instance=RequestContext(request))
	except:
		pass
		
	try:
		for key, value in leftover_data.items():	
			if key == 'redirect' and value == 'none':
				response['template'] = None
			else:
				response[key] = value
	except Exception, e:
		logger.warning ('Not lefover items! Raised: ' + str(e))
		

	return HttpResponse(json.dumps(response), mimetype='application/json')

def load_json(request):
	'''
	Load JSON requests
	'''
	try:
		response = json.loads(request)
	except:
		response = None

	return response

class GenericView(View):
	'''
	Generic view thats improve all custom views work
	'''
	def _request(self, request, *args, **kwargs):

		if request.is_ajax():

			return render_to_json(request, self.get_template_name(request), self.get_context_data(request))
		else:
			context_data = self.get_context_data(request)

			try:
				return context_data['file']
			except:
				pass

			try:
				template_data = context_data['template']
			except Exception, e:
				logger.warning('Variable context_data[template] aren\'t defined! Raised: ' + str(e))

				template_data = None						

			try:
				leftover_data = context_data['leftover']
			except:
				leftover_data = None

			try:
				for key, value in leftover_data.items():	
					if key == 'redirect':
						return HttpResponseRedirect(value)
			except Exception, e:
				logger.warning ('Not lefover items! Raised: ' + str(e))

			return render_to_response(self.get_template_name(request), template_data, context_instance=RequestContext(request))

	def post(self, request, *args, **kwargs):

		return self._request(request, args, kwargs)
		
	def get(self, request, *args, **kwargs):

		return self._request(request, args, kwargs)

	def get_context_data(self, request):
		data = {}

		try:
			slug = str(self.kwargs['slug'])
		except Exception, e:
			logger.error('Kwargs[slug] isn\'t defined! Raised: ' + str(e))
		else:	
			slug_method = getattr(self, slug)
			data = slug_method(request)
		finally:
			return data

	def get_template_name(self, request):
		page_name = request.resolver_match.url_name
		app_name = request.resolver_match.app_name
		paths = []

		try:
			slug = str(self.kwargs['slug'])
		except Exception, e:
			logger.error('Kwargs[slug] aren\'t defined! Raised: ' + str(e))

			return app_name + '/404.html'
		else:
			if request.is_ajax():				
				paths.append(app_name + '/' + page_name + '/ajax/' + slug + '.html')
				paths.append(app_name + '/ajax/' + page_name + '.html')
				paths.append(page_name + '/ajax/' + slug + '.html')
			else:
				paths.append(app_name + '/' + page_name + '/' + slug + '.html')
				paths.append(app_name + '/' + page_name + '.html')
				paths.append(app_name + '/' + slug + '.html')

			for path in paths:
				try:
					template = loader.get_template(path)				
				except Exception, e:
					logger.error('Template not found! Raised: ' + str(e))
				else:
					logger.info('Template loaded: ' + str(path))

					return path
				
			logger.info('Not found available templates, loading 404 template!')

			return app_name + '/404.html'


def paginate(obj, page, num_per_page):
	'''
	Easy way to paginate object query set
	'''
	paginator = Paginator(obj, num_per_page)

	try:
		page = int(page)
		obj = paginator.page(page)
	except PageNotAnInteger:
		page = 1
		obj = paginator.page(page)
	except EmptyPage:
		page = paginator.num_pages
		obj = paginator.page(page)
	except:
		page = 1
		obj = paginator.page(page)

	try:
		paginator.page(page - 10)
		paginator.page(page - 11)

		obj.has_less_ten = page - 10					
	except EmptyPage:
		pass

	try:
		paginator.page(page - 2)
		obj.has_less_two = page - 2
	except EmptyPage:
		pass

	try:
		paginator.page(page - 3)
		obj.has_less_three = page - 3
	except EmptyPage:
		pass

	obj.page = page

	try:
		paginator.page(page + 2)
		obj.has_more_two = page + 2
	except EmptyPage:
		pass

	try:
		paginator.page(page + 3)
		obj.has_more_three = page + 3
	except EmptyPage:
		pass
	
	try:
		paginator.page(page + 10)
		paginator.page(page + 11)

		obj.has_more_ten = page + 10					
	except EmptyPage:
		pass

	return obj

# TRASH CODE --------------------------------------------------------------------------------------------------
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

# -------------------------------------------------------------------------------------------------------------