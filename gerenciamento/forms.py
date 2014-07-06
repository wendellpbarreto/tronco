#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.forms import ModelForm
from gerenciamento.models import Funcionario

class FuncionarioForm(ModelForm):
	
	class Meta:
		model = Funcionario
