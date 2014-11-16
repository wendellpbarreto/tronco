#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
try:
    from PIL import Image
except ImportError:
    import Image

from django.db.models import signals
from django.dispatch.dispatcher import receiver

from django.core.exceptions import ObjectDoesNotExist, ValidationError

from django.db import models
from django.contrib.auth.models import User, Group

from sorl.thumbnail import ImageField
from museuvirtual.settings import MEDIA_ROOT

from decimal import Decimal

import museuvirtual.create_auto_admin


class Categoria(models.Model):
	nome = models.CharField(max_length=200, help_text="Categoria da obra (200 caracteres, no máximo).", unique=True)

	def __unicode__(self):
		return self.nome

	class Meta:
		verbose_name = "Categoria da Obra"
		verbose_name_plural = "Categorias da Obra"

class FonteOriginal(models.Model):
	nome = models.CharField(max_length=200, help_text="Acervo onde o suporte físico se encontra (200 caracteres, no máximo).", unique=True)

	def __unicode__(self):
		return self.nome

	class Meta:
		verbose_name = "Fonte Original"
		verbose_name_plural = "Fontes Originais"

class FuncaoAutor(models.Model):
	nome = models.CharField(max_length=200, help_text="Nome da função do autor (200 caracteres, no máximo).", unique=True)

	def __unicode__(self):
		return self.nome

	class Meta:
		verbose_name = "Função do Autor"
		verbose_name_plural = "Funções do Autor"


class Autor(models.Model):
	nome = models.CharField(max_length=200, help_text="Nome do autor (200 caracteres, no máximo).", null=False, blank=False)
	nome_artistico = models.CharField(verbose_name="Nome artístico", max_length=200, help_text="Nome artístico do autor (200 caracteres, no máximo). ", blank=True, null=True)
	funcao_autor = models.ForeignKey(FuncaoAutor, verbose_name="Função do autor", help_text="Função do autor", blank=True, null=True,)


	def __unicode__(self):

		retorno = self.nome

		if self.nome_artistico:
			retorno += " (%s) " %self.nome_artistico

		if self.funcao_autor:
			retorno += " - %s" %self.funcao_autor

		return retorno

	def __str__(self):

		retorno = self.nome

		if self.nome_artistico:
			retorno += " (%s) " %self.nome_artistico

		if self.funcao_autor:
			retorno += " - %s" %self.funcao_autor

		return retorno

	class Meta:
		verbose_name = "Autor"
		verbose_name_plural = "Autores"

class Origem(models.Model):
	nome = models.CharField(max_length=200, unique=True, help_text="Local/ cidade de origem da peça (200 caracteres, no máximo).")

	def __unicode__(self):
		return self.nome

	class Meta:
		verbose_name = "Origem"
		verbose_name_plural = "Origens"

class Procedencia(models.Model):
	nome = models.CharField(max_length=200, help_text="Nome da procedência da peça (200 caracteres, no máximo).", unique=True)

	def __unicode__(self):
		return self.nome

	class Meta:
		verbose_name = "Procedência"
		verbose_name_plural = "Procedências"


class Proprietario(models.Model):
	nome = models.CharField(max_length=200, help_text="Nome do atual proprietário (200 caracteres, no máximo).", unique=True)

	def __unicode__(self):
		return self.nome

	class Meta:
		verbose_name = "Proprietário"
		verbose_name_plural = "Proprietários"

class ExProprietario(models.Model):
	nome = models.CharField(max_length=200, help_text="Nome do ex-proprietário (200 caracteres, no máximo).", unique=True)

	def __unicode__(self):
		return self.nome

	class Meta:
		verbose_name = "Ex-Proprietário"
		verbose_name_plural = "Ex-Proprietários"

class Secao(models.Model):
	nome = models.CharField(max_length=200, help_text="Nome da seção (200 caracteres, no máximo).", unique=True)

	def __unicode__(self):
		return self.nome

	class Meta:
		verbose_name = "Seção"
		verbose_name_plural = "Seções"

class Colecao(models.Model):
	nome = models.CharField(max_length=200, help_text="Nome da coleção (200 caracteres, no máximo).", unique=True)

	def __unicode__(self):
		return self.nome

	class Meta:
		verbose_name = "Coleção"
		verbose_name_plural = "Coleções"

class SubColecao(models.Model):
	nome = models.CharField(max_length=200, help_text="Nome da sub-coleção (200 caracteres, no máximo).", unique=True)
	colecao = models.ForeignKey(Colecao, verbose_name="Coleção")

	def __unicode__(self):
		return self.nome

	class Meta:
		verbose_name = "Sub-Coleção"
		verbose_name_plural = "Sub-Coleções"

class Material(models.Model):
	nome = models.CharField(max_length=200,  help_text="Material em que a peça foi construída (200 caracteres, no máximo).", unique=True)

	def __unicode__(self):
		return self.nome

	class Meta:
		verbose_name = "Material"
		verbose_name_plural = "Materiais"

class Tecnica(models.Model):
	nome = models.CharField(max_length=200,  help_text="Técnica em que a peça foi construída (200 caracteres, no máximo).", unique=True)

	def __unicode__(self):
		return self.nome

	class Meta:
		verbose_name = "Técnica"
		verbose_name_plural = "Técnicas"


class FormaAquisicao(models.Model):
	nome = models.CharField(max_length=200,  help_text="Nome da forma de aquisição (200 caracteres, no máximo).", unique=True)

	def __unicode__(self):
		return self.nome

	class Meta:
		verbose_name = "Forma de Aquisição"
		verbose_name_plural = "Formas de Aquisição"

class Provisor(models.Model):
	nome = models.CharField(max_length=200, help_text="Nome do provisor (200 caracteres, no máximo).", unique=True)

	def __unicode__(self):
		return self.nome

	class Meta:
		verbose_name = "Provisor"
		verbose_name_plural = "Provisores"

class Cargo(models.Model):
	nome = models.CharField(max_length=200, help_text="Nome do cargo (200 caracteres, no máximo).", unique=True)

	def __unicode__(self):
		return self.nome

	class Meta:
		verbose_name = "Cargo"
		verbose_name_plural = "Cargos"

class Equipe(models.Model):
	nome = models.CharField(max_length=200, help_text="Nome da equipe (200 caracteres, no máximo).", unique=True)

	def __unicode__(self):
		return self.nome

	class Meta:
		verbose_name = "Equipe"
		verbose_name_plural = "Equipes"

class FuncaoFuncionario(Group):

	class Meta:
		verbose_name = "Função do Funcionário"
		verbose_name_plural = "Funções do Funcionário"

class Funcionario(User):

	class Meta:
		verbose_name = "Funcionário"
		verbose_name_plural = "Funcionários"

class InformacoesFuncionais(models.Model):
	usuario = models.OneToOneField(Funcionario, verbose_name="Usuário do sistema", help_text="Funcionário.", primary_key=True)
	cpf = models.CharField(verbose_name="CPF", help_text="Número do CPF (somente números, com 11 caracteres, no máximo).", max_length=11, blank=True, null=True)
	rg = models.CharField(verbose_name="RG", help_text="Número do RG (somente números, com 11 caracteres, no máximo).", max_length=11, blank=True, null=True)
	data_de_nascimento = models.DateField(verbose_name="Data de Nascimento", help_text="Data de nascimento do funcionário, seguindo o formato dd/mm/aaaa.", blank=True, null=True)
	cargo = models.ForeignKey(Cargo, help_text="Cargo que o funcionário pode estar ocupando no momento.", blank=True, null=True)
	equipe = models.ForeignKey(Equipe, help_text="Equipe a qual o funcionário pertence no momento.", blank=True, null=True)
	funcao_funcionario = models.ForeignKey(FuncaoFuncionario, verbose_name="Função do Funcionário.", help_text="Função que o funcionário exerce no museu.", blank=True, null=True)


class DataFormatada(models.Model):
	data_especifica = models.DateField(verbose_name="Data específica", help_text="Data específica, seguindo o formato dd/mm/aaaa.", blank=True, null=True)
	decada_ano = models.CharField(verbose_name="Década/ Ano", max_length=4, help_text="Década ou ano (até quatro caracteres).", blank=True, null=True)
	seculo = models.CharField(verbose_name="Século", max_length=3, help_text="Século (até 3 caracteres).", blank=True, null=True)
	periodo = models.CharField(verbose_name="Período", max_length=50, help_text="Período (formatação livre, com 50 caracteres, no máximo)", blank=True, null=True)

	def __unicode__(self):
		if self.data_especifica:
			return  unicode(self.data_especifica.strftime('%d/%m/%Y'))
		elif self.decada_ano:
			return u'Década/ ano de ' + self.decada_ano
		elif self.seculo:
			return u'Século ' + self.seculo
		elif self.periodo:
			return u'Período ' + self.periodo

	class Meta:
		verbose_name = "Data"
		verbose_name_plural = "Datas"

class Objeto(models.Model):
	nome = models.CharField(max_length=200, help_text="Breve descrição do objeto (200 caracteres, no máximo).", unique=True)

	def __unicode__(self):
		return self.nome

	class Meta:
		verbose_name = "Objeto"
		verbose_name_plural = "Objetos"


class TipoMoeda(models.Model):
	nome = models.CharField(max_length=200, help_text="Tipo da Moeda (real, cruzeiro, dolar etc., com 200 caracteres, no máximo).", unique=True)

	def __unicode__(self):
		return self.nome

	class Meta:
		verbose_name = "Tipo de Moeda"
		verbose_name_plural = "Tipos de Moeda"

class Peca(models.Model):

	# Informações essenciais

	numero_registro = models.CharField(max_length=20, verbose_name="Número de Registro", help_text="Número de registro da peça (20 caracteres, no máximo). Evite o uso de acentos, espaços e caracteres especiais. (Ex.: EI2013-01, MCC201021, EXPO-IND-2012) ", blank=False, null=False, unique=True)

	secao = models.ForeignKey(Secao, verbose_name="Seção", help_text="Seção onde peça está.", blank=True, null=True)
	colecao = models.ForeignKey(Colecao, verbose_name="Coleção", help_text="Coleção que a peça faz parte.", blank=True, null=True)
	sub_colecao =  models.ForeignKey(SubColecao, verbose_name="Sub-coleção", help_text="Subcoleção que a peça faz parte.", blank=True, null=True)


	objeto = models.ForeignKey(Objeto, help_text="Breve descrição do objeto.", blank=False, null=False)
	titulo = models.CharField(max_length=200, verbose_name="Título",  help_text="Título da peça (200 caracteres, no máximo).", blank=False, null=False)
	autores = models.ManyToManyField(Autor, help_text="Autor da peça.", blank=False, null=False, related_name='autores')
	data_criacao = models.ForeignKey(DataFormatada, verbose_name="Data de Criação", help_text="Data de criação da peça.", blank=False, null=False, related_name="data_criacao")
	descricao = models.TextField(verbose_name="Descrição", max_length=500, help_text="Descrição detalhada da peça (500 caracteres, no máximo). .", blank=False, null=False)
	categoria = models.ForeignKey(Categoria, verbose_name="Categoria", help_text="Categoria da peça.", blank=True, null=True)


	# Informações mais específicas

	origem = models.ForeignKey(Origem, help_text="Origem da peça.", blank=True, null=True)
	iconografia = models.TextField(max_length=500, help_text="Iconografia da peça (500 caracteres, no máximo).", blank=True, null=True)
	observacoes = models.TextField(verbose_name="Observações", max_length=200, help_text="Observações sobre a peça (200 caracteres, no máximo)..", blank=True, null=True)
	dados_historicos = models.TextField(verbose_name="Dados históricos", max_length=500, help_text="Dados históricos da peça (500 caracteres, no máximo).", blank=True, null=True)
	referencias = models.TextField(max_length=500, verbose_name="Referências", help_text="Referências (500 caracteres, no máximo).", blank=True, null=True)
	texto = models.TextField(max_length=500, verbose_name="Texto", help_text="Texto referente à peça (500 caracteres, no máximo)..", blank=True, null=True)


	procedencia = models.ForeignKey(Procedencia, verbose_name="Procedência", help_text="Procedência da peça.", blank=True, null=True)
	proprietario = models.ForeignKey(Proprietario, verbose_name="Proprietário", help_text="Proprietário da peça.", blank=True, null=True, related_name="proprietario")


	forma_aquisicao = models.ForeignKey(FormaAquisicao, verbose_name="Forma de aquisição", help_text="Forma de aquisição.", blank=True, null=True)
	data_aquisicao = models.ForeignKey(DataFormatada, verbose_name="Data de aquisição", help_text="Data de aquisição da peça.", blank=True, null=True, related_name="data_aquisicao")
	#data_aquisicao = models.DateField(help_text="Data de aquisição da peça, seguindo o formato dd/mm/aaaa.", blank=True, null=True)

	numero_processo = models.CharField(max_length=200, verbose_name="Número do processo",  help_text="Número do processo (200 caracteres, no máximo).", blank=True, null=True)

	# Alternativa para 'fornecedor'.
	provisor = models.ForeignKey(Provisor, help_text="Provisor da peça.", blank=True, null=True)

	moeda = models.ForeignKey(TipoMoeda, verbose_name="Tipo da moeda", help_text="Tipo da Moeda (real, cruzeiro, dolar etc.).", blank=True, null=True)
	valor_aquisicao = models.DecimalField(verbose_name="Valor de aquisição", max_digits=10, default=Decimal('0.00'), decimal_places=2, help_text="Valor de aquisição da peça, utilizando ponto em vez de vírgula (por ex.: 549.99).", blank=True, null=True)
	valor_seguro = models.DecimalField(verbose_name="Valor do seguro", max_digits=10, default=Decimal('0.00'), decimal_places=2, help_text="Valor do seguro da peça, utilizando ponto em vez de vírgula (por ex.: 100.00).", blank=True, null=True)

	ex_proprietario = models.ForeignKey(ExProprietario, verbose_name="Ex-proprietário", help_text="Ex proprietário da peça.", blank=True, null=True)

	funcionario = models.ForeignKey(User, editable=False, verbose_name="Funcionário", help_text="Funcionário responsável pelo cadastro da peça.", blank=True, null=True)
	data_cadastro = models.DateField(auto_now=True, verbose_name="Data do cadastro", help_text="Data do cadastro da peça, seguindo o formato dd/mm/aaaa.", blank=True, null=True)

	fonte_original = models.ForeignKey(FonteOriginal, verbose_name="Fonte Original", help_text="Fonte original da peça.", blank=True, null=True)

	# Informações físicas

	numero_partes = models.IntegerField(verbose_name="Número de partes", help_text="Quantidade de partes da peça (apenas números).",  blank=True, null=True)
	material = models.ForeignKey(Material, help_text="Material em que a peça foi construída.", blank=True, null=True)
	tecnica = models.ForeignKey(Tecnica, verbose_name="Técnica", help_text="Técnica em que a peça foi construída.", blank=True, null=True)
	altura = models.FloatField(help_text="Altura da peça (apenas números, em centímetros).", blank=True, null=True)
	circunferencia = models.FloatField(verbose_name="Circunferência", help_text="Circunferência da peça (apenas números, em centímetros).", blank=True, null=True)
	diametro = models.FloatField(verbose_name="Diâmetro", help_text="Diâmetro da peça (apenas números, em centímetros).", blank=True, null=True)
	comprimento = models.FloatField(help_text="Comprimento da peça (apenas números, em centímetros).", blank=True, null=True)
	largura= models.FloatField(help_text="Largura da peça (apenas números, em centímetros).", blank=True, null=True)
	peso = models.FloatField(help_text="Peso da peça (apenas números, em gramas).", blank=True, null=True)
	profundidade = models.FloatField(help_text="Profundidade da peça (apenas números, em centímetros).", blank=True, null=True)


	palavras_chave = models.CharField(max_length=200, verbose_name="Palavras-chave", help_text="Digite no máximo 5 palavras chave, separadas por vírgula (200 caracteres, no máximo).", blank=True, null=True,)


	def __unicode__(self):
		return self.titulo

	class Meta:
		verbose_name = "Peça"
		verbose_name_plural = "Peças"

	def gerar_relatorio(self):
		return "<a href='%s'>Gerar Relatório</a>" %("/gerenciamento/relatorio/%d/" %(self.pk))

	gerar_relatorio.allow_tags = True

	def imagens(self):
		return Imagem.objects.filter(peca=self)

	def videos(self):
		return Video.objects.filter(peca=self)

	def audios(self):
		return Audio.objects.filter(peca=self)

	def documentos(self):
		return Documento.objects.filter(peca=self)

	def autores_texto(self):
		lista_autores = ''
		for a in self.autores.all():
			lista_autores += a.nome + ', '
		return lista_autores[:-2:1]

	def data_cadastro_texto(self):

		return self.data_cadastro.strftime("%d/%m/%Y")

	def outros_numeros(self):

		return OutroNumero.objects.filter(peca=self)

	def inscricoes(self):

		return Inscricao.objects.filter(peca=self)

	def intervencoes(self):

		return Intervencao.objects.filter(peca=self)

	def historicos_movimentacao(self):

		return HistoricoMovimentacao.objects.filter(peca=self)

	def historicos_conservacao(self):

		return HistoricoConservacao.objects.filter(peca=self)

def validar_formato_imagem(value):
	if not (value.name.lower().endswith('.jpg') or value.name.lower().endswith('.jpeg') or value.name.lower().endswith('.png') or value.name.lower().endswith('.bmp') or  value.name.lower().endswith('.gif')):
		raise ValidationError(u'Formato não suportado. Por favor, envie um arquivo no formato .jpg, .jpeg, .png., .bmp ou .gif.')

class Imagem(models.Model):
	peca = models.ForeignKey(Peca)
	autor = models.ForeignKey(Autor, help_text="Autor da imagem.", blank=True, null=True)
	data = models.DateField(help_text="Data que a imagem foi criada, seguindo o formato dd/mm/aaaa.", blank=True, null=True)

	def imagem_dinamica(self, filename):
		try:
			caminho = os.path.join(MEDIA_ROOT, 'imagens', 'pecas', unicode(self.peca.numero_registro))
			lista_imagens = os.listdir(caminho)
			quantidade = len(lista_imagens)/4
			for i in range(1,quantidade+2):
				if not ("imagem%d.png" %i) in lista_imagens:
					return os.path.join("imagens", "pecas", unicode(self.peca.numero_registro), ("imagem%d.png" %i))
					break
		except Exception:
			return os.path.join("imagens", "pecas", unicode(self.peca.numero_registro), "imagem1.png")


	def pequena(self):
		extensao = self.imagem.__unicode__().rsplit('.', 1)[1]
		return self.imagem.__unicode__().replace("." + extensao, '-pequena.png')

	def media(self):
		extensao = self.imagem.__unicode__().rsplit('.', 1)[1]
		return self.imagem.__unicode__().replace("." + extensao, '-media.png')

	def grande(self):
		extensao = self.imagem.__unicode__().rsplit('.', 1)[1]
		return self.imagem.__unicode__().replace("." + extensao, '-grande.png')

	imagem = ImageField(upload_to=imagem_dinamica, max_length=200, help_text="Imagem da peça.", validators=[validar_formato_imagem])


	def __unicode__(self):
		return "Imagem %s" %(unicode(self.id))

	class Meta:
		verbose_name = "Imagem"
		verbose_name_plural = "Imagens"

def validar_formato_audio(value):
	if not (value.name.lower().endswith('.mp3') or value.name.lower().endswith('.wav') or value.name.lower().endswith('.ogg')):
		raise ValidationError(u'Formato não suportado. Por favor, envie um arquivo no formato .mp3, .wav ou .ogg.')

class Audio(models.Model):
	peca = models.ForeignKey(Peca)
	autor = models.ForeignKey(Autor, help_text="Autor do audio.", blank=True, null=True)
	data = models.DateField(help_text="Data que o audio foi feito, seguindo o formato dd/mm/aaaa.", blank=True, null=True)


	def audio_dinamico(self, filename):
		try:
			extensao = filename.split(".")[1]
		except IndexError:
			pass
		try:
			caminho = os.path.join(MEDIA_ROOT, 'audios', 'pecas', unicode(self.peca.numero_registro))
			lista_audios = os.listdir(caminho)
			quantidade = len(lista_audios)
			for i in range(1,quantidade+2):
				if not ("audio%d.%s" %(i, extensao)) in lista_audios:
					return os.path.join("audios", "pecas", unicode(self.peca.numero_registro), ("audio%d.%s" %(i,extensao)))
					break
		except Exception:
			return os.path.join("audios", "pecas", unicode(self.peca.numero_registro), "audio1.%s" %extensao)

	audio = models.FileField(upload_to=audio_dinamico, max_length=200, help_text="Audio da peça.", validators=[validar_formato_audio])

	def __unicode__(self):
		return "Audio de %s" %(unicode(self.peca))

	class Meta:
		verbose_name = "Audio"
		verbose_name_plural = "Audios"

def validar_formato_video(value):
	if not (value.name.lower().endswith('.mp4') or value.name.lower().endswith('.webm') or value.name.lower().endswith('.ogg')):
		raise ValidationError(u'Formato não suportado. Por favor, envie um arquivo no formato .mp4, .webm ou .ogg.')


class Video(models.Model):
	peca = models.ForeignKey(Peca)
	autor = models.ForeignKey(Autor, help_text="Autor do vídeo.", blank=True, null=True)
	data = models.DateField(help_text="Data que o vídeo foi criado, seguindo o formato dd/mm/aaaa.", blank=True, null=True)


	def video_dinamico(self, filename):
		try:
			extensao = filename.split(".")[1]
		except IndexError:
			pass
		try:
			caminho = os.path.join(MEDIA_ROOT, 'videos', 'pecas', unicode(self.peca.numero_registro))
			lista_audios = os.listdir(caminho)
			quantidade = len(lista_audios)
			for i in range(1,quantidade+2):
				if not ("video%d.%s" %(i, extensao)) in lista_audios:
					return os.path.join("videos", "pecas", unicode(self.peca.numero_registro), ("video%d.%s" %(i,extensao)))
					break
		except Exception:
			return os.path.join("videos", "pecas", unicode(self.peca.numero_registro), "video1.%s" %extensao)

	video = models.FileField(upload_to=video_dinamico, max_length=200, help_text="Vídeo da peça.", validators=[validar_formato_video], blank=True, null=True)
	youtube = models.URLField(max_length=200, blank=True, help_text="Ex: //www.youtube.com/embed/umMIcZODm2k", null=True)
	vimeo = models.URLField(max_length=200, blank=True, help_text="Ex: //player.vimeo.com/video/85228844", null=True)

	def normal(self):
		return self.video.__unicode__()

	def __unicode__(self):
		return "Video de %s" %(unicode(self.peca))

	class Meta:
		verbose_name = "Vídeo"
		verbose_name_plural = "Vídeos"

def validar_formato_documento(value):
	if not (value.name.lower().endswith('.pdf')):
		raise ValidationError(u'Formato não suportado. Por favor, envie um arquivo no formato .pdf.')

class OutroNumero(models.Model):
	peca = models.ForeignKey(Peca)
	numero = models.CharField(verbose_name="Número", max_length=20, help_text="Outro número (20 caracteres, no máximo).", blank=False, null=False)
	observacao = models.CharField(verbose_name="Observação", max_length=200, help_text="Descrição sobre este número (200 caracteres, no máximo).", blank=False, null=False)

	def __unicode__(self):
		return self.numero

	class Meta:
		verbose_name = "Outro Número"
		verbose_name_plural = "Outros Números"


# Ver onde esse documento realmente é anexado.
class Documento(models.Model):
	peca = models.ForeignKey(Peca)
	autor = models.ForeignKey(Autor, help_text="Autor do documento.", blank=True, null=True)
	data = models.DateField(help_text="Data que o documento foi criado, seguindo o formato dd/mm/aaaa.", blank=True, null=True)

	def documento_dinamico(self, filename):
		try:
			extensao = filename.split(".")[1]
		except IndexError:
			pass
		try:
			caminho = os.path.join(MEDIA_ROOT, 'documentos', 'pecas', unicode(self.peca.numero_registro))
			lista_audios = os.listdir(caminho)
			quantidade = len(lista_audios)
			for i in range(1,quantidade+2):
				if not ("documento%d.%s" %(i, extensao)) in lista_audios:
					return os.path.join("documentos", "pecas", unicode(self.peca.numero_registro), ("documento%d.%s" %(i,extensao)))
					break
		except Exception:
			return os.path.join("documentos", "pecas", unicode(self.peca.numero_registro), "documento1.%s" %extensao)

	documento = models.FileField(upload_to=documento_dinamico, max_length=200, help_text="Vídeo da peça.", validators=[validar_formato_documento])

	def __unicode__(self):
		return "Documento de %s" %(str(self.peca))

	class Meta:
		verbose_name = "Documento"
		verbose_name_plural = "Documentos"


class EstadoConservacao(models.Model):
	nome = models.CharField(max_length=200, help_text="Nome do estado de conservação (200 caracteres, no máximo).", unique=True)

	def __unicode__(self):
		return self.nome

	class Meta:
		verbose_name = "Estado de Conservação"
		verbose_name_plural = "Estados de Conservação"

class HistoricoConservacao(models.Model):
	peca = models.ForeignKey(Peca, help_text="Peça.")
	data_avaliacao = models.DateTimeField(verbose_name="Data da avaliação", help_text="Data da avaliação, seguindo o formato dd/mm/aaaa.", blank=True, null=True)
	estado_conservacao = models.ForeignKey(EstadoConservacao, verbose_name="Estado de conservação", help_text="Estado de conservação.", blank=True, null=True)
	descricao = models.TextField(verbose_name="Descrição", max_length=200, help_text="Descrição da conservação da peça (200 caracteres, no máximo).", blank=True, null=True)
	funcionario = models.ForeignKey(User, verbose_name="Funcionário", help_text="Funcionário responsável pela avaliação.", blank=True, null=True)

	def __unicode__(self):
		return u'Histórico de ' + unicode(self.peca)

	class Meta:
		unique_together = ('peca','data_avaliacao')
		verbose_name = "Histórico de Conservação"
		verbose_name_plural = "Históricos de Conservação"

class Intervencao(models.Model):
	peca = models.ForeignKey(Peca, help_text="Peça.")
	data_intervencao = models.DateTimeField(verbose_name="Data da intervenção", help_text="Data de intervenção, seguindo o formato dd/mm/aaaa.", blank=True, null=True)
	descricao = models.TextField(verbose_name="Descrição", max_length=200, help_text="Descrição da intervenção (200 caracteres, no máximo).", blank=True, null=True)
	funcionario = models.ForeignKey(User, verbose_name="Funcionário", help_text="Funcionário que realizou a intervenção.", blank=True, null=True)

	def imagem_dinamica(self, filename):
		return os.path.join("imagens", "intervencoes", unicode(self.peca.numero_registro), filename)

	imagem = ImageField(upload_to=imagem_dinamica, max_length=200, help_text="Imagem da intervenção.", null=True, blank=True,validators=[validar_formato_imagem],)


	def __unicode__(self):
		return u'Intervenção %d de ' %(self.id) + unicode(self.peca)

	class Meta:
		unique_together = ('peca','data_intervencao')
		verbose_name = "Intervenção"
		verbose_name_plural = "Intervenções"

class Local(models.Model):
	nome = models.CharField(max_length=200, help_text="Nome do local onde as peças podem estar (200 caracteres, no máximo).",unique=True)

	def __unicode__(self):
		return self.nome

	class Meta:
		verbose_name = "Local"
		verbose_name_plural = "Locais"

class HistoricoMovimentacao(models.Model):
	peca = models.ForeignKey(Peca, help_text="Peça")
	data_alteracao_localizacao = models.DateTimeField(verbose_name="Data da alteração da localização", help_text="Data em que foi alterada a localização da peça, seguindo o formato dd/mm/aaaa.", blank=True, null=True)
	descricao = models.TextField(verbose_name="Descrição", max_length=200, help_text="Descrição acerca da alteração da peça (200 caracteres, no máximo).", blank=True, null=True)
	localizacao_fixa = models.ForeignKey(Local, verbose_name="Localização Fixa", help_text="Localização fixa da peça.", blank=True, null=True, related_name='localizacao_fixa')
	localizacao_atual = models.ForeignKey(Local, verbose_name="Localização atual", help_text="Localização atual da peça.", blank=True, null=True, related_name='localizacao_atual')

	def __unicode__(self):
		return u'Histório de movimentação %d de ' %(self.id) + unicode(self.peca)

	class Meta:
		unique_together = ('peca','data_alteracao_localizacao')
		verbose_name = "Histórico de Movimentação"
		verbose_name_plural = "Históricos de Movimentação"

class TipoInscricao(models.Model):
	nome = models.CharField(max_length=200, help_text="Nome do tipo de inscrição (200 caracteres, no máximo).", unique=True)

	def __unicode__(self):
		return self.nome

	class Meta:
		verbose_name = "Tipo de Inscrição"
		verbose_name_plural = "Tipos de Inscrição"

class Inscricao(models.Model):
	peca = models.ForeignKey(Peca, help_text="Peça.")
	tipo_inscricao = models.ForeignKey(TipoInscricao, verbose_name="Tipo da Inscrição", help_text="Tipo de inscrição.", blank=True, null=True,)
	peca_assinada = models.BooleanField(verbose_name="Peça assinada", help_text="Marque este campo caso a peça tenha sido assinada.", blank=True)

	descricao = models.TextField(max_length=500, help_text="Descrição detalhada da inscrição (500 caracteres, no máximo).", blank=True, null=True)

	def imagem_dinamica(self, filename):
		return os.path.join("imagens", "inscricoes", unicode(self.peca.numero_registro), filename)

	imagem = ImageField(upload_to=imagem_dinamica, max_length=200, help_text="Imagem da inscrição, marca ou legenda.", null=True, blank=True,validators=[validar_formato_imagem],)

	localizacao_assinatura = models.ForeignKey(Local, verbose_name="Localização da assinatura", help_text="Localização fixa da peça.", related_name='+', blank=True, null=True,)

	def __unicode__(self):
		return u'Inscrição %d de ' %(self.id) + unicode(self.peca)

	class Meta:
		verbose_name = "Inscrição"
		verbose_name_plural = "Inscrições"

	def peca_assinada_texto(self):
		if self.peca_assinada:
			return u'Sim'
		else:
			return u'Não'

class InformacoesIPHAN(models.Model):
	peca = models.ForeignKey(Peca, help_text="Peça.")
	memoria_historia = models.TextField(verbose_name="Memória e História", max_length=500, help_text="Memória e história (500 caracteres, no máximo).", blank=True, null=True)
	saberes_fazeres = models.TextField(verbose_name="Saberes e Fazeres",max_length=500, help_text="Saberes e fazeres (500 caracteres, no máximo).", blank=True, null=True)
	celebracoes = models.TextField(verbose_name="Celebrações", max_length=500, help_text="Celebrações (500 caracteres, no máximo).", blank=True, null=True)
	lugares = models.TextField(verbose_name="Lugares", max_length=500, help_text="Lugares (500 caracteres, no máximo).", blank=True, null=True)
	expressoes = models.TextField(verbose_name="Expressões", max_length=500, help_text="Expressões (500 caracteres, no máximo).", blank=True, null=True)

	def __unicode__(self):
		return self.id

	class Meta:
		verbose_name = "Informações do IPHAN"
		verbose_name_plural = "Informações do IPHAN"

def apagar_arquivos_imagem(imagem):

	caminho_imagem = unicode(imagem.path)
	nome_arquivo = caminho_imagem.rsplit("/",1)[1].rsplit(".")[0]
	diretorio = caminho_imagem.rsplit('/', 1)[0]

	try:
		os.remove(caminho_imagem)
	except OSError:
		print u"Não foi possível apagar %s." %(caminho_imagem)

	try:
		os.remove(os.path.join(diretorio, nome_arquivo + "-grande.png"))
	except OSError:
		print u"Não foi possível apagar %s." %(caminho_imagem)
	try:
		os.remove(os.path.join(diretorio, nome_arquivo + "-media.png"))
	except OSError:
		print u"Não foi possível apagar %s." %(caminho_imagem)
	try:
		os.remove(os.path.join(diretorio, nome_arquivo + "-pequena.png"))
	except OSError:
		print u"Não foi possível apagar %s." %(caminho_imagem)

@receiver(signals.pre_save, sender=Imagem)
def editar_imagens(sender, instance, **kwargs):
	try:
		imagem_antiga = Imagem.objects.get(id=instance.id).imagem
		apagar_arquivos_imagem(imagem_antiga)
	except ObjectDoesNotExist:
		pass

@receiver(signals.pre_delete, sender=Imagem)
def apagar_imagens_peca(sender, instance, **kwargs):
	imagem = instance.imagem
	apagar_arquivos_imagem(imagem)


@receiver(signals.post_save, sender=Imagem)
def criar_outras_imagens(sender, instance, **kwargs):

	objeto = instance
	tamanhos = {'pequeno': {'altura': 24, 'largura': 24}, 'medio': {'altura': 300, 'largura': 300}, 'grande': {'altura': 600, 'largura': 600},}

	caminho_imagem = unicode(objeto.imagem.path)


	im = Image.open(caminho_imagem)

	extensao = caminho_imagem.rsplit('.', 1)[1]
	nome_arquivo = caminho_imagem.rsplit("/",1)[1].rsplit(".")[0]
	diretorio = caminho_imagem.rsplit('/', 1)[0]

	if im.mode not in ("L", "RGB"):
		im = im.convert("RGB")

	# Lança uma exceção em caso de imagem em formato desconhecido.
	if extensao not in ['jpg', 'jpeg', 'gif', 'png']:
		sys.exit()

	DEFAULT_COLOR = (255, 255, 255, 0)

	# Criar o tamanho grande.

	im.thumbnail((tamanhos['grande']['largura'], tamanhos['grande']['altura']), Image.ANTIALIAS)

	grande = Image.new("RGBA", (tamanhos['grande']['largura'], tamanhos['grande']['altura']), DEFAULT_COLOR)
	grande.paste(im, ((tamanhos['grande']['largura'] - im.size[0]) / 2, (tamanhos['grande']['altura'] - im.size[1]) / 2))
	grande.save(os.path.join(diretorio, nome_arquivo + "-grande.png"), 'PNG', quality=100)

	# Criar o tamanho medio.


	im.thumbnail((tamanhos['medio']['largura'], tamanhos['medio']['altura']), Image.ANTIALIAS)

	medio = Image.new("RGBA", (tamanhos['medio']['largura'], tamanhos['medio']['altura']), DEFAULT_COLOR)
	medio.paste(im, ((tamanhos['medio']['largura'] - im.size[0]) / 2, (tamanhos['medio']['altura'] - im.size[1]) / 2))
	medio.save(os.path.join(diretorio, nome_arquivo + "-media.png"), 'PNG', quality=100)

	# Criar o icone.

	im.thumbnail((tamanhos['pequeno']['largura'], tamanhos['pequeno']['altura']), Image.ANTIALIAS)

	pequeno = Image.new("RGBA", (tamanhos['pequeno']['largura'], tamanhos['pequeno']['altura']), DEFAULT_COLOR)
	pequeno.paste(im, ((tamanhos['pequeno']['largura'] - im.size[0]) / 2, (tamanhos['pequeno']['altura'] - im.size[1]) / 2))
	pequeno.save(os.path.join(diretorio, nome_arquivo + "-pequena.png"), 'PNG', quality=100)


@receiver(signals.post_save, sender=Inscricao)
def renomear_imagem_inscricao(sender, instance, **kwargs):
	objeto = instance
	try:
		caminho_imagem = unicode(objeto.imagem.path)

		extensao = caminho_imagem.rsplit('.', 1)[1]
		diretorio = caminho_imagem.rsplit('/', 1)[0]

		novo_nome = os.path.join(diretorio,("inscricao%s" %unicode(instance.id)) + ".png")

		if extensao != 'png':
			im = Image.open(caminho_imagem)
			if im.mode not in ("L", "RGB"):
				im = im.convert("RGB")
			im.save(novo_nome, 'PNG', quality=100)
			os.remove(caminho_imagem)
		else:
			os.rename(caminho_imagem, novo_nome)

		nova_imagem = novo_nome.split("/media/")[1]

		if instance.imagem != nova_imagem:
			instance.imagem = nova_imagem
			instance.save()
	except ValueError:
		pass

#@receiver(signals.post_save, sender=Intervencao)
def renomear_imagem_intervencao(sender, instance, **kwargs):
	objeto = instance
	caminho_imagem = unicode(objeto.imagem.path)

	extensao = caminho_imagem.rsplit('.', 1)[1]
	diretorio = caminho_imagem.rsplit('/', 1)[0]

	novo_nome = os.path.join(diretorio,("intervencao%s" %unicode(instance.id)) + ".png")

	if extensao != 'png':
		im = Image.open(caminho_imagem)
		if im.mode not in ("L", "RGB"):
			im = im.convert("RGB")
		im.save(novo_nome, 'PNG', quality=100)
		os.remove(caminho_imagem)
	else:
		os.rename(caminho_imagem, novo_nome)

	nova_imagem = novo_nome.split("/media/")[1]

	if instance.imagem != nova_imagem:
		instance.imagem = nova_imagem
		instance.save()

@receiver(signals.pre_delete, sender=Inscricao)
def apagar_imagem_inscricao(sender, instance, **kwargs):
	imagem = instance.imagem
	apagar_arquivos_imagem(imagem)

@receiver(signals.pre_delete, sender=Intervencao)
def apagar_imagem_intervencoes(sender, instance, **kwargs):
	imagem = instance.imagem
	apagar_arquivos_imagem(imagem)


@receiver(signals.pre_delete, sender=Audio)
def apagar_audio(sender, instance, **kwargs):
	caminho_audio = unicode(instance.audio.path)

	try:
		os.remove(caminho_audio)
	except OSError:
		print u"Não foi possível apagar %s." %(caminho_audio)


@receiver(signals.pre_save, sender=Audio)
def editar_audio(sender, instance, **kwargs):
	try:
		audio_antigo = Audio.objects.get(id=instance.id).audio
		try:
			os.remove(audio_antigo.path)
		except OSError:
			print u"Não foi possível apagar %s." %(audio_antigo.path)
	except ObjectDoesNotExist:
		pass


@receiver(signals.pre_delete, sender=Video)
def apagar_video(sender, instance, **kwargs):
	try:
		caminho_video = unicode(instance.video.path)

		os.remove(caminho_video)
	except:
		pass

@receiver(signals.pre_save, sender=Video)
def editar_video(sender, instance, **kwargs):
	try:
		video_antigo = Video.objects.get(id=instance.id).video
		# try:
		# 	os.remove(video_antigo.path)
		# except:
		# 	print u"Não foi possível apagar %s." %(video_antigo.path)
	except:
		pass


@receiver(signals.pre_delete, sender=Documento)
def apagar_documento(sender, instance, **kwargs):
	caminho_documento = unicode(instance.documento.path)

	try:
		os.remove(caminho_documento)
	except OSError:
		print u"Não foi possível apagar %s." %(caminho_documento)


@receiver(signals.pre_save, sender=Documento)
def editar_documento(sender, instance, **kwargs):
	try:
		documento_antigo = Documento.objects.get(id=instance.id).documento
		try:
			os.remove(documento_antigo.path)
		except OSError:
			print u"Não foi possível apagar %s." %(documento_antigo.path)
	except ObjectDoesNotExist:
		pass