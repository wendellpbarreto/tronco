#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User
from gerenciamento.models import * 

from sorl.thumbnail.admin import AdminImageMixin

from autocomplete.widgets import *

from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect

from django.shortcuts import render_to_response
from django.template import RequestContext


class CategoriaAdmin(admin.ModelAdmin):
	list_display = ('nome',)
	search_fields = ('nome',)
	
class FonteOriginalAdmin(admin.ModelAdmin):
	list_display = ('nome',)
	search_fields = ('nome',)

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class InformacoesFuncionaisInline(admin.StackedInline):
	model = InformacoesFuncionais
	can_delete = False
	verbose_name = 'Informações Funcionais'
	verbose_name_plural = 'Informações Funcionais'
	list_display = ('nome','nome_de_usuario', 'cpf', 'funcao')
	search_fields = ('nome','nome_de_usuario')
	list_filter = ('funcao',)

# Define a new User admin
class UserAdmin(UserAdmin):
	inlines = [InformacoesFuncionaisInline]
	verbose_name = 'Funcionário'
	verbose_name_plural = 'Funcionários'
	
class FuncaoAutorAdmin(admin.ModelAdmin):
	list_display = ('nome',)
	search_fields = ('nome',)
	
class AutorAdmin(admin.ModelAdmin):
	list_display = ('nome','nome_artistico','funcao_autor',)
	search_fields = ('nome',)
	list_filter = ('funcao_autor',)
	
class OrigemAdmin(admin.ModelAdmin):
	list_display = ('nome',)
	search_fields = ('nome',)

class ProcedenciaAdmin(admin.ModelAdmin):
	list_display = ('nome',)
	search_fields = ('nome',)
	
class ProprietarioAdmin(admin.ModelAdmin):
	list_display = ('nome',)
	search_fields = ('nome',)
	
class SecaoAdmin(admin.ModelAdmin):
	list_display = ('nome',)
	search_fields = ('nome',)
	
class ColecaoAdmin(admin.ModelAdmin):
	list_display = ('nome',)
	search_fields = ('nome',)
	
class SubColecaoAdmin(admin.ModelAdmin):
	list_display = ('nome','colecao',)
	search_fields = ('nome',)
	
class MaterialAdmin(admin.ModelAdmin):
	list_display = ('nome',)
	search_fields = ('nome',)
	verbose_name = u"Material"
	verbose_name_plural = u"Materiais"
	
class TecnicaAdmin(admin.ModelAdmin):
	list_display = ('nome',)
	search_fields = ('nome',)
	search_fields = ('nome',)
	verbose_name = u"Técnica"
	verbose_name_plural = u"Técnicas"
	
class FormaAquisicaoAdmin(admin.ModelAdmin):
	list_display = ('nome',)
	search_fields = ('nome',)
	model = Imagem
	can_delete = True
	
class ProvisorAdmin(admin.ModelAdmin):
	list_display = ('nome',)
	search_fields = ('nome',)
	
class ExProprietarioAdmin(admin.ModelAdmin):
	list_display = ('nome',)
	search_fields = ('nome',)
	
class CargoAdmin(admin.ModelAdmin):
	list_display = ('nome',)
	search_fields = ('nome',)
	
class EquipeAdmin(admin.ModelAdmin):
	list_display = ('nome',)
	search_fields = ('nome',)

class ImagemInline(AdminImageMixin, admin.TabularInline):
	model = Imagem
	can_delete = True
	verbose_name = 'Imagem'
	verbose_name_plural = 'Imagens'
	extra = 0

class AudioInline(admin.TabularInline):
	model = Audio
	can_delete = True
	verbose_name = 'Audio'
	verbose_name_plural = 'Audios'
	extra = 0

class VideoInline(admin.StackedInline):
	model = Video
	can_delete = True
	verbose_name = 'Vídeo'
	verbose_name_plural = 'Vídeos'
	extra = 0

class OutroNumeroInline(admin.TabularInline):
	model = OutroNumero
	can_delete = True
	verbose_name = 'Outro Número'
	verbose_name_plural = 'Outros Números'
	extra = 0

class DocumentoInline(admin.TabularInline):
	model = Documento
	can_delete = True
	verbose_name = 'Documento'
	verbose_name_plural = 'Documentos'
	extra = 0
	
	
class EstadoConservacaoAdmin(admin.ModelAdmin):
	list_display = ('nome',)
	search_fields = ('nome',)

class ObjetoAdmin(admin.ModelAdmin):
	list_display = ('nome',)
	search_fields = ('nome',)
	
class LocalAdmin(admin.ModelAdmin):
	list_display = ('nome',)
	search_fields = ('nome',)
	
class TipoMoedaAdmin(admin.ModelAdmin):
	list_display = ('nome',)
	search_fields = ('nome',)

	
class TipoInscricaoAdmin(admin.ModelAdmin):
	list_display = ('nome',)
	search_fields = ('nome',)
	
class HistoricoConservacaoInline(admin.TabularInline):
	model = HistoricoConservacao
	can_delete = True
	verbose_name = 'Histórico de Conservação'
	verbose_name_plural = 'Históricos de Conservação'
	extra = 0

class InvervencaoInline(AdminImageMixin, admin.TabularInline):
	model = Intervencao
	can_delete = True
	verbose_name = 'Intervenção'
	verbose_name_plural = 'Intervenções'
	extra = 0

class HistoricoMovimentacaoInline(admin.TabularInline):
	model = HistoricoMovimentacao
	can_delete = True
	verbose_name = 'Histrório da Movimentação'
	verbose_name_plural = 'Históricos da Movimentação'
	extra = 0

class InscricaoInline(AdminImageMixin, admin.TabularInline):
	model = Inscricao
	can_delete = True
	verbose_name = 'Inscrição'
	verbose_name_plural = 'Inscrições'
	extra = 0
	
	
class InformacoesIPHANInline(admin.StackedInline):
	model = InformacoesIPHAN
	can_delete = True
	verbose_name = "Informações do IPHAN"
	verbose_name_plural = "Informações do IPHAN"
	extra = 0


# Lista de filtros

class SecaoListFilter(admin.FieldListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Seção'


class PecaAdmin(AutocompleteModelAdmin):
	
	def todos_os_autores(self, obj):
		lista_autores = '\n'
		for a in obj.autores.all():
			lista_autores += a.nome + ', '
		return lista_autores[:-2:1]

	todos_os_autores.short_description = "Todos os Autores"

	actions = ['gerar_relatorios',]

	def gerar_relatorios(self, request, queryset):
		
		lista_pecas = list(queryset)

		request.session['pecas_relatorio'] = lista_pecas
		
		return render_to_response('admin/gerar_relatorios.html', locals(), context_instance=RequestContext(request))

	gerar_relatorios.short_description = "Gerar relatórios das peças"

	fieldsets = (
        ("Informações Principais", {
        	'description': 'Aqui ficam as informações principais da peça.',
        	'classes': ('wide', 'extrapretty'),
            'fields': ('numero_registro',('secao','colecao','sub_colecao'),('objeto','titulo'),'autores','data_criacao','descricao','categoria'),
        }),

       ("Informações Detalhadas", {
        	'description': 'Aqui ficam as informações mais detalhadas da peça.',
        	'classes': ('wide', 'extrapretty','collapse'),
            'fields': ('iconografia','observacoes','dados_historicos','referencias','texto',('origem','procedencia', 'proprietario'),('forma_aquisicao','numero_processo','provisor'),('moeda','valor_aquisicao','valor_seguro'),('data_aquisicao','ex_proprietario'),('fonte_original','palavras_chave'),),
        }),

       ("Medidas da Peça", {
        	'description': 'Aqui ficam as medidas da peça.',
        	'classes': ('wide', 'extrapretty','collapse'),
            'fields': ('numero_partes','material','tecnica','altura','circunferencia','diametro','comprimento','largura','profundidade','peso'),
        }),


    )
	
	inlines = [
			InscricaoInline,
			OutroNumeroInline, 
			ImagemInline, 
			AudioInline, 
			VideoInline,
			DocumentoInline,			
			HistoricoMovimentacaoInline, 
			HistoricoConservacaoInline, 
			InvervencaoInline,
			#InformacoesIPHANInline,
			]
	list_display = ('numero_registro','titulo', 'objeto','todos_os_autores','data_criacao','gerar_relatorio',)
	search_fields = (
				'numero_registro',
				'titulo',
				'objeto__nome',
				'proprietario__nome',
				'autores__nome',
				'origem__nome',
				'procedencia__nome',
				'secao__nome',
				'colecao__nome',
				'sub_colecao__nome',
				'material__nome',
				'tecnica__nome',
				'provisor__nome',
				'ex_proprietario__nome',
				'funcionario__first_name',
				)
	related_search_fields = { 

                #'objeto': ('nome',),
                'autores': ('nome','nome_artistico',),
                #'proprietario': ('nome',),
                'data_criacao': ('data_especifica','decada_ano','seculo','periodo',),
                'origem': ('nome',),
                #'procedencia': ('nome',),
                #'secao': ('nome',),
                #'colecao': ('nome',),
                #'sub_colecao': ('nome',),
                #'material_tecnica': ('nome',),
                'data_aquisicao': ('data_especifica','decada_ano','seculo','periodo',),
                #'forma_aquisicao': ('nome',),
                #'provisor': ('nome',),
                #'ex_proprietario': ('nome',),
    }
	list_filter = (
				'proprietario',
				'objeto',
				#'titulo',
				'data_criacao',
				'autores',
				'origem',
				'procedencia',
				'secao',
				'colecao',
				'sub_colecao',
				'material',
				'tecnica',
				#'numero_processo',
				'peso',
				'altura',
				'largura',
				'profundidade',
				'comprimento',
				'circunferencia',
				'diametro',
				'data_aquisicao',
				'forma_aquisicao',
				'provisor',
				'valor_aquisicao',
				'valor_seguro',
				'ex_proprietario',
				'funcionario',
				'data_cadastro',
				)

	actions_selection_counter = True

	def save_model(self, request, obj, form, change):
		if not change:
			obj.funcionario = request.user

		super(self.__class__, self).save_model(request, obj, form, change)
	
class DataFormatadaAdmin(admin.ModelAdmin):
	pass
	
admin.site.unregister(User)
admin.site.register(Funcionario, UserAdmin)

admin.site.unregister(Group)
admin.site.register(FuncaoFuncionario, GroupAdmin)
admin.site.register(Objeto, ObjetoAdmin)
admin.site.register(Colecao, ColecaoAdmin)
admin.site.register(SubColecao, SubColecaoAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Tecnica, TecnicaAdmin)
admin.site.register(FormaAquisicao, FormaAquisicaoAdmin )
admin.site.register(Provisor, ProvisorAdmin)
admin.site.register(ExProprietario, ExProprietarioAdmin)
admin.site.register(Cargo, CargoAdmin)
admin.site.register(Equipe, EquipeAdmin)
admin.site.register(Proprietario, ProprietarioAdmin)
admin.site.register(Autor, AutorAdmin)
admin.site.register(FuncaoAutor, FuncaoAutorAdmin)
admin.site.register(Origem, OrigemAdmin)
admin.site.register(Procedencia, ProcedenciaAdmin)
admin.site.register(Secao, SecaoAdmin)

admin.site.register(TipoMoeda, TipoMoedaAdmin)

admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(FonteOriginal, FonteOriginalAdmin)

admin.site.register(Peca, PecaAdmin)
admin.site.register(EstadoConservacao, EstadoConservacaoAdmin)

admin.site.register(Local, LocalAdmin)

admin.site.register(TipoInscricao, TipoInscricaoAdmin)
admin.site.register(DataFormatada, DataFormatadaAdmin)


