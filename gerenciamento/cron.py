#!/usr/bin/python
# -*- coding: utf-8 -*-

import kronos
from museuvirtual import settings
from criacao.models import Coletanea
from django.utils import timezone
import datetime

@kronos.register('0 0 * * *') # Toos os dias, à meia noite, o programa é executado.
def complain():
    agora =  timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone())
    todas_coletaneas = Coletanea.objects.all()
    
    for coletanea in todas_coletaneas:
        try:
            if agora >= coletanea.inicio_exposicao and agora < coletanea.fim_exposicao:
                print "Iniciando exposição da coletanea %d" %coletanea.id
                coletanea.status = True
            else:
                print "Encerrando exposição da coletanea %d" %coletanea.id
                coletanea.status = False
            coletanea.save()
        except TypeError:
            print "Coletânea %d sem data." %coletanea.id
            coletanea.status = False
            coletanea.save()