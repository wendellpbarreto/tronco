#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

from datetime import datetime, date, time

from .generic import *

from criacao.forms import *
from criacao.models import *
from gerenciamento.models import *

class ColetaneaView(GenericView):

	def criar(self, request):
		if request.method == 'POST':
			form = ColetaneaForm(request.POST)
			if not form.is_valid():
				data = {
					'leftover' : {
						'validation-error' : form.errors,
					},
				}
				return data
			
			nome = request.POST['nome']
			descricao = request.POST['descricao']
			fim_exposicao = request.POST['fim_exposicao']
			inicio_exposicao = request.POST['inicio_exposicao']
		
			try:
				inicio_exposicao = datetime.strptime(inicio_exposicao, "%d/%m/%Y")
			except:
				inicio_exposicao = datetime.strptime("01/01/2013", "%d/%m/%Y")

			try:
				fim_exposicao = datetime.strptime(fim_exposicao, "%d/%m/%Y")
			except:
				fim_exposicao = datetime.strptime("01/01/2113", "%d/%m/%Y")

			try:
				lista_de_pecas = request.POST.getlist('lista_de_pecas[]')
			except:
				pass

			if not lista_de_pecas:
				data = {
					'leftover' : {
						'alert-error' : 'Coletânea precisa ter pelo menos uma peça!',
					},
				}
			else:
				try:
					coletanea = Coletanea(
						nome=nome,
						descricao=descricao,
						funcionario=request.user,
						inicio_exposicao=inicio_exposicao,
						fim_exposicao=fim_exposicao,
					)
					coletanea.save()

					for peca in lista_de_pecas:
					 	peca = Peca.objects.get(numero_registro=peca)
					 	coletanea.pecas.add(peca)
				except Exception, e:
					data = {
						'leftover' : {
							'alert-error' : 'Não foi possível cadastrar a peça, tente novamente',
						},
					}
				else:
					data = {
						'leftover' : {
							'alert-success' : 'Coletânea criada com sucesso!',
							'redirect' : '/criacao/coletanea/listar/'
						},
					}
			return data
		else:
			museu, museu_nome = UTIL_informacoes_museu()
			form = ColetaneaForm()
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
					'alert-error' : 'Não foi possível processar essa visualização!',
				},
			}
		else:
			museu, museu_nome = UTIL_informacoes_museu()

			coletanea = Coletanea.objects.get(pk=pk)
			pecas = coletanea.pecas.all()

			for peca in pecas:
				peca.imagem = Imagem.objects.filter(peca=peca)[0].imagem

			coletanea.lista_pecas = pecas

			data = {
				'template' : {
					'request' : request,
					'museu_nome' : museu_nome,
					'coletanea' : coletanea,
				},
			}
		finally:
			return data

	def editar(self, request):

		if request.method == 'POST':
			form = ColetaneaForm(request.POST)
			if not form.is_valid():
				data = {
					'leftover' : {
						'validation-error' : form.errors,
					},
				}
				return data
			
			pk = self.kwargs['key']
			nome = request.POST['nome']
			descricao = request.POST['descricao']
			inicio_exposicao = request.POST['inicio_exposicao']
			fim_exposicao = request.POST['fim_exposicao']
		
			try:
				inicio_exposicao = datetime.strptime(inicio_exposicao, "%d/%m/%Y")
			except:
				inicio_exposicao = datetime.strptime("01/01/2013", "%d/%m/%Y")

			try:
				fim_exposicao = datetime.strptime(fim_exposicao, "%d/%m/%Y")
			except:
				fim_exposicao = datetime.strptime("01/01/2113", "%d/%m/%Y")

			try:
				lista_de_pecas = request.POST.getlist('lista_de_pecas[]')
			except:
				pass

			if not lista_de_pecas:

				return {
					'leftover' : {
						'alert-error' : 'Coletânea precisa ter pelo menos uma peça!',
					},
				}

			coletanea = Coletanea.objects.get(pk=pk);
			coletanea.nome = nome
			coletanea.descricao = descricao
			coletanea.inicio_exposicao = inicio_exposicao
			coletanea.fim_exposicao = fim_exposicao
			coletanea.save()

			coletanea.pecas.clear()

			for peca in lista_de_pecas:
				peca = Peca.objects.get(numero_registro = peca)
				coletanea.pecas.add(peca)

			data = {
				'leftover' : {
					'alert-success' : 'Coletânea editada com sucesso!',
					'redirect' : '/criacao/coletanea/listar/'
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

				coletanea = Coletanea.objects.get(pk=pk)
				pecas = coletanea.pecas.all()

				for peca in pecas:
					peca.imagem = Imagem.objects.filter(peca=peca)[0].imagem

				coletanea.lista_pecas = pecas

				form = ColetaneaForm(initial={
					'nome' : coletanea.nome,
					'descricao' : coletanea.descricao,
					'inicio_exposicao' : coletanea.inicio_exposicao,
					'fim_exposicao' : coletanea.fim_exposicao,
				})

				data = {
					'template' : {
						'request' : request,
						'museu_nome' : museu_nome,
						'coletanea' : coletanea,
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
			Coletanea.objects.get(pk=pk).delete()

			data = {
				'leftover' : {
					'alert-success' : 'Coletânea deletada com sucesso!',
				},
			}
		finally:
			return data

	def listar(self, request):
		listagem = False
		museu, museu_nome = UTIL_informacoes_museu()
		coletanea_principal, coletaneas = UTIL_buscar_coletaneas()

		try:
			page = int(self.kwargs['key'])
		except:
			page = 1
		finally:
			coletaneas = paginate(obj=coletaneas, page=page, num_per_page=8)

		data = {
			'template' : {
				'request' : request,
				'museu' : museu,
				'museu_nome' : museu_nome,
				'coletaneas' : coletaneas,
				'coletanea_principal' : coletanea_principal,
				'listagem' : listagem,
			},
		}

		return data