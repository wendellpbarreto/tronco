#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'relatorio/(?P<peca_id>\d+)/$', 'gerenciamento.views.relatorio', name='relatorio'),
    url(r'gerar_relatorios/$', 'gerenciamento.views.gerar_relatorios', name='gerar_relatorios'),
)
