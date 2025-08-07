from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Categorias"

class Produto(models.Model):
    nome = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=50, unique=True)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2)
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2)
    estoque_minimo = models.IntegerField(default=10)
    estoque_atual = models.IntegerField(default=0)
    unidade_medida = models.CharField(max_length=20, default='UN')
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} - {self.codigo}"

    @property
    def estoque_baixo(self):
        return self.estoque_atual <= self.estoque_minimo

    @property
    def valor_total_estoque(self):
        return self.estoque_atual * self.preco_custo

class MovimentacaoEstoque(models.Model):
    TIPO_CHOICES = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
        ('ajuste', 'Ajuste'),
    ]

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    quantidade = models.IntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    forma_pagamento = models.ForeignKey(
        'FormaPagamento', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        help_text='Forma de pagamento utilizada (apenas para saídas/vendas)'
    )
    observacao = models.TextField(blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_movimentacao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.produto.nome} - {self.tipo} - {self.quantidade}"

    @property
    def valor_total(self):
        if self.preco_unitario:
            return self.quantidade * self.preco_unitario
        return 0

    class Meta:
        verbose_name_plural = "Movimentações de Estoque"
        ordering = ['-data_movimentacao']

class Fornecedor(models.Model):
    nome = models.CharField(max_length=200)
    cnpj = models.CharField(max_length=18, unique=True)
    telefone = models.CharField(max_length=20)
    email = models.EmailField()
    endereco = models.TextField()
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Fornecedores"

class Cliente(models.Model):
    nome = models.CharField(max_length=200)
    cpf_cnpj = models.CharField(max_length=18)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    endereco = models.TextField()
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class FormaPagamento(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)
    prazo_recebimento = models.IntegerField(
        default=0, 
        help_text='Prazo em dias para recebimento (0 = à vista)'
    )
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Forma de Pagamento'
        verbose_name_plural = 'Formas de Pagamento'
        ordering = ['nome']


class Venda(models.Model):
    STATUS_CHOICES = [
        ('aberta', 'Aberta'),
        ('finalizada', 'Finalizada'),
        ('cancelada', 'Cancelada')
    ]
    
    numero_venda = models.CharField(max_length=20, unique=True, editable=False)
    cliente = models.ForeignKey('Cliente', on_delete=models.SET_NULL, null=True, blank=True)
    forma_pagamento = models.ForeignKey('FormaPagamento', on_delete=models.SET_NULL, null=True)
    data_venda = models.DateTimeField(default=timezone.now)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    observacao = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aberta')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.numero_venda:
            # Gerar número sequencial da venda
            ultimo_numero = Venda.objects.count() + 1
            self.numero_venda = f"VD{ultimo_numero:06d}"
        super().save(*args, **kwargs)
    
    @property
    def valor_total(self):
        return sum(item.valor_total for item in self.itens.all())
    
    @property
    def quantidade_total_itens(self):
        return sum(item.quantidade for item in self.itens.all())
    
    @property
    def total_itens(self):
        return self.itens.count()
    
    @property
    def data_vencimento(self):
        """Calcula a data de vencimento baseada no prazo da forma de pagamento"""
        if self.forma_pagamento and self.forma_pagamento.prazo_recebimento > 0:
            from datetime import timedelta
            return self.data_venda.date() + timedelta(days=self.forma_pagamento.prazo_recebimento)
        return self.data_venda.date()
    
    def __str__(self):
        return f"Venda {self.numero_venda}"
    
    class Meta:
        verbose_name_plural = "Vendas"
        ordering = ['-data_venda']


class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey('Produto', on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    @property
    def valor_total(self):
        return self.quantidade * self.preco_unitario
    
    def __str__(self):
        return f"{self.produto.nome} - {self.quantidade}x R${self.preco_unitario}"
    
    class Meta:
        verbose_name = "Item da Venda"
        verbose_name_plural = "Itens da Venda"
