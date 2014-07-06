#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

from geraldo import Report, ReportBand, Label, Image

from models import Imagem, HistoricoConservacao

import datetime

def abreviar_autor(autor):
	partes = autor.nome.split(" ")
	
	if len(partes) > 1:
		sobre_nome = partes.pop(-1)
		abreviado = partes.pop(0) + " "
	
		for p in partes:
			abreviado += p[0] + ". "
			
		abreviado += sobre_nome
	else:
		abreviado = partes[0]
    
	return abreviado
        
def preencher_relatorio(peca, funcionario):
    
    # Número de Registro
    
    if peca.numero_registro:
        numero_registro = peca.numero_registro
    else:
        numero_registro = "N/A"
    
    # Classificação
    #if peca.secao:
    #    classificacao = peca.secao
    #else:
    #    classificacao = "O que é classificação?"
    if peca.secao:
        secao = peca.secao.nome
    else:
        secao = "N/A"

    classificacao = secao
        
    # Autores
    autores = ""
    print peca.autores.all()
    if peca.autores:
        for autor in peca.autores.all():
            autores += abreviar_autor(autor) + ", "
    else:
        autores = "N/A"

        
    if len(autores) > 35:
        #autores = abreviar_autor(autores)
        autores = autores[0:35:1]
    
        
    # Descrição
    if peca.descricao:
        descricao = peca.descricao
    else:
        descricao = "N/A"
        
    if len(descricao) > 200:
        descricao = descricao[0:280:1]
    
    # Objeto
    
    if peca.objeto:
        objeto = peca.objeto.nome
    else:
        objeto = "N/A"
        
    # Imagem
    imagem = ""
    caminho_imagem = ""
    imagens = Imagem.objects.filter(peca=peca)
    if imagens:       
        imagem = imagens[0].imagem
        CAMINHO_APLICACAO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        caminho_imagem = os.path.join(CAMINHO_APLICACAO, 'museuvirtual', 'media', str(imagem))
    
    # Dimensões
    dimensoes = ""
    if peca.altura:
        dimensoes += str(peca.altura)
    if peca.largura:
        dimensoes += " x " + str(peca.largura)
    if peca.comprimento:
        dimensoes += " x " + str(peca.comprimento)
        
    if dimensoes == "":
        dimensoes = "N/A"
        
    # Peso
    if peca.peso:
        peso = str(peca.peso)
    else:
        peso = "N/A"
        
    # Data de entrada (aquisição)
    
    if peca.data_aquisicao:
        if peca.data_aquisicao.data_especifica:
            data_entrada = peca.data_aquisicao.data_especifica.strftime('%d/%m/%Y')
        elif peca.data_aquisicao.decada:
            data_entrada = peca.data_aquisicao.decada
        elif peca.data_aquisicao.seculo:
            data_entrada = peca.data_aquisicao.seculo
        elif peca.data_aquisicao.periodo:
            data_entrada = peca.data_aquisicao.periodo
        else:
            data_entrada = "N/A"
    else:
        data_entrada = "N/A"
        
    # Modo de aquisicao
    
    coleta = ""
    compra = ""
    doacao = ""
    legado = ""
    emprestimo = ""
    
    if peca.forma_aquisicao:
        if str(peca.forma_aquisicao) == "Coleta":
            coleta = "X"
        elif str(peca.forma_aquisicao) == "Compra":  
            compra = "X"
        elif str(peca.forma_aquisicao) == "Doação":  
            doacao = "X"
        elif str(peca.forma_aquisicao) == "Legado":  
            legado = "X"
        elif str(peca.forma_aquisicao) == "Empréstimo":  
            emprestimo = "X"
            
    # Origem
    
    if peca.origem:
        origem = str(peca.origem)
    else:
        origem = "N/A"
        
    # Procedência 
    
    if peca.procedencia:
        procedencia = str(peca.procedencia)
    else:
        procedencia = "N/A"
        
    # Proprietário
        
    if peca.proprietario:
        proprietario = str(peca.proprietario)
    else:
        proprietario = "N/A"
        
    # Estado de conservação
    
    ultimo_historico = None
    bom = ""
    regular = ""
    ruim = ""

    ultimos_historicos = HistoricoConservacao.objects.filter(peca=peca)
    if ultimos_historicos:
        ultimo_historico = ultimos_historicos.latest('data_avaliacao')
        if ultimo_historico.estado_conservacao:
            if str(ultimo_historico.estado_conservacao) == "Bom":
                bom = "X"
            elif str(ultimo_historico.estado_conservacao) == "Regular":
                regular = "X"
            elif str(ultimo_historico.estado_conservacao) == "Ruim":
                ruim = "X"
            
    # Observações
    
    if peca.observacoes:
        observacoes = str(peca.observacoes)
    else:
        observacoes = "N/A"
        
    if len(observacoes) > 200:
        observacoes = observacoes[0:250:1]
        
    # Responsável
    
    if funcionario:
        responsavel = funcionario.first_name + " " + funcionario.last_name 
        if responsavel == ' ':
        	responsavel = "N/A"
    else:
        responsavel = "N/A"
        
    # Função do Responsável
    
    if funcionario.groups.all():
        funcao_responsavel = str(funcionario.groups.all()[0])
    else:
        funcao_responsavel = "N/A"
        
    # Data do relatório
    
    data_relatorio = datetime.datetime.now().strftime('%d/%m/%Y')
          
    elements = [
            Label(text=numero_registro, top=0.95*cm,  left=13*cm, style={'fontSize': 12}), 
            
            Label(text=classificacao, top=1.95*cm,  left=0.5*cm, width=9*cm, style={'fontSize': 12}), 
            Label(text=objeto, top=3.15*cm,  left=0.5*cm, width=9*cm, style={'fontSize': 12}), 
            Label(text=autores, top=4.45*cm,  left=0.5*cm, width=9*cm, style={'fontSize': 12}),  
            Label(text=descricao, top=5.55*cm,  left=0.5*cm, width=8.5*cm, style={'fontSize': 12}),
            
            Image(left=10.35*cm, top=1.95*cm, width=12.5*cm, height=12.5*cm, filename=caminho_imagem),
             
            Label(text=dimensoes, top=9.75*cm,  left=0.5*cm, width=9*cm, style={'fontSize': 12}), 
            Label(text=peso, top=9.75*cm,  left=6.40*cm, width=9*cm, style={'fontSize': 12}),
            Label(text=data_entrada, top=9.75*cm, left=9.75*cm, width=9*cm, style={'fontSize': 12}),
            
            Label(text=coleta, top=10.65*cm,  left=3.70*cm, style={'fontSize': 12}),
            Label(text=compra, top=10.65*cm,  left=5.5*cm, style={'fontSize': 12}),
            Label(text=doacao, top=10.65*cm,  left=7.40*cm, style={'fontSize': 12}),
            Label(text=legado, top=10.65*cm,  left=9.30*cm, style={'fontSize': 12}),
            Label(text=emprestimo, top=10.65*cm,  left=11.15*cm, style={'fontSize': 12}),
            Label(text="Que informação entra aqui?", top=11.25*cm,  left=0.5*cm, style={'fontSize': 12}),
            
            Label(text=origem, top=13.65*cm,  left=0.5*cm, width=9*cm, style={'fontSize': 12}),
            Label(text=(procedencia + " / " + proprietario), width=9*cm, top=13.65*cm,  left=9.75*cm, style={'fontSize': 12}),
            
            Label(text=bom, top=14.5*cm,  left=4.5*cm, style={'fontSize': 12}),
            Label(text=regular, top=14.5*cm,  left=6.55*cm, style={'fontSize': 12}),
            Label(text=ruim, top=14.5*cm,  left=9.20*cm, style={'fontSize': 12}),
            
            Label(text=observacoes, top=16.00*cm,  left=0.5*cm, width=18*cm, style={'fontSize': 12}),
            Label(text=responsavel, top=19.05*cm,  left=0.5*cm, width=15*cm, style={'fontSize': 12}),
            Label(text=funcao_responsavel, top=20*cm,  left=0.5*cm, width=15*cm, style={'fontSize': 12}),
            Label(text=data_relatorio, top=20.95*cm,  left=0.5*cm, width=15*cm, style={'fontSize': 12}),
        ]
    
    return elements
   

class RelatorioPeca(Report):
        
    page_size = A4    
    
    # Cabeçalho. Aqui, é definida a imagem de fundo.
    class band_page_header(ReportBand):
        
        CAMINHO_APLICACAO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        MODELO = os.path.join(CAMINHO_APLICACAO, 'gerenciamento', 'modelos', 'modelo.jpg')
        
        elements = [
                Image(left=0*cm, top=0*cm, right=0*cm, bottom=0*cm, filename=MODELO),
        ]
        
    # Preenchimento dos dados do relatório em cima da imagem.
    class band_detail(ReportBand):
       
        elements = []
