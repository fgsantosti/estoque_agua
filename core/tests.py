from django.test import TestCase
from django.contrib.auth.models import User
from .models import Categoria, Produto, MovimentacaoEstoque

class ProdutoTestCase(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nome='Água')
        self.produto = Produto.objects.create(
            nome='Galão 20L',
            categoria=self.categoria,
            codigo='GAL20L',
            preco_venda=15.00,
            preco_custo=10.00,
            estoque_minimo=10,
            estoque_atual=50
        )

    def test_produto_creation(self):
        self.assertEqual(self.produto.nome, 'Galão 20L')
        self.assertEqual(self.produto.estoque_atual, 50)
        self.assertFalse(self.produto.estoque_baixo)

    def test_estoque_baixo(self):
        self.produto.estoque_atual = 5
        self.produto.save()
        self.assertTrue(self.produto.estoque_baixo)
