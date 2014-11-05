#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

from .generic import *

from criacao.forms import *
from criacao.models import *
from .views import UTIL_informacoes_museu

class InformacoesView(GenericView):

	def editar(self, request):
		museu, museu_nome = UTIL_informacoes_museu()

		if request.method == 'POST':
			try:
				informacoes = InformacoesMuseu.objects.all()[0]
				customfields = CustomField.objects.all()

				for customfield in customfields:
					try:
						informacoes.data[customfield.name] = request.POST[customfield.name]
					except Exception, e:
						informacoes.data[customfield.name] = ''

				informacoes.save()
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
				customfields = CustomField.objects.all()
			except Exception, e:
				logger.error(str(e))

				data = {
					'leftover' : {
						'alert-error' : 'Informações não iniciadas no gerenciamento!',
					}
				}
			else:

				data = {
					'template' : {
						'informacoes' : informacoes,
						'customfields' : customfields,
						'museu' : museu,
						'museu_nome' : museu_nome,
					}
				}
			finally:
				return data

	def listar(self, request):
		museu, museu_nome = UTIL_informacoes_museu()
		try:
			informacoes = InformacoesMuseu.objects.all()[0]
		except Exception, e:
			informacoes = InformacoesMuseu().save()

		return {
			'template' : {
				'informacoes' : informacoes,
				'museu' : museu,
				'museu_nome' : museu_nome,
			}
		}