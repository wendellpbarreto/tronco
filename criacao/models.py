#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
try:
    from PIL import Image
except ImportError:
    import Image

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models
from django.db.models import signals
from django.dispatch.dispatcher import receiver
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail import ImageField

from gerenciamento.models import (
	Funcionario,
	Peca
)

class Link(models.Model):
	name = models.CharField(_('Name'), max_length=32, help_text=_('Link name'))
	url = models.CharField(_('URL'), max_length=128, help_text=_('Link url'))

	class Meta:
		verbose_name = _('Link')
		verbose_name_plural = _('Links')

	def __unicode__(self):
		return '%s' % (self.name)

class NoticiaManager(models.Manager):

    pass

class Noticia(models.Model):
	titulo = models.CharField(max_length=70, verbose_name='Título', help_text='Título da notícia.')
	descricao_breve = models.CharField(max_length=140, verbose_name='Descrição breve', help_text='Descrição breve da notícia.')
	descricao = models.CharField(max_length=650, verbose_name='Descrição completa', help_text='Descrição da notícia.')
	pecas = models.ManyToManyField(Peca, verbose_name='Peça',)
	data_de_criacao = models.DateField(auto_now_add=True, verbose_name='Data de criação da notícia.', help_text='Data de criação da notícia, seguindo o formato dd/mm/aaaa.')

	objects = NoticiaManager()

	class Meta:
		verbose_name = 'Notícia'
		verbose_name_plural = 'Notícias'

	def __unicode__(self):
		return '%s' % (self.titulo)

	def imagem_dinamica(self, filename):
		return os.path.join('imagens', 'noticias', self.titulo, filename)

	imagem = ImageField(upload_to=imagem_dinamica, verbose_name='Imagem', max_length=200, help_text='Imagem da intervenção.', null=True)

	def imagem_pequena(self):
		extensao = self.imagem.__unicode__().rsplit('.', 1)[1]
		return self.imagem.__unicode__().replace('.' + extensao, '-pequena.png')

	def imagem_media(self):
		extensao = self.imagem.__unicode__().rsplit('.', 1)[1]
		return self.imagem.__unicode__().replace('.' + extensao, '-media.png')

	def imagem_grande(self):
		extensao = self.imagem.__unicode__().rsplit('.', 1)[1]
		return self.imagem.__unicode__().replace('.' + extensao, '-grande.png')

class Coletanea(models.Model):
	data_criacao = models.DateField(verbose_name='Data de criação', auto_now_add=True)
	descricao = models.TextField(verbose_name='Descrição', max_length=500)
	inicio_exposicao = models.DateField(verbose_name='Início da Exposição', help_text='Data em que a exposição terá a exibição iniciada.', blank=True, null=True)
	fim_exposicao = models.DateField(verbose_name='Fim da Exposição', help_text='Data em que a exposição terá a exibição encerrada.', blank=True, null=True)
	funcionario = models.ForeignKey(User, verbose_name='Funcionário', blank=True, null=True)
	informacoes_iphan = models.BooleanField(default=False, verbose_name='Informações do IPHAN')
	informacoes_tecnicas = models.BooleanField(default=False, verbose_name='Informações Técnicas', help_text='Data em que a exposição começará a ser exibida.')
	nivel = models.PositiveIntegerField(default=1, verbose_name='Nível')
	nome = models.CharField(max_length=100, verbose_name='Nome')
	pecas = models.ManyToManyField(Peca, verbose_name='Peças')
	status = models.BooleanField(default=True, verbose_name='Status')

	class Meta:
		verbose_name = 'Coletânea'
		verbose_name_plural = 'Coletâneas'

	def __unicode__(self):
		return '%s' % (self.nome)

class Tema(models.Model):
	nome = models.CharField(max_length=45, verbose_name='Nome', unique=True)

	class Meta:
		verbose_name = 'Tema'
		verbose_name_plural = 'Temas'

	def __unicode__(self):
		return '%s' % (self.nome)


class InformacoesMuseu(models.Model):
	nome = models.CharField(verbose_name='Nome', max_length=100, blank=True)
	data_fundacao = models.DateField(verbose_name='Data de Fundação', blank=True)
	apresentacao = models.CharField(verbose_name='Apresentação', max_length=1000, blank=True)
	concepcao = models.CharField(verbose_name='Concepção', max_length=1000, blank=True)
	missao = models.CharField(verbose_name='Missão', max_length=500, blank=True)
	objetivos = models.CharField(verbose_name='Objetivos', max_length=500, blank=True)
	descricao_tecnica = models.CharField(verbose_name='Descrição Técnica', max_length=500, blank=True)
	caracteristicas_acervo = models.CharField(verbose_name='Características do Acervo', max_length=500, blank=True)
	tema = models.ForeignKey(Tema, blank=True, null=True, verbose_name='Tema')

	class Meta:
		verbose_name = 'Informação do Museu'
		verbose_name_plural = 'Informações do Museu'

	def __unicode__(self):
		return '%s' % (self.nome)

@receiver(signals.post_save, sender=Noticia)
def renomear_imagem_noticia(sender, instance, **kwargs):
	objeto = instance
	caminho_imagem = unicode(objeto.imagem.path)

	extensao = caminho_imagem.rsplit('.', 1)[1]
	diretorio = caminho_imagem.rsplit('/', 1)[0]

	novo_nome = os.path.join(diretorio,('noticia%s' % str(instance.id)) + '.png')

	if extensao != 'png':
		im = Image.open(caminho_imagem)
		if im.mode not in ('L', 'RGB'):
			im = im.convert('RGB')
		im.save(novo_nome, 'PNG', quality=100)
		os.remove(caminho_imagem)
	else:
		os.rename(caminho_imagem, novo_nome)

	nova_imagem = novo_nome.split('/media/')[1]

	if instance.imagem != nova_imagem:
		instance.imagem = nova_imagem
		instance.save()

@receiver(signals.post_save, sender=Noticia)
def criar_outras_imagens(sender, instance, **kwargs):
	objeto = instance
	tamanhos = {'pequeno': {'altura': 24, 'largura': 24}, 'medio': {'altura': 300, 'largura': 300}, 'grande': {'altura': 600, 'largura': 600},}

	caminho_imagem = str(objeto.imagem.path)

	im = Image.open(caminho_imagem)

	extensao = caminho_imagem.rsplit('.', 1)[1]
	nome_arquivo = caminho_imagem.rsplit('/',1)[1].rsplit('.')[0]
	diretorio = caminho_imagem.rsplit('/', 1)[0]

	if im.mode not in ('L', 'RGB'):
		im = im.convert('RGB')

	# Lança uma exceção em caso de imagem em formato desconhecido.
	if extensao not in ['jpg', 'jpeg', 'gif', 'png']:
		sys.exit()

	DEFAULT_COLOR = (255, 255, 255, 0)

	# Criar o tamanho grande.
	im.thumbnail((tamanhos['grande']['largura'], tamanhos['grande']['altura']), Image.ANTIALIAS)

	grande = Image.new('RGBA', (tamanhos['grande']['largura'], tamanhos['grande']['altura']), DEFAULT_COLOR)
	grande.paste(im, ((tamanhos['grande']['largura'] - im.size[0]) / 2, (tamanhos['grande']['altura'] - im.size[1]) / 2))
	grande.save(os.path.join(diretorio, nome_arquivo + '-grande.png'), 'PNG', quality=100)

	# Criar o tamanho medio.
	im.thumbnail((tamanhos['medio']['largura'], tamanhos['medio']['altura']), Image.ANTIALIAS)

	medio = Image.new('RGBA', (tamanhos['medio']['largura'], tamanhos['medio']['altura']), DEFAULT_COLOR)
	medio.paste(im, ((tamanhos['medio']['largura'] - im.size[0]) / 2, (tamanhos['medio']['altura'] - im.size[1]) / 2))
	medio.save(os.path.join(diretorio, nome_arquivo + '-media.png'), 'PNG', quality=100)

	# Criar o icone.
	im.thumbnail((tamanhos['pequeno']['largura'], tamanhos['pequeno']['altura']), Image.ANTIALIAS)

	pequeno = Image.new('RGBA', (tamanhos['pequeno']['largura'], tamanhos['pequeno']['altura']), DEFAULT_COLOR)
	pequeno.paste(im, ((tamanhos['pequeno']['largura'] - im.size[0]) / 2, (tamanhos['pequeno']['altura'] - im.size[1]) / 2))
	pequeno.save(os.path.join(diretorio, nome_arquivo + '-pequena.png'), 'PNG', quality=100)

