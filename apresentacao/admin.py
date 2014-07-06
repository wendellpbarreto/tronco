#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin

from apresentacao.models import Destinatario, Mensagem 

admin.site.register(Destinatario)
admin.site.register(Mensagem)