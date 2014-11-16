#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms
# from redactor.widgets import RedactorEditor

from .models import *
from gerenciamento.models import Peca

class ColetaneaForm(forms.Form):
	CHOICES  =  [
		(True,'Sim'),
        (False,'Não')
    ]

	nome = forms.CharField(widget = forms.TextInput(attrs={'placeholder': 'Nome da coletânea'}), max_length = 100, label = u'')
	descricao = forms.CharField(widget = forms.Textarea(attrs={'placeholder': 'Descrição'}), max_length = 500, label = u'')
	inicio_exposicao = forms.DateField(widget = forms.DateInput(attrs={'placeholder': 'Data de início da exposição'}))
	fim_exposicao = forms.DateField(widget = forms.DateInput(attrs={'placeholder': 'Data de término da exposição'}))
	informacoes_iphan = forms.ChoiceField(choices = CHOICES, widget = forms.RadioSelect(), initial = False)
	informacoes_tecnicas = forms.ChoiceField(choices = CHOICES, widget = forms.RadioSelect(), initial = False)

class NoticiaForm(forms.Form):
	titulo = forms.CharField(widget = forms.TextInput(), max_length = 70, label = u'')
	descricao_breve = forms.CharField(widget = forms.Textarea(attrs = {'maxlength':'140'}), max_length = 140, label = u'')
	descricao = forms.CharField(widget = forms.Textarea(attrs = {'maxlength':'650'}), max_length = 650, label = u'')

class CustomFieldForm(forms.Form):
    name = forms.CharField(widget = forms.TextInput(), max_length = 70, label = u'')

class PecaForm(forms.ModelForm):
	class Meta:
		model = Peca

class LinkForm(forms.ModelForm):
	class Meta:
		model = Link