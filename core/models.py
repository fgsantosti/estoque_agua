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
        ('paga', 'Paga'),
        ('parcial', 'Pago Parcial'),
        ('cancelada', 'Cancelada')
    ]
    
    numero_venda = models.CharField(max_length=20, unique=True, editable=False)
    cliente = models.ForeignKey('Cliente', on_delete=models.SET_NULL, null=True, blank=True)
    forma_pagamento = models.ForeignKey('FormaPagamento', on_delete=models.SET_NULL, null=True, blank=True)
    data_venda = models.DateTimeField(default=timezone.now)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    observacao = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aberta')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    @property
    def valor_total_pago(self):
        """Soma todos os pagamentos realizados"""
        return sum(p.valor_pago for p in self.pagamentos.all()) or 0
    
    @property
    def valor_pendente(self):
        """Valor que ainda falta pagar"""
        return self.valor_total - self.valor_total_pago
    
    @property
    def percentual_pago(self):
        """Percentual já pago da venda"""
        if self.valor_total > 0:
            return (self.valor_total_pago / self.valor_total) * 100
        return 0
    
    def atualizar_status_pagamento(self):
        """Atualiza status baseado nos pagamentos"""
        valor_pago = self.valor_total_pago
        
        # Se venda foi cancelada, não alterar status
        if self.status == 'cancelada':
            return
            
        if valor_pago == 0:
            # Sem pagamentos - manter como aberta se não foi finalizada
            if self.status not in ['aberta']:
                self.status = 'finalizada'  # Se estava finalizada, manter finalizada
                self.save()
        elif valor_pago >= self.valor_total:
            # Totalmente paga
            if self.status != 'paga':
                self.status = 'paga'
                self.save()
        else:
            # Pagamento parcial
            if self.status != 'parcial':
                self.status = 'parcial'
                self.save()
    
    def save(self, *args, **kwargs):
        if not self.numero_venda:
            # Gerar número sequencial da venda
            # Buscar o maior número existente para evitar duplicatas
            ultimo_registro = Venda.objects.filter(numero_venda__startswith='VD').order_by('numero_venda').last()
            if ultimo_registro:
                # Extrair o número da string e incrementar
                try:
                    ultimo_numero = int(ultimo_registro.numero_venda[2:]) + 1
                except (ValueError, IndexError):
                    ultimo_numero = 1
            else:
                ultimo_numero = 1
            
            # Verificar se já existe para evitar conflitos
            while Venda.objects.filter(numero_venda=f"VD{ultimo_numero:06d}").exists():
                ultimo_numero += 1
                
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


class Pagamento(models.Model):
    """Controla os pagamentos de uma venda - permite múltiplas formas"""
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='pagamentos')
    forma_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.CASCADE)
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2)
    data_pagamento = models.DateTimeField(default=timezone.now)
    observacao = models.TextField(blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-data_pagamento']
        verbose_name = "Pagamento"
        verbose_name_plural = "Pagamentos"
    
    def __str__(self):
        return f"Pagamento {self.forma_pagamento.nome} - R$ {self.valor_pago} - Venda {self.venda.numero_venda}"


class ContasReceber(models.Model):
    """Controla contas a receber de clientes"""
    STATUS_CHOICES = [
        ('aberto', 'Em Aberto'),
        ('parcial', 'Pago Parcial'),
        ('quitado', 'Quitado'),
        ('vencido', 'Vencido')
    ]
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='contas_receber')
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, null=True, blank=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    data_vencimento = models.DateField()
    data_criacao = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aberto')
    observacao = models.TextField(blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    @property
    def valor_pendente(self):
        return self.valor_total - self.valor_pago
    
    @property
    def percentual_pago(self):
        if self.valor_total > 0:
            return (self.valor_pago / self.valor_total) * 100
        return 0
    
    @property
    def esta_vencido(self):
        from datetime import date
        return self.data_vencimento < date.today() and self.status != 'quitado'
    
    def __str__(self):
        return f"Conta {self.cliente.nome} - R$ {self.valor_pendente} pendente"
    
    class Meta:
        verbose_name = "Conta a Receber"
        verbose_name_plural = "Contas a Receber"
        ordering = ['-data_criacao']


class PagamentoConta(models.Model):
    """Pagamentos diretos em contas a receber (para contas avulsas sem venda)"""
    conta_receber = models.ForeignKey(ContasReceber, on_delete=models.CASCADE, related_name='pagamentos_conta')
    forma_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.CASCADE)
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2)
    data_pagamento = models.DateTimeField(default=timezone.now)
    observacao = models.TextField(blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-data_pagamento']
        verbose_name = "Pagamento de Conta"
        verbose_name_plural = "Pagamentos de Contas"
    
    def __str__(self):
        return f"Pagamento {self.forma_pagamento.nome} - R$ {self.valor_pago} - {self.conta_receber.cliente.nome}"
