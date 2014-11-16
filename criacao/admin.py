#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from criacao.models import Tema, InformacoesMuseu, Coletanea, Noticia
from sorl.thumbnail.admin import AdminImageMixin
from .forms import *


class InformacoesMuseuAdmin(admin.ModelAdmin):
    pass

class TemaAdmin(admin.ModelAdmin):
	pass

class ColetaneaAdmin(admin.ModelAdmin):
	pass

class NoticiaAdmin(AdminImageMixin, admin.ModelAdmin):
	pass


admin.site.register(InformacoesMuseu, InformacoesMuseuAdmin)
admin.site.register(Tema, TemaAdmin)
admin.site.register(Coletanea, ColetaneaAdmin)
admin.site.register(Noticia, NoticiaAdmin)