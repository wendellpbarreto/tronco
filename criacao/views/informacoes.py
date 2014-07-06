#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

from .generic import *

from criacao.forms import *
from criacao.models import * 

class InformacoesView(GenericView):

	def editar(self, request):
		if request.method == 'POST':
			try:
				informacoes = InformacoesMuseu.objects.all()[0]
				form = InformacoesMuseuForm(request.POST, instance=informacoes)
				form.save()
			except Exception, e:
				logger.error(str(e))
				
				data = {
					'leftover' : {
						'alert-error' : 'Ocorreu um erro na edição, tentar novamente mais tarde!',
						'redirect' : '/criacao/informacoes/listar/'
					},
				}
			else:
				data = {
					'leftover' : {
						'alert-success' : 'Informações editadas com sucesso!',
						'redirect' : '/criacao/informacoes/listar/'
					},
				}
			finally:
				return data
		else:
			try:
				informacoes = InformacoesMuseu.objects.all()[0]
			except Exception, e:
				logger.error(str(e))

				data = {
					'leftover' : {
						'alert-error' : 'Informações não iniciadas no gerenciamento!',
					}
				}
			else:
				form = InformacoesMuseuForm(instance=informacoes)

				data = {
					'template' : {
						'form' : form,
					}
				}
			finally:
				return data

	def listar(self, request):
		informacoes = InformacoesMuseu.objects.all()[0]
		museu, museu_nome = UTIL_informacoes_museu()	
		
		return {
			'template' : {
				'informacoes' : informacoes,
				'museu' : museu,
				'museu_nome' : museu_nome,
			}
		}