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

class PecaView(GenericView):

	def criar(self, request):
		data = None

		form = PecaForm()

		data = {
			'template' : {
				'form' : form,
			}
		}

		return data
		
	def listar(self, request):
		museu, museu_nome = UTIL_informacoes_museu()	
		pecas = Peca.objects.all()

		try:
			page = int(self.kwargs['key'])
		except:
			page = 1
		finally:
 			pecas = paginate(obj=pecas, page=page, num_per_page=8)

		data = {
			'template' : {
				'request' : request,
				'museu' : museu,
				'museu_nome' : museu_nome,
				'pecas' : pecas,
			},
		} 

		return data