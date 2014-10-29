#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from gerenciamento.models import *
from django.core.files import File

class ImagemTestCase(TestCase):
	def setUp(self):
		objeto = Objeto.objects.create(nome="Objeto")
		autor = Autor.objects.create(nome="Autor")
		data_criacao = DataFormatada.objects.create()
		peca = Peca.objects.create(
				titulo="Titulo",
				descricao="Descricao",
				objeto=objeto,
				data_criacao=data_criacao
			)
		fotogaleria = Fotogaleria.objects.create(titulo="Titulo")

	def test_creation_imagem_peca(self):
		imagem = ImagemPeca.objects.create(
			peca=Peca.objects.all()[0],
			imagem="imagens/pecas/03/imagem1-grande.png"
			)
		self.assertEqual(ImagemPeca.objects.all()[0], imagem)

	def test_creation_imagem_peca(self):
		imagem = ImagemFotogaleria.objects.create(
			peca=Fotogaleria.objects.all()[0],
			imagem="imagens/pecas/03/imagem1-grande.png"
			)
		self.assertEqual(ImagemFotogaleria.objects.all()[0], imagem)