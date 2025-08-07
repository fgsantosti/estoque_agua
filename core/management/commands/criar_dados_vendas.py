from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import (
    Categoria, Produto, Cliente, FormaPagamento, 
    Venda, ItemVenda, MovimentacaoEstoque
)
from django.utils import timezone
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Cria dados de exemplo para vendas'

    def handle(self, *args, **options):
        self.stdout.write('Criando dados de exemplo para vendas...')
        
        # Buscar usuário admin
        try:
            admin_user = User.objects.get(is_superuser=True)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('Usuário admin não encontrado. Execute: python manage.py createsuperuser'))
            return
        
        # Verificar se já existem categorias e produtos
        if not Categoria.objects.exists():
            self.stdout.write('Criando categorias...')
            categorias = [
                {'nome': 'Água Mineral', 'descricao': 'Águas minerais em diversos tamanhos'},
                {'nome': 'Galão', 'descricao': 'Galões de 20 litros'},
                {'nome': 'Copos Descartáveis', 'descricao': 'Copos plásticos descartáveis'},
            ]
            
            for cat_data in categorias:
                Categoria.objects.get_or_create(**cat_data)
        
        # Verificar se já existem produtos
        if not Produto.objects.exists():
            self.stdout.write('Criando produtos...')
            categoria_agua = Categoria.objects.get(nome='Água Mineral')
            categoria_galao = Categoria.objects.get(nome='Galão')
            categoria_copos = Categoria.objects.get(nome='Copos Descartáveis')
            
            produtos = [
                {
                    'nome': 'Água Mineral 500ml',
                    'categoria': categoria_agua,
                    'codigo': 'AGUA-500ML',
                    'preco_venda': Decimal('2.50'),
                    'preco_custo': Decimal('1.20'),
                    'estoque_minimo': 50,
                    'estoque_atual': 200,
                    'unidade_medida': 'UN'
                },
                {
                    'nome': 'Água Mineral 1,5L',
                    'categoria': categoria_agua,
                    'codigo': 'AGUA-1500ML',
                    'preco_venda': Decimal('4.00'),
                    'preco_custo': Decimal('2.00'),
                    'estoque_minimo': 30,
                    'estoque_atual': 150,
                    'unidade_medida': 'UN'
                },
                {
                    'nome': 'Galão 20L',
                    'categoria': categoria_galao,
                    'codigo': 'GALAO-20L',
                    'preco_venda': Decimal('15.00'),
                    'preco_custo': Decimal('8.00'),
                    'estoque_minimo': 20,
                    'estoque_atual': 80,
                    'unidade_medida': 'UN'
                },
                {
                    'nome': 'Copos 200ml (Pacote 100un)',
                    'categoria': categoria_copos,
                    'codigo': 'COPO-200ML',
                    'preco_venda': Decimal('12.00'),
                    'preco_custo': Decimal('6.00'),
                    'estoque_minimo': 10,
                    'estoque_atual': 50,
                    'unidade_medida': 'PCT'
                }
            ]
            
            for prod_data in produtos:
                Produto.objects.get_or_create(
                    codigo=prod_data['codigo'],
                    defaults=prod_data
                )
        
        # Criar clientes de exemplo
        if not Cliente.objects.exists():
            self.stdout.write('Criando clientes...')
            clientes = [
                {
                    'nome': 'João Silva',
                    'cpf_cnpj': '123.456.789-00',
                    'telefone': '(11) 99999-9999',
                    'email': 'joao@email.com',
                    'endereco': 'Rua A, 123'
                },
                {
                    'nome': 'Maria Santos',
                    'cpf_cnpj': '987.654.321-00',
                    'telefone': '(11) 88888-8888',
                    'email': 'maria@email.com',
                    'endereco': 'Rua B, 456'
                },
                {
                    'nome': 'Pedro Oliveira',
                    'cpf_cnpj': '456.789.123-00',
                    'telefone': '(11) 77777-7777',
                    'email': 'pedro@email.com',
                    'endereco': 'Rua C, 789'
                }
            ]
            
            for cliente_data in clientes:
                Cliente.objects.get_or_create(
                    cpf_cnpj=cliente_data['cpf_cnpj'],
                    defaults=cliente_data
                )
        
        # Criar formas de pagamento
        if not FormaPagamento.objects.exists():
            self.stdout.write('Criando formas de pagamento...')
            formas_pagamento = [
                {'nome': 'Dinheiro', 'prazo_recebimento': 0},
                {'nome': 'Cartão de Débito', 'prazo_recebimento': 0},
                {'nome': 'Cartão de Crédito', 'prazo_recebimento': 30},
                {'nome': 'PIX', 'prazo_recebimento': 0},
            ]
            
            for forma_data in formas_pagamento:
                FormaPagamento.objects.get_or_create(
                    nome=forma_data['nome'],
                    defaults=forma_data
                )
        
        # Criar vendas de exemplo
        self.stdout.write('Criando vendas de exemplo...')
        
        produtos = list(Produto.objects.all())
        clientes = list(Cliente.objects.all())
        formas_pagamento = list(FormaPagamento.objects.all())
        
        # Criar 10 vendas de exemplo
        for i in range(10):
            # Data aleatória nos últimos 30 dias
            dias_atras = random.randint(0, 30)
            data_venda = timezone.now() - timezone.timedelta(days=dias_atras)
            
            venda = Venda.objects.create(
                cliente=random.choice(clientes) if random.random() > 0.3 else None,
                forma_pagamento=random.choice(formas_pagamento),
                data_venda=data_venda,
                usuario=admin_user,
                observacao=f'Venda de exemplo #{i+1}',
                status='finalizada'
            )
            
            # Adicionar 1-4 itens aleatórios à venda
            num_itens = random.randint(1, 4)
            produtos_selecionados = random.sample(produtos, num_itens)
            
            for produto in produtos_selecionados:
                quantidade = random.randint(1, 5)
                
                # Verificar se há estoque suficiente
                if produto.estoque_atual >= quantidade:
                    ItemVenda.objects.create(
                        venda=venda,
                        produto=produto,
                        quantidade=quantidade,
                        preco_unitario=produto.preco_venda
                    )
                    
                    # Atualizar estoque
                    produto.estoque_atual -= quantidade
                    produto.save()
                    
                    # Criar movimentação de estoque
                    MovimentacaoEstoque.objects.create(
                        produto=produto,
                        tipo='saida',
                        quantidade=quantidade,
                        preco_unitario=produto.preco_venda,
                        forma_pagamento=venda.forma_pagamento,
                        observacao=f'Venda {venda.numero_venda}',
                        usuario=admin_user,
                        data_movimentacao=data_venda
                    )
        
        vendas_criadas = Venda.objects.count()
        self.stdout.write(
            self.style.SUCCESS(
                f'Dados de exemplo criados com sucesso! '
                f'{vendas_criadas} vendas foram geradas.'
            )
        )
