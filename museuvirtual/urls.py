#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView

# Uncomment the next two lines to enable the admin:

admin.autodiscover()

urlpatterns = patterns('',
    # Redactor
    # url(r'^redactor/', include('redactor.urls')),

    # TinyMCE
    # (r'^tinymce/', include('tinymce.urls')),
    
    url(r'^admin_tools/', include('admin_tools.urls')),

    url(r'^$', RedirectView.as_view(url= '/apresentacao/')),
    url(r'^apresentacao/', include('apresentacao.urls', app_name='apresentacao'), name='apresentacao'), # Pagina inicial/ apresentacao

    url(r'^criacao/', include('criacao.urls', app_name='criacao'), name='criacao'),

    #url(r'^accounts/login/$', 'django.contrib.auth.views.login'),	

    url(r'^accounts/login/$', RedirectView.as_view(url= '/criacao/')),


    url(r'^gerar_relatorios/', 'gerenciamento.views.gerar_relatorios', name='gerar_relatorios'),

    url(r'^media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),


    # Examples:
    # url(r'^$', 'museuvirtual.views.home', name='home'),
    # url(r'^museuvirtual/', include('museuvirtual.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^gerenciamento/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^gerenciamento/', include(admin.site.urls)),

    url(r'^gerenciamento/', include('gerenciamento.urls')),

    # Para o desenvolvimento

    url(r'^preencher/$', 'museuvirtual.views.preencher', name='preencher'),
    	
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()


