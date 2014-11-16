#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gerenciamento.models import *
from criacao.views.views import *
from criacao.forms import *

from django.contrib.auth.models import User

class TemaView(GenericView):

	def get_context_data(self, request):

		try:
			slug = self.kwargs['slug']

			if slug == 'criar':
				try:
					if request.method == 'GET':
						museu, museu_nome = UTIL_informacoes_museu()
						form = ColetaneaForm()					

						return {'template' : {
										'request' : request,
										'museu_nome' : museu_nome,
										'form' : form,
									},
								}
					elif request.method == 'POST':
						nome = loads_json(request.POST['nome'])
						descricao = loads_json(request.POST['descricao'])
						pecas = loads_json(request.POST['pecas'])

						u = User.objects.get(username__exact='admin')

						cltn = Coletanea(nome=nome, descricao=descricao, funcionario=u)
						cltn.save()

						for peca in pecas:
							peca = Peca.objects.get(numero_registro=peca)
							cltn.pecas.add(peca)

						return {'leftover' : {
										'alert-success' : 'Coletânea criada com sucesso!',
										'redirect' : '/criacao/coletanea/listar/'
									},
								}						
				except:
					return None
			elif slug == 'visualizar':
				try:
					key = self.kwargs['key']					

					museu, museu_nome = UTIL_informacoes_museu()

					coletanea = Coletanea.objects.get(pk = key)
					pecas = coletanea.pecas.all()

					for peca in pecas:
						peca.imagem = Imagem.objects.filter(peca=peca)[0].imagem

					coletanea.lista_pecas = pecas

					return {'template' : {
									'request' : request,
									'museu_nome' : museu_nome,
									'coletanea' : coletanea,
								},
							}
				except:
					return None
			elif slug == 'editar':
				try:
					key = self.kwargs['key']					

					if request.method == 'GET':
						museu, museu_nome = UTIL_informacoes_museu()
	
						coletanea = Coletanea.objects.get(id = key)
						pecas = coletanea.pecas.all()
						
						for peca in pecas:
							peca.imagem = Imagem.objects.filter(peca=peca)[0].imagem
						
						coletanea.lista_pecas = pecas
						
						form = ColetaneaForm(initial = {'nome' : coletanea.nome, 'descricao' : coletanea.descricao})

						return {'template' : {
										'request' : request,
										'museu_nome' : museu_nome,
										'coletanea' : coletanea,
										'form' : form,
									},
								}
					elif request.method == 'POST':
						nome = loads_json(request.POST['nome'])
						descricao = loads_json(request.POST['descricao'])
						pecas = loads_json(request.POST['pecas'])

						cltn = Coletanea.objects.get(pk = key);
						cltn.nome=nome
						cltn.descricao=descricao
						cltn.save()

						cltn.pecas.clear()
						
						for peca in pecas:
							peca = Peca.objects.get(numero_registro=peca)
							cltn.pecas.add(peca)

						return {'leftover' : {
										'alert-success' : 'Coletânea salva com sucesso!',
										'redirect' : '/criacao/coletanea/listar/'
									},
								}
				except:
					return None
			elif slug == 'excluir':
				try:
					key = self.kwargs['key']	

					Coletanea.objects.get(pk = key).delete()

					return {'leftover' : {
									'alert-success' : 'Coletânea deletada com sucesso!',
								},
							}
				except:
					return None
			else:
				museu, museu_nome = UTIL_informacoes_museu()	
				coletaneas = UTIL_buscar_coletaneas()

				return {'template' : {
								'request' : request,
								'museu' : museu,
								'museu_nome' : museu_nome,
								'coletaneas' : coletaneas,
							},
						}
		except:
			return None