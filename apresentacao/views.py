#!/usr/bin/python
# -*- coding: utf-8 -*-

from .generic_view import GenericView

from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.validators import email_re
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q

from .forms import ContactForm

from apresentacao.models import (
    Mensagem,
    Destinatario,
)
from criacao.models import (
    InformacoesMuseu,
    Coletanea,
    Noticia,
    Link,
)
from gerenciamento.models import (
    Peca,
    InformacoesIPHAN,
)

class View(GenericView):

    def home(self, request):
        data = None
        contact_form = ContactForm()
        links = Link.objects.all()

        try:
            informations = InformacoesMuseu.objects.all()[0]
        except Exception, e:
            informations = None

        try:
            news = Noticia.objects.order_by('data_de_criacao')[:4]
        except:
            news = None

        try:
            main_collectanea = Coletanea.objects.filter(nivel=0)[0]
            main_parts = main_collectanea.pecas.all().order_by('?')[:5]
        except Exception, e:
            main_collectanea = None

        try:
            collectaneas = Coletanea.objects.filter(nivel=1)[:5]
        except:
            collectaneas = None

        data = {
            'template': {
                'links': links,
                'informations': informations,
                'news': news,
                'main_collectanea': main_collectanea,
                'main_parts': main_parts,
                'collectaneas': collectaneas,
            }
        }

        return data

    def collectaneas(self, request):
        data = None
        links = Link.objects.all()

        try:
            informations = InformacoesMuseu.objects.all()[0]
        except Exception, e:
            informations = None

        try:
            keywords = request.GET['keywords'].split()
            collectaneas = Coletanea.objects.filter(reduce(lambda x, y: x | y, [Q(nome__icontains=unicode(keyword)) for keyword in keywords])).order_by('-data_criacao')
        except Exception, e:
            # logger.info(str(e))

            collectaneas = Coletanea.objects.all().order_by('-data_criacao')

        data = {
            'template': {
                'links': links,
                'informations': informations,
                'collectaneas': collectaneas,
            }
        }

        return data

    def collectanea(self, request):
        data = None
        links = Link.objects.all()

        try:
            informations = InformacoesMuseu.objects.all()[0]
        except Exception, e:
            informations = None

        try:
            pk = self.kwargs['pk']
            collectanea = Coletanea.objects.get(pk=pk)
        except Exception, e:
            # logger.info(str(e))

            collectanea = Coletanea.objects.all()[0]

        try:
            keywords = request.GET['keywords'].split()
            parts = collectanea.pecas.filter(reduce(lambda x, y: x | y, [Q(titulo__icontains=unicode(keyword)) for keyword in keywords])).order_by('-data_criacao')
        except Exception, e:
            parts = collectanea.pecas.all()

        data = {
            'template': {
                'links': links,
                'informations': informations,
                'collectanea': collectanea,
                'parts': parts,
            }
        }

        return data

    def part(self, request):
        data = None
        sections = ['photos', 'videos', 'audios', 'documents', 'iphan-informations']
        links = Link.objects.all()

        try:
            informations = InformacoesMuseu.objects.all()[0]
        except Exception, e:
            informations = None

        try:
            section = self.kwargs['section']
        except Exception, e:
            # logger.info(str(e))

            section = 'photos'
        else:
            if not section in sections:
                section = 'photos'


        try:
            pk = self.kwargs['pk']
            part = Peca.objects.get(pk=pk)
        except Exception, e:
            # logger.info(str(e))

            part = None
        else:
            part.iphan_informations = InformacoesIPHAN.objects.filter(peca=part)

        try:
            pk2 = self.kwargs['pk2']
            collectanea = Coletanea.objects.get(pk=pk2)
        except Exception, e:
            # logger.info(str(e))

            collectanea = Coletanea.objects.all()[0]

        data = {
            'template': {
                'links': links,
                'informations': informations,
                'section': section,
                'collectanea': collectanea,
                'part': part,
            }
        }

        return data

    def institutional(self, request):
        data = None
        sections = ['who-we-are', 'conception', 'mission', 'goals', 'technical-description', 'acquis-characteristics']
        links = Link.objects.all()

        try:
            informations = InformacoesMuseu.objects.all()[0]
        except Exception, e:
            informations = None

        try:
            section = self.kwargs['section']
        except Exception, e:
            # logger.info(str(e))

            section = 'who-we-are'
        else:
            if not section in sections:
                section = 'who-we-are'

        data = {
            'template': {
                'links': links,
                'informations': informations,
                'section': section,
            }
        }

        return data

    def news(self, request):
        data = None
        links = Link.objects.all()

        try:
            informations = InformacoesMuseu.objects.all()[0]
        except Exception, e:
            informations = None

        try:
            news = Noticia.objects.order_by('-data_de_criacao')
        except:
            news = None

        data = {
            'template': {
                'links': links,
                'informations': informations,
                'news': news,
            }
        }

        return data

    def new(self, request):
        data = None
        links = Link.objects.all()

        try:
            informations = InformacoesMuseu.objects.all()[0]
        except Exception, e:
            informations = None

        try:
            pk = self.kwargs['pk']
            new = Noticia.objects.get(pk=pk)
        except Exception, e:
            # logger.info(str(e))

            new = Noticia.objects.all()[0]

        data = {
            'template': {
                'links': links,
                'informations': informations,
                'new': new,
            }
        }

        return data

    def contact(self, request):
        data = None
        links = Link.objects.all()
        contact_form = ContactForm()

        try:
            informations = InformacoesMuseu.objects.all()[0]
        except Exception, e:
            informations = None

        data = {
            'template': {
                'links': links,
                'informations': informations,
                'contact_form': contact_form,
            }
        }

        return data

    def mail(self, request):
        data = None

        try:
            name = request.POST['name']
            email = request.POST['email']
            message = request.POST['message']
        except Exception, e:
            # logger.error(str(e))

            response = 'Todos os campos são obrigatórios, por favor, preencha-os.'
        else:
            if not (name or email or message):
                response = 'Todos os campos são obrigatórios, por favor, preencha-os.'
            elif not (email_re.match(email)):
                response = 'O email não está no formato correto.'
            else:
                receivers = []

                for receiver in Destinatario.objects.all():
                    receivers.append(receiver.funcionario.email)

                if receivers:
                    email = EmailMessage(
                        subject='Contato MuseuVirtual [%s]' % (email),
                        from_email=email,
                        to=receivers,
                        body=message
                    )
                    email.send()
                    response = 'Mensagem enviada com sucesso!'
                else:
                    response = 'Mensagem enviada com sucesso!'
        finally:
            data = {
                'leftover': {
                    'alert-success': response,
                }
            }

            return data

