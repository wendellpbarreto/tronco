#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.base import RedirectView

from views import *

urlpatterns = patterns('',
    url(r'^$', 'criacao.views.views.entrar', name='entrar',),
    url(r'^entrar', 'criacao.views.views.entrar', name='entrar'),
    url(r'^inicio', 'criacao.views.views.inicio', name='inicio'),
    url(r'^sair', 'criacao.views.views.sair', name='sair'),

    # informacoes
    url(r'^informacoes/(?P<slug>\w+)/$', login_required(informacoes.InformacoesView.as_view()), name='informacoes',),
    url(r'^informacoes/(?P<slug>\w+)/(?P<key>\d+)/$', login_required(informacoes.InformacoesView.as_view()), name='informacoes',),

    # coletanea
    url(r'^coletanea/(?P<slug>\w+)/$', login_required(coletanea.ColetaneaView.as_view()), name='coletanea',),
    url(r'^coletanea/(?P<slug>\w+)/(?P<key>\d+)/$', login_required(coletanea.ColetaneaView.as_view()), name='coletanea',),

    # noticia
    url(r'^noticia/(?P<slug>\w+)/$', login_required(noticia.NoticiaView.as_view()), name='noticia',),
    url(r'^noticia/(?P<slug>\w+)/(?P<key>\d+)/$', login_required(noticia.NoticiaView.as_view()), name='noticia',), 

    # links
    url(r'^link/(?P<slug>\w+)/$', login_required(link.LinkView.as_view()), name='link',),
    url(r'^link/(?P<slug>\w+)/(?P<key>\d+)/$', login_required(link.LinkView.as_view()), name='link',),
    
    # peca
    url(r'^peca/(?P<slug>\w+)/$', login_required(peca.PecaView.as_view()), name='peca',),
    url(r'^peca/(?P<slug>\w+)/(?P<key>\d+)/$', login_required(peca.PecaView.as_view()), name='peca',),
    url(r'^peca/(?P<slug>\w+)/(?P<key>\d+)/(?P<key2>\d+)/$', login_required(peca.PecaView.as_view()), name='peca',),
)