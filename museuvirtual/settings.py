#!/usr/bin/python
# -*- coding: utf-8 -*-

# Django settings for museuvirtual project.

MYSQL_ROOT_PASSWORD = 'p@$$:=dr@w!ng'

DEBUG=True
USE_MYSQL=False
USE_POSTGRESQL=True
TEMPLATE_DEBUG = DEBUG

import os

from django.utils.translation import ugettext_lazy as _

ROOT_URL = 'http://mcc.museuvirtual.info/'

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

USE_THOUSAND_SEPARATOR = True

DEFAULT_CURRENCY_CODE = 'BRL'

if USE_POSTGRESQL:
    DATABASES = {
        'default': {
            'ENGINE':'django.db.backends.postgresql_psycopg2',
            'NAME': 'mcc_db',
            'USER': 'mcc_admin',
            'PASSWORD': 'p@$$:=dr@w!ng=mcc',
            'HOST': 'localhost',
            'PORT': '',
        }
    }
elif USE_MYSQL:
    DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.mysql',   # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
             'NAME': 'mcc_db',                       # Or path to database file if using sqlite3.
             'USER': 'mcc_admin',                    # Not used with sqlite3.
             'PASSWORD': 'p@$$:=dr@w!ng=mcc',        # Not used with sqlite3.
             'HOST': 'localhost',                    # Set to empty string for localhost. Not used with sqlite3.
             'PORT': '18000',                        # Set to empty string for default. Not used with sqlite3.
         }
    }
else:
    DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.sqlite3',            # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
             'NAME': 'museuvirtual.db',                         # Or path to database file if using sqlite3.
         }
    }

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.4/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Fortaleza'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'pt-br'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'museuvirtual', 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"

STATIC_ROOT = os.path.join(PROJECT_PATH, 'museuvirtual', 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # os.path.join(PROJECT_PATH, 'museuvirtual', 'static'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'bf2iz7phco1utf+db!_=w71^&amp;ch8%6km4h4!!bursf2l1dtek8'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'museuvirtual.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'museuvirtual.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'museuvirtual','templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

INSTALLED_APPS = (
    'fluent_dashboard',
    'admin_tools',     # for staticfiles in Django 1.3
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',

    'sorl.thumbnail',
    'kronos',
    'django_social_share',
    'autocomplete',
    'south',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
#    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'apresentacao',
    'criacao',
    'gerenciamento',

)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        # 'logfile': {
        #     'level':'DEBUG',
        #     'class':'logging.handlers.RotatingFileHandler',
        #     'filename': PROJECT_DIR.child('logs') + '/django.log',
        #     'maxBytes': 50000,
        #     'backupCount': 2,
        #     'formatter': 'standard',
        # },
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers':['console'],
            'propagate': True,
            'level':'WARN',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'criacao': {
            # 'handlers': ['console', 'logfile'],
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    }
}

EMAIL_HOST = 'mail.museuvirtual.info'
EMAIL_HOST_PASSWORD = '(museuvirtual)'
EMAIL_HOST_USER = 'museuvirtual'
EMAIL_PORT = '465'
EMAIL_SUBJECT_PREFIX = '' # The default is [Django] so you may want to replace it.
EMAIL_USE_TLS = True


DATE_FORMAT = 'd/m/Y'
DATETIME_FORMAT = 'd/m/Y H:i'
TIME_FORMAT = 'H:i'




ADMIN_TOOLS_INDEX_DASHBOARD = 'fluent_dashboard.dashboard.FluentIndexDashboard'
ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'fluent_dashboard.dashboard.FluentAppIndexDashboard'
ADMIN_TOOLS_MENU = 'fluent_dashboard.menu.FluentMenu'


FLUENT_DASHBOARD_ICON_THEME = 'oxygen' #Nome do tema = diretorio static/'nomedotema'

FLUENT_DASHBOARD_APP_ICONS = {

    'apresentacao/destinatario': 'user-identity.png',
    'apresentacao/mensagem': 'view-pim-mail.png',
    'apresentacao/noticia': 'view-pim-news.png',


    'criacao/coletanea': 'folder-image.png',
    'criacao/informacoesmuseu': 'documentation.png',
    'criacao/tema': 'preferences-contact-list.png',
    'criacao/noticia': 'view-pim-news.png',

    'gerenciamento/funcaoautor': 'resource-group.png',
    'gerenciamento/autor': 'meeting-participant.png',
    'gerenciamento/cargo': 'resource-group.png',
    'gerenciamento/colecao': 'view-presentation.png',
    'gerenciamento/equipe': 'system-users.png',
    'gerenciamento/estadoconservacao': 'view-calendar-agenda.png',
    'gerenciamento/peca': 'utilities-file-archiver.png',
    'gerenciamento/exproprietario': 'meeting-participant.png',
    'gerenciamento/formaaquisicao': 'view-form.png',
    'gerenciamento/fornecedor': 'meeting-participant.png',
    'gerenciamento/funcaofuncionario': 'resource-group.png',
    'gerenciamento/historicoconservacao': 'x-office-address-book.png',
    'gerenciamento/historicolocalizacao': 'x-office-address-book.png',
    'gerenciamento/inscricao': 'view-pim-journal.png',
    'gerenciamento/intervencao': 'view-pim-tasks.png',
    'gerenciamento/local': 'go-home.png',
    'gerenciamento/material': 'applications-engineering.png',
    'gerenciamento/tecnica': 'applications-engineering.png',
    'gerenciamento/origem': 'go-home.png',
    'gerenciamento/procedencia': 'go-home.png',
    'gerenciamento/proprietario': 'view-pim-contacts.png',
    'gerenciamento/secao': 'view-calendar-journal.png',
    'gerenciamento/subcolecao': 'view-presentation.png',
    'gerenciamento/tipoinscricao': 'view-pim-journal.png',
    'gerenciamento/dataformatada': 'view-resource-calendar.png',
    'gerenciamento/provisor': 'preferences-contact-list.png',
    'gerenciamento/objeto': 'server-database.png',
    'gerenciamento/tipomoeda': 'wallet-open.png',
    'gerenciamento/categoria': 'folder-image.png',
    'gerenciamento/fonteoriginal': 'view-bank-account.png',


    'auth/group': 'resource-group.png',
    #'auth/user':  'view-media-artist.png',
    'gerenciamento/funcionario':  'view-media-artist.png',

    'cms/page': 'internet-web-browser.png',
    'comments/comment': 'kde-telepathy.png', #'irc-voice.png',
    'dashboardmods/rssdashboardmodule': 'feed-subscribe.png',
    'fluent_blogs/entry': 'view-calendar-journal.png',
    'fluent_pages/pagelayout': 'view-choose.png',
    'fluent_pages/page': 'internet-web-browser.png',
    'ecms_media/file': 'folder.png',
    'fiber/contentitem': 'folder-txt.png',
    'fiber/file': 'folder.png',
    'fiber/image': 'folder-image.png',
    'fiber/page': 'internet-web-browser.png',
    'filer/folder': 'folder.png',
    'form_designer/formdefinition': 'mail-mark-task.png',
    'form_designer/formlog': 'view-calendar-journal.png',
    'google_analytics/analytics': 'view-statistics.png',
    'page/page': 'internet-web-browser.png',
    'media_tree/filenode': 'folder.png',
    'registration/registrationprofile': 'list-add-user.png',
    'sharedcontent/sharedcontent': 'x-office-document.png',
    'sites/site': 'applications-internet.png',
    'snippet/snippet': 'folder-txt.png',
    'tagging/tag': 'feed-subscribe.png',
    'tagging/taggeditem': 'feed-subscribe.png',
    'threadedcomments/threadedcomment': 'kde-telepathy.png', #'irc-voice.png',
    'zinnia/category': 'folder-bookmark.png',
    'zinnia/entry': 'view-calendar-journal.png',
}

FLUENT_DASHBOARD_DEFAULT_ICON = 'unknown.png'

FLUENT_DASHBOARD_DEFAULT_MODULE = 'admin_tools.dashboard.modules.AppList'

CUSTOM_FLUENT_DASHBOARD_DEFAULT_MODULE = 'museuvirtual.tela_gerenciamento.ListaAplicacoes'

# Application grouping:

FLUENT_DASHBOARD_APP_GROUPS = (


    (_(u'Apresentação'), {
        'models': (
            'apresentacao.*',
        ),
    }),


    (_(u'Criação'), {
        'models': (
            'criacao.*',
        ),
    }),

    (_(u'Gerenciamento'), {
        'models': (
            'gerenciamento.models.Peca',
            'gerenciamento.models.Autor',
            'gerenciamento.models.FuncaoAutor',
            'gerenciamento.models.Secao',
            'gerenciamento.models.Colecao',
            'gerenciamento.models.SubColecao',
            'gerenciamento.models.Categoria',
            'gerenciamento.models.Funcionario',
            'gerenciamento.models.FuncaoFuncionario',
            'gerenciamento.models.Cargo',
            'gerenciamento.models.Equipe',
            'gerenciamento.models.Proprietario',
            'gerenciamento.models.ExProprietario',
            'gerenciamento.models.Objeto',
            'gerenciamento.models.EstadoConservacao',
            'gerenciamento.models.Origem',
            'gerenciamento.models.Procedencia',
            'gerenciamento.models.Local',
            'gerenciamento.models.Objeto',
            'gerenciamento.models.TipoMoeda',
            'gerenciamento.models.FormaAquisicao',
            'gerenciamento.models.Provisor',
            'gerenciamento.models.FonteOriginal',
            'gerenciamento.models.Material',
            'gerenciamento.models.Tecnica',
            'gerenciamento.models.TipoInscricao',
            'gerenciamento.models.Data',





        ),

        'module': CUSTOM_FLUENT_DASHBOARD_DEFAULT_MODULE,
    }),


    #(_('Applications'), {
    #    'models': ('*',),
    #    'module': FLUENT_DASHBOARD_DEFAULT_MODULE,
    #    'collapsible': True,
    #
    #}),
)

AUTOCOMPLETE_MEDIA_PREFIX = STATIC_ROOT

KRONOS_PYTHON='/usr/bin/python'
KRONOS_MANAGE=os.path.join(PROJECT_PATH, 'manage.py')
KRONOS_PYTHONPATH=''
KRONOS_POSTFIX=''


# Redactor config

REDACTOR_OPTIONS = {'lang': 'en'}
REDACTOR_UPLOAD = os.path.join(MEDIA_ROOT, 'uploads')
