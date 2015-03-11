# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CustomField'
        db.create_table(u'criacao_customfield', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'criacao', ['CustomField'])

        # Adding model 'Link'
        db.create_table(u'criacao_link', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'criacao', ['Link'])

        # Adding model 'Noticia'
        db.create_table(u'criacao_noticia', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('titulo', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('descricao_breve', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('descricao', self.gf('django.db.models.fields.CharField')(max_length=650)),
            ('data_de_criacao', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('imagem', self.gf('sorl.thumbnail.fields.ImageField')(max_length=200, null=True)),
        ))
        db.send_create_signal(u'criacao', ['Noticia'])

        # Adding M2M table for field pecas on 'Noticia'
        m2m_table_name = db.shorten_name(u'criacao_noticia_pecas')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('noticia', models.ForeignKey(orm[u'criacao.noticia'], null=False)),
            ('peca', models.ForeignKey(orm[u'gerenciamento.peca'], null=False))
        ))
        db.create_unique(m2m_table_name, ['noticia_id', 'peca_id'])

        # Adding model 'Coletanea'
        db.create_table(u'criacao_coletanea', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data_criacao', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('descricao', self.gf('django.db.models.fields.TextField')(max_length=500)),
            ('inicio_exposicao', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('fim_exposicao', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('funcionario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('informacoes_iphan', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('informacoes_tecnicas', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('nivel', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'criacao', ['Coletanea'])

        # Adding M2M table for field pecas on 'Coletanea'
        m2m_table_name = db.shorten_name(u'criacao_coletanea_pecas')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('coletanea', models.ForeignKey(orm[u'criacao.coletanea'], null=False)),
            ('peca', models.ForeignKey(orm[u'gerenciamento.peca'], null=False))
        ))
        db.create_unique(m2m_table_name, ['coletanea_id', 'peca_id'])

        # Adding model 'Tema'
        db.create_table(u'criacao_tema', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(unique=True, max_length=45)),
        ))
        db.send_create_signal(u'criacao', ['Tema'])

        # Adding model 'InformacoesMuseu'
        db.create_table(u'criacao_informacoesmuseu', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data', self.gf(u'django_hstore.fields.DictionaryField')()),
        ))
        db.send_create_signal(u'criacao', ['InformacoesMuseu'])


    def backwards(self, orm):
        # Deleting model 'CustomField'
        db.delete_table(u'criacao_customfield')

        # Deleting model 'Link'
        db.delete_table(u'criacao_link')

        # Deleting model 'Noticia'
        db.delete_table(u'criacao_noticia')

        # Removing M2M table for field pecas on 'Noticia'
        db.delete_table(db.shorten_name(u'criacao_noticia_pecas'))

        # Deleting model 'Coletanea'
        db.delete_table(u'criacao_coletanea')

        # Removing M2M table for field pecas on 'Coletanea'
        db.delete_table(db.shorten_name(u'criacao_coletanea_pecas'))

        # Deleting model 'Tema'
        db.delete_table(u'criacao_tema')

        # Deleting model 'InformacoesMuseu'
        db.delete_table(u'criacao_informacoesmuseu')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'criacao.coletanea': {
            'Meta': {'object_name': 'Coletanea'},
            'data_criacao': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'descricao': ('django.db.models.fields.TextField', [], {'max_length': '500'}),
            'fim_exposicao': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'funcionario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'informacoes_iphan': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'informacoes_tecnicas': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'inicio_exposicao': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'nivel': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'pecas': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['gerenciamento.Peca']", 'symmetrical': 'False'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'criacao.customfield': {
            'Meta': {'object_name': 'CustomField'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'criacao.informacoesmuseu': {
            'Meta': {'object_name': 'InformacoesMuseu'},
            'data': (u'django_hstore.fields.DictionaryField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'criacao.link': {
            'Meta': {'object_name': 'Link'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'criacao.noticia': {
            'Meta': {'object_name': 'Noticia'},
            'data_de_criacao': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'descricao': ('django.db.models.fields.CharField', [], {'max_length': '650'}),
            'descricao_breve': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagem': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '200', 'null': 'True'}),
            'pecas': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['gerenciamento.Peca']", 'symmetrical': 'False'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '70'})
        },
        u'criacao.tema': {
            'Meta': {'object_name': 'Tema'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '45'})
        },
        u'gerenciamento.autor': {
            'Meta': {'object_name': 'Autor'},
            'funcao_autor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gerenciamento.FuncaoAutor']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'nome_artistico': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'gerenciamento.categoria': {
            'Meta': {'object_name': 'Categoria'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'gerenciamento.colecao': {
            'Meta': {'object_name': 'Colecao'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'gerenciamento.dataformatada': {
            'Meta': {'object_name': 'DataFormatada'},
            'data_especifica': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'decada_ano': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'periodo': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'seculo': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'})
        },
        u'gerenciamento.exproprietario': {
            'Meta': {'object_name': 'ExProprietario'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'gerenciamento.fonteoriginal': {
            'Meta': {'object_name': 'FonteOriginal'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'gerenciamento.formaaquisicao': {
            'Meta': {'object_name': 'FormaAquisicao'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'gerenciamento.funcaoautor': {
            'Meta': {'object_name': 'FuncaoAutor'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'gerenciamento.material': {
            'Meta': {'object_name': 'Material'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'gerenciamento.objeto': {
            'Meta': {'object_name': 'Objeto'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'gerenciamento.origem': {
            'Meta': {'object_name': 'Origem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'gerenciamento.peca': {
            'Meta': {'object_name': 'Peca'},
            'altura': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'autores': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'autores'", 'symmetrical': 'False', 'to': u"orm['gerenciamento.Autor']"}),
            'categoria': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gerenciamento.Categoria']", 'null': 'True', 'blank': 'True'}),
            'circunferencia': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'colecao': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gerenciamento.Colecao']", 'null': 'True', 'blank': 'True'}),
            'comprimento': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'dados_historicos': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'data_aquisicao': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'data_aquisicao'", 'null': 'True', 'to': u"orm['gerenciamento.DataFormatada']"}),
            'data_cadastro': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'data_criacao': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'data_criacao'", 'to': u"orm['gerenciamento.DataFormatada']"}),
            'descricao': ('django.db.models.fields.TextField', [], {'max_length': '500'}),
            'diametro': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'ex_proprietario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gerenciamento.ExProprietario']", 'null': 'True', 'blank': 'True'}),
            'fonte_original': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gerenciamento.FonteOriginal']", 'null': 'True', 'blank': 'True'}),
            'forma_aquisicao': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gerenciamento.FormaAquisicao']", 'null': 'True', 'blank': 'True'}),
            'funcionario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'iconografia': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'largura': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'material': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gerenciamento.Material']", 'null': 'True', 'blank': 'True'}),
            'moeda': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gerenciamento.TipoMoeda']", 'null': 'True', 'blank': 'True'}),
            'numero_partes': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'numero_processo': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'numero_registro': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'objeto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gerenciamento.Objeto']"}),
            'observacoes': ('django.db.models.fields.TextField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'origem': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gerenciamento.Origem']", 'null': 'True', 'blank': 'True'}),
            'palavras_chave': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'peso': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'procedencia': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gerenciamento.Procedencia']", 'null': 'True', 'blank': 'True'}),
            'profundidade': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'proprietario': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'proprietario'", 'null': 'True', 'to': u"orm['gerenciamento.Proprietario']"}),
            'provisor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gerenciamento.Provisor']", 'null': 'True', 'blank': 'True'}),
            'referencias': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'secao': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gerenciamento.Secao']", 'null': 'True', 'blank': 'True'}),
            'sub_colecao': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gerenciamento.SubColecao']", 'null': 'True', 'blank': 'True'}),
            'tecnica': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gerenciamento.Tecnica']", 'null': 'True', 'blank': 'True'}),
            'texto': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'valor_aquisicao': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'valor_seguro': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'})
        },
        u'gerenciamento.procedencia': {
            'Meta': {'object_name': 'Procedencia'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'gerenciamento.proprietario': {
            'Meta': {'object_name': 'Proprietario'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'gerenciamento.provisor': {
            'Meta': {'object_name': 'Provisor'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'gerenciamento.secao': {
            'Meta': {'object_name': 'Secao'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'gerenciamento.subcolecao': {
            'Meta': {'object_name': 'SubColecao'},
            'colecao': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gerenciamento.Colecao']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'gerenciamento.tecnica': {
            'Meta': {'object_name': 'Tecnica'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'gerenciamento.tipomoeda': {
            'Meta': {'object_name': 'TipoMoeda'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        }
    }

    complete_apps = ['criacao']