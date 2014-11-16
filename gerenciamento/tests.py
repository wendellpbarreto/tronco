# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

# """
# This file demonstrates writing tests using the unittest module. These will pass
# when you run "manage.py test".

# Replace this with more appropriate tests for your application.
# """

# from django.test import TestCase
# from gerenciamento.models import *
# from django.core.files import File

# class ImagemTestCase(TestCase):
# 	def setUp(self):
# 		objeto = Objeto.objects.create(nome="Objeto")
# 		autor = Autor.objects.create(nome="Autor")
# 		data_criacao = DataFormatada.objects.create()
# 		peca = Peca.objects.create(
# 				titulo="Titulo",
# 				descricao="Descricao",
# 				objeto=objeto,
# 				data_criacao=data_criacao
# 			)
# 		fotogaleria = Fotogaleria.objects.create(titulo="Titulo")

# 	def test_creation_imagem_peca(self):
# 		imagem = ImagemPeca.objects.create(
# 			peca=Peca.objects.all()[0],
# 			imagem="imagens/pecas/03/imagem1-grande.png"
# 		)
# 		self.assertEqual(ImagemPeca.objects.all()[0], imagem)

# 	def test_creation_imagem_fotogaleria(self):
# 		imagem = ImagemFotogaleria.objects.create(
# 			peca=Fotogaleria.objects.all()[0],
# 			imagem="imagens/pecas/03/imagem1-grande.png"
# 			)
# 		self.assertEqual(ImagemFotogaleria.objects.all()[0], imagem)

# class ObjetoTestCase(TestCase):
# 	def test_creation_objeto(self):
# 		objeto = Objeto.objects.create(nome="Objeto2")
# 		self.assertEqual(Objeto.objects.all()[0], objeto)

# class AutorTestCase(TestCase):
# 	def test_creation_autor(self):
# 		autor = Autor.objects.create(nome="Autor")
# 		self.assertEqual(Autor.objects.all()[0], autor)

# class DataTestCase(TestCase):
# 	def test_creation_data_criacao(self):
# 		data_criacao = DataFormatada.objects.create()
# 		self.assertEqual(DataFormatada.objects.all()[0], data_criacao)

# class PecaTestCase(TestCase):
# 	def test_creation_peca(self):
# 		objeto = Objeto.objects.create(nome="Objeto")
# 		data_criacao = DataFormatada.objects.create()
# 		peca = Peca.objects.create(
# 				titulo="Titulo",
# 				descricao="Descricao",
# 				objeto=Objeto.objects.all()[0],
# 				data_criacao=DataFormatada.objects.all()[0],
# 				numero_registro=1
# 			)
# 		self.assertEqual(Peca.objects.all()[0], peca)


# class VideoTestCase(TestCase):
# 	def setUp(self):
# 		objeto = Objeto.objects.create(nome="Objeto")
# 		autor = Autor.objects.create(nome="Autor")
# 		data_criacao = DataFormatada.objects.create()
# 		peca = Peca.objects.create(
# 				titulo="Titulo",
# 				descricao="Descricao",
# 				objeto=objeto,
# 				data_criacao=data_criacao
# 			)

# 	def test_creation_video(self):
# 		video = Video.objects.create(peca=Peca.objects.all()[0])
# 		self.assertEqual(Video.objects.all()[0], video)