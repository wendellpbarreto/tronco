#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

from .views import View

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='/apresentacao/home/')),

    url(r'^(?P<slug>\w+)$', View.as_view(), name='view',),
    url(r'^(?P<slug>\w+)/search/$', View.as_view(), name='view',),
    url(r'^(?P<slug>\w+)/(?P<section>[\w+\-]*)$', View.as_view(), name='view',),
    url(r'^(?P<slug>\w+)/(?P<pk>\d+)/$', View.as_view(), name='view',),
    url(r'^(?P<slug>\w+)/(?P<pk>\d+)/(?P<slug2>\w+)/(?P<pk2>\d+)/$', View.as_view(), name='view',),
    url(r'^(?P<slug>\w+)/(?P<pk>\d+)/(?P<slug2>\w+)/(?P<pk2>\d+)/(?P<section>[\w+\-]*)$', View.as_view(), name='view',),
    url(r'^(?P<slug>\w+)/(?P<pk>\d+)/search$', View.as_view(), name='view',),

    # url(r'^(?P<slug>\w+)/(?P<pk>.\d+)/$', View.as_view(), name='view',),
    # url(r'^(?P<slug>\w+)/(?P<page>.\d+)/$', View.as_view(), name='view',),
    # url(r'^(?P<slug>\w+)/(?P<pk>.\d+)/(?P<page>.\d+)/$', View.as_view(), name='view',),
    # url(r'^(?P<slug>\w+)/(?P<keywords>.\w+)/$', View.as_view(), name='view',),
    # url(r'^(?P<slug>\w+)/(?P<page>\d+)/(?P<keywords>[A-Za-z0-9_\+]*)/$', View.as_view(), name='view',),

)

# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

# from django.conf.urls.defaults import patterns, url

# urlpatterns = patterns('',
#     url(r'^$', 'apresentacao.views.inicio', name='inicio'),
#     url(r'^inicio/$', 'apresentacao.views.inicio', name='inicio'),
#     url(r'^coletaneas/$', 'apresentacao.views.coletaneas', name='coletaneas'),
    
#     url(r'^institucional/$', 'apresentacao.views.institucional', name='institucional'),
#     url(r'^pesquisar_peca/$', 'apresentacao.views.pesquisar_peca', name="pesquisar_peca"),
    
#     url(r'^mail/$', 'apresentacao.views.mail', name='mail'),  

#     url(r'^search/$', 'apresentacao.views.search', name='search'),   
#     url(r'^search/(?P<keywords>.\w+)/$', 'apresentacao.views.search', name='search'),   
#     url(r'^search/(?P<page>\d+)/(?P<keywords>[A-Za-z0-9_\+]*)/$', 'apresentacao.views.search', name='search'),   

#     # NEW ##
#     url(r'^news/(?P<page>\d+)/$', 'apresentacao.ajax.news', name='news'),
#     url(r'^read_news/(?P<id>\d+)/$', 'apresentacao.ajax.read_news', name='read_news'),

#     url(r'^coletaneas/(?P<pagina>\d+)/(?P<palavra>.*)/$', 'apresentacao.ajax.coletaneas', name='coletaneas'),
#     url(r'^pecas/(?P<coletanea>\d+)/(?P<pagina>\d+)/(?P<palavra>.*)/$', 'apresentacao.ajax.pecas', name='pecas'),

#     url(r'^controle_pecas/(?P<peca>\d+)/(?P<coletanea>\d+)/$', 'apresentacao.ajax.controle_pecas', name='controle_pecas'),
#     url(r'^controle_coletaneas/(?P<coletanea>\d+)/(?P<pagina>\d+)/$', 'apresentacao.ajax.controle_coletaneas', name='controle_coletaneas'),

#     url(r'^imagem/(?P<id>\d+)/(?P<pagina>\d+)/$', 'apresentacao.ajax.imagem', name='imagem'),
#     url(r'^video/(?P<id>\d+)/(?P<pagina>\d+)/$', 'apresentacao.ajax.video', name='video'),
#     url(r'^audio/(?P<id>\d+)/(?P<pagina>\d+)/$', 'apresentacao.ajax.audio', name='audio'),
#     url(r'^documento/(?P<id>\d+)/(?P<pagina>\d+)/$', 'apresentacao.ajax.documento', name='documento'),
#     url(r'^informacoes_iphan/(?P<id>\d+)/(?P<pagina>\d+)/$', 'apresentacao.ajax.informacoes_iphan', name='informacoes_iphan'),
# )
