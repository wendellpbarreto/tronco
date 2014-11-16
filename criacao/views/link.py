#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from .generic import *

from criacao.forms import *
from criacao.models import * 
from gerenciamento.models import *

logger = logging.getLogger(__name__)

class LinkView(GenericView):

	def criar(self, request): 

		if request.method == 'POST':
			try:
				name = request.POST['name']
				url = request.POST['url']
			except Exception, e:
				logger.error(str(e))

				data = {
					'leftover' : {
						'alert-error' : 'Está faltando alguma informação, por favor, verifique os campos!',
					}
				}
			else:
				link = Link(name=name, url=url)
				try:
					link.save() 
				except Exception, e:
					logger.error(str(e))

				data = {
					'leftover' : {
						'alert-success' : 'Link criado com sucesso!',
						'redirect' : '/criacao/link/listar/'
					},
				}	 
			finally:
				return data
		else:
			museu, museu_nome = UTIL_informacoes_museu()
			form = LinkForm()

			data = {
				'template' : {
					'request' : request,
					'museu_nome' : museu_nome,
					'form' : form,
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

			link = Link.objects.get(pk=pk)

			data = {
				'template' : {
					'request' : request,
					'museu_nome' : museu_nome,
					'link' : link,
				},
			}
		finally:
			return data

	def editar(self, request):

		if request.method == 'POST':
			try:
				pk = self.kwargs['key']
				name = request.POST['name']
				url = request.POST['url']
			except Exception, e:
				logger.error(str(e))

				data = {
					'leftover' : {
						'alert-error' : 'Não foi possível processar esta edição!',
					}
				}
			else:
				link = Link.objects.get(pk=pk);

				link.name=name
				link.url=url
				link.save() 

				data = {
					'leftover' : {
						'alert-success' : 'Link editada com sucesso!',
						'redirect' : '/criacao/link/listar/'
					},
				}
			finally:
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

				link = Link.objects.get(pk=pk);

				form = LinkForm(initial={
					'name': link.name, 
					'url': link.url, 
				})

				data = {
					'template' : {
						'request' : request,
						'museu_nome' : museu_nome,
						'link' : link,
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
			Link.objects.get(pk=pk).delete()

			data = {
				'leftover' : {
					'alert-success' : 'Link deletado com sucesso!',
				},
			}
		finally:
			return data
 
	def listar(self, request):
		museu, museu_nome = UTIL_informacoes_museu()	
		links = Link.objects.all()

		try:
			page = int(self.kwargs['key'])
		except:
			page = 1
		finally:
			links = paginate(obj=links, page=page, num_per_page=8)

		data = {
			'template' : {
				'request' : request,
				'museu' : museu,
				'museu_nome' : museu_nome,
				'links' : links,
			},
		} 

		return data