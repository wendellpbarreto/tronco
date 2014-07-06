#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from django.http import HttpResponse

from reports import RelatorioPeca, preencher_relatorio
from geraldo.generators import PDFGenerator
from models import Peca

from django.shortcuts import render_to_response
from django.template import RequestContext

from django.conf import settings

import zipfile

import pdfkit

from StringIO import StringIO


def gerar_relatorios(request):

	caminho_relatorios = os.path.join(settings.MEDIA_ROOT, 'relatorios')

	options = {
	    'page-size': 'A4',
	    'margin-top': '0.75in',
	    'margin-right': '0.75in',
	    'margin-bottom': '0.75in',
	    'margin-left': '0.75in',
	    'encoding': "UTF-8",
	   #'no-outline': None
	}


	informacoes = dict(request.POST).keys()

	for info in informacoes:
		locals()[info] = True

	lista_pecas = None

	lista_arquivos_pdf = []

	if 'pecas_relatorio' in request.session and request.session['pecas_relatorio']:
		lista_pecas = request.session['pecas_relatorio']

	for peca in lista_pecas:

		rtr = render_to_response('relatorio_peca.html', locals(), context_instance=RequestContext(request))
		conteudo = rtr.content

		arquivo = open(os.path.join(caminho_relatorios, '%s.html' %peca.id), 'w')
		arquivo.write(conteudo)

		caminho_arquivo_html = arquivo.name
		arquivo.close()

		caminho_arquivo_pdf = os.path.join(caminho_relatorios, peca.numero_registro + '.pdf')

		pdfkit.from_file(caminho_arquivo_html, caminho_arquivo_pdf, options=options)

		lista_arquivos_pdf.append(caminho_arquivo_pdf)

	if len(lista_arquivos_pdf) > 1:

		zf = zipfile.ZipFile(os.path.join(caminho_relatorios, "relatorios.zip"), "w")

		for arquivo_pdf in lista_arquivos_pdf:

			zf.write(arquivo_pdf, arquivo_pdf.split("/")[-1])

		zf.close()

		arquivo = open(os.path.join(caminho_relatorios, "relatorios.zip"))

		saida = arquivo.read()

		arquivo.close()

		resp = HttpResponse(saida, mimetype = "application/x-zip-compressed")
		resp['Content-Disposition'] = 'attachment; filename=relatorios.zip'

		return resp

	elif len(lista_arquivos_pdf) == 1:

		arquivo_pdf = lista_arquivos_pdf[0]

		arquivo = open(arquivo_pdf)

		saida = arquivo.read()

		arquivo.close()

		resp = HttpResponse(saida, mimetype = "application/pdf")
		resp['Content-Disposition'] = 'attachment; filename=relatorio.pdf'

		return resp

	else:
		
		return HttpResponse("Erro")

	#return render_to_pdf('saida_relatorio/saida.html', RequestContext(request))


def relatorio(request, peca_id):
    
    funcionario = request.user # Verificar se é o funcionário que cadastrou ou que gerou o relatório...
    resposta = HttpResponse(mimetype='application/pdf')
    
    peca = Peca.objects.get(id=peca_id)          
     
    if peca:
        relatorio = RelatorioPeca(queryset=[peca,],)
        relatorio.band_detail.elements = preencher_relatorio(peca, funcionario)      
        relatorio.generate_by(PDFGenerator, filename=resposta)

    return resposta


