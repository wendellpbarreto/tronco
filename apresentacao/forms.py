#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms

class ContactForm(forms.Form):
	name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nome', 'class': 'teste'}), max_length=100, label = u'')	
	email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email','class': 'teste'}), max_length=100, label = u'')	
	message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Mensagem', 'class': 'testemen'}), max_length=100, label = u'')	
