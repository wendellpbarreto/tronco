#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

from .generic import *

from criacao.forms import *
from criacao.models import *
from gerenciamento.models import *
from .views import UTIL_informacoes_museu

class CustomFieldView(GenericView):

    def create(self, request):

        if request.method == 'POST':
            try:
                name = request.POST['name']
            except Exception, e:
                logger.error(str(e))

                data = {
                    'leftover' : {
                        'alert-error' : 'Está faltando alguma informação, por favor, verifique os campos!',
                    }
                }
            else:
                custom_field = CustomField(name=name)
                informacoes = InformacoesMuseu.objects.all()[0]
                informacoes.data[name] = ''
                informacoes.save()
                try:
                    custom_field.save()
                except Exception, e:
                    logger.error(str(e))

                data = {
                    'leftover' : {
                        'alert-success' : 'Campo dinâmico criado com sucesso!',
                        'redirect' : '/criacao/configurations/'
                    },
                }
            finally:
                return data
        else:
            museu, museu_nome = UTIL_informacoes_museu()
            form = CustomFieldForm()
            data = {
                'template' : {
                    'request' : request,
                    'museu_nome' : museu_nome,
                    'form' : form,
                },
            }

            return data


    def edit(self, request):

        if request.method == 'POST':
            try:
                pk = self.kwargs['key']
                name = request.POST['name']
            except Exception, e:
                logger.error(str(e))

                data = {
                    'leftover' : {
                        'alert-error' : 'Não foi possível processar esta edição!',
                    }
                }
            else:
                custom_field = CustomField.objects.get(pk=pk);

                custom_field.name=name
                custom_field.save()

                data = {
                    'leftover' : {
                        'alert-success' : 'Campo dinâmico editada com sucesso!',
                        'redirect' : '/criacao/configurations/'
                    },
                }
            finally:
                return data
        else:
            try:
                pk = self.kwargs['key']
            except Exception, e:
                logger.error(str(e))

                data = {
                    'leftover' : {
                        'alert-error' : 'Não foi possível processar essa edição!',
                    }
                }
            else:
                museu, museu_nome = UTIL_informacoes_museu()

                custom_field = CustomField.objects.get(pk=pk);

                form = CustomFieldForm(initial={
                    'name': custom_field.name,
                })

                data = {
                    'template' : {
                        'request' : request,
                        'museu_nome' : museu_nome,
                        'custom_field' : custom_field,
                        'form' : form,
                    },
                }
            finally:
                return data

    def delete(self, request):
        try:
            pk = self.kwargs['key']
        except Exception, e:
            logger.error(str(e))

            data = {
                'leftover' : {
                    'alert-error' : 'Não foi possível processar essa exclusão!',
                }
            }
        else:
            CustomField.objects.get(pk=pk).delete()

            data = {
                'leftover' : {
                    'alert-success' : 'Campo dinâmico deletada com sucesso!',
                },
            }
        finally:
            return data
