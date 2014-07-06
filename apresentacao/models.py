#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models

from gerenciamento.models import Peca, Funcionario

class Destinatario(models.Model):
	funcionario = models.ForeignKey(Funcionario, verbose_name='Funcionário', unique=True, help_text='Funcionário que receberá e-mails do formulário de contato do Museu Virtual.')
	
	class Meta:
		verbose_name = 'Destinatário'
		verbose_name_plural = 'Destinatários'
	
	def __unicode__(self):
		return u'%s %s' % (self.funcionario.first_name.capitalize(), self.funcionario.last_name.capitalize())

class Mensagem(models.Model):
	nome_remetente = models.CharField('Nome', max_length=45, help_text='Nome do remetente.')
	telefone = models.CharField('Telefone', max_length=20, help_text='Telefone do remetente.')
	email = models.EmailField('E-mail', max_length=255, help_text='E-mail do remetente')
	descricao = models.TextField('Descrição', max_length=500, help_text='Descrição da mensagem.')

	class Meta:
		verbose_name = 'Mensagem'
		verbose_name_plural = 'Mensagens'

	def __unicode__(self):
		return u'%s' % (self.nome.capitalize())
	
