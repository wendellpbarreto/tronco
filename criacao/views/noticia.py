#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

from .generic import *

from criacao.forms import *
from criacao.models import * 
from gerenciamento.models import *


class NoticiaView(GenericView):

	def criar(self, request): 

		if request.method == 'POST':
			form = NoticiaForm(request.POST)
			if not form.is_valid():
				data = {
					'leftover' : {
						'validation-error' : form.errors,
					},
				}
				return data
		
			titulo = request.POST['titulo']
			descricao_breve = request.POST['descricao_breve']
			descricao = request.POST['descricao']
		
			noticia = Noticia(titulo=titulo, descricao_breve=descricao_breve, descricao=descricao)
			try:
				noticia.save() 
			except Exception, e:
				logger.error(str(e))

			data = {
				'leftover' : {
					'alert-success' : 'Notícia criada com sucesso!',
					'redirect' : '/criacao/noticia/listar/'
				},
			}	 
		
			return data
	
		museu, museu_nome = UTIL_informacoes_museu()
		form = NoticiaForm()
		pecas = Peca.objects.all()					

		data = {
			'template' : {
				'request' : request,
				'museu_nome' : museu_nome,
				'form' : form,
				'pecas' : pecas,
			},
		}	

		return data

	def visualizar(self, request):

		try:
			pk = self.kwargs['key']					
		except Exception, e:
			logger.error(str(e))

			data = {
				'leftover' : {
					'alert-error' : 'Não foi possível processar essa visualização.',
				}
			}
		else:
			museu, museu_nome = UTIL_informacoes_museu()

			noticia = Noticia.objects.get(pk=pk)
			pecas = noticia.pecas.all()

			for peca in pecas:
				peca.imagem = Imagem.objects.filter(peca=peca)[0].imagem

			noticia.lista_pecas = pecas

			data = {
				'template' : {
					'request' : request,
					'museu_nome' : museu_nome,
					'noticia' : noticia,
				},
			}
		finally:
			return data

	def editar(self, request):
		if request.method == 'POST':
			form = NoticiaForm(request.POST)
			if not form.is_valid():
				data = {
					'leftover' : {
						'validation-error' : form.errors,
					},
				}
				return data

			pk = self.kwargs['key']
			titulo = request.POST['titulo']
			descricao_breve = request.POST['descricao_breve']
			descricao = request.POST['descricao']

			noticia = Noticia.objects.get(pk=pk);

			noticia.titulo=titulo
			noticia.descricao_breve=descricao_breve
			noticia.descricao=descricao

			try:
				noticia.save() 
			except Exception, e:
				logger.error(str(e))

			data = {
				'leftover' : {
					'alert-success' : 'Notícia editada com sucesso!',
					'redirect' : '/criacao/noticia/listar/'
				},
			}

			return data
		else:
			try:
				pk = self.kwargs['key']
			except Exception, e:
				logger.error(str(e))

				data = {
					'leftover' : {
						'alert-error' : 'Não foi possível processar essa edição!',
					}
				}
			else:
				museu, museu_nome = UTIL_informacoes_museu()

				noticia = Noticia.objects.get(pk=pk);
				pecas = noticia.pecas.all()

				for peca in pecas:
					peca.imagem = Imagem.objects.filter(peca=peca)[0].imagem

				noticia.lista_pecas = pecas

				form = NoticiaForm(initial={
					'titulo': noticia.titulo, 
					'descricao_breve': noticia.descricao_breve, 
					'descricao': noticia.descricao
				})

				data = {
					'template' : {
						'request' : request,
						'museu_nome' : museu_nome,
						'noticia' : noticia,
						'form' : form,
					},
				} 
			finally:
				return data

	def excluir(self, request):
		try:
			pk = self.kwargs['key']	
		except Exception, e:
			logger.error(str(e))

			data = {
				'leftover' : {
					'alert-error' : 'Não foi possível processar essa exclusão!',
				}
			}
		else:
			Noticia.objects.get(pk=pk).delete()

			data = {
				'leftover' : {
					'alert-success' : 'Notícia deletada com sucesso!',
					'reload': True,
				},
			}
		finally:
			return data
 
	def listar(self, request):
		museu, museu_nome = UTIL_informacoes_museu()	
		noticias = Noticia.objects.order_by('-id')

		try:
			page = int(self.kwargs['key'])
		except:
			page = 1
		finally:
			noticias = paginate(obj=noticias, page=page, num_per_page=3)

		data = {
			'template' : {
				'request' : request,
				'museu' : museu,
				'museu_nome' : museu_nome,
				'noticias' : noticias,
			},
		} 

		return data