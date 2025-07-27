from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Categoria, Produto, Fornecedor, Cliente, MovimentacaoEstoque, FormaPagamento
from django.utils import timezone
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Cria dados de exemplo para o sistema de estoque de água'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Limpa todos os dados existentes antes de criar novos',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Limpando dados existentes...')
            MovimentacaoEstoque.objects.all().delete()
            Produto.objects.all().delete()
            Cliente.objects.all().delete()
            Fornecedor.objects.all().delete()
            FormaPagamento.objects.all().delete()
            Categoria.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write(self.style.WARNING('Dados existentes removidos!'))

        self.stdout.write('Criando dados de exemplo...')

        # Criar superusuário se não existir
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@estoque.com',
                password='admin123',
                first_name='Administrador'
            )
            self.stdout.write(self.style.SUCCESS('Superusuário criado: admin/admin123'))

        # Criar usuário comum
        if not User.objects.filter(username='usuario').exists():
            User.objects.create_user(
                username='usuario',
                email='usuario@estoque.com',
                password='usuario123',
                first_name='Usuário'
            )
            self.stdout.write(self.style.SUCCESS('Usuário criado: usuario/usuario123'))

        # Criar categorias
        categorias_data = [
            {'nome': 'Água Mineral', 'descricao': 'Águas minerais naturais em diversos formatos'},
            {'nome': 'Água Alcalina', 'descricao': 'Águas com pH alcalino para melhor hidratação'},
            {'nome': 'Água com Gás', 'descricao': 'Águas gaseificadas naturalmente ou artificialmente'},
            {'nome': 'Água Saborizada', 'descricao': 'Águas com sabores naturais diversos'},
            {'nome': 'Galões', 'descricao': 'Galões de 20 litros para uso doméstico e comercial'},
            {'nome': 'Água Premium', 'descricao': 'Águas premium de fontes especiais'},
        ]

        for cat_data in categorias_data:
            categoria, created = Categoria.objects.get_or_create(
                nome=cat_data['nome'],
                defaults={'descricao': cat_data['descricao']}
            )
            if created:
                self.stdout.write(f'Categoria criada: {categoria.nome}')

        # Criar formas de pagamento
        formas_pagamento_data = [
            {
                'nome': 'À Vista',
                'descricao': 'Pagamento à vista (dinheiro, PIX, débito)',
                'prazo_recebimento': 0,
                'ativo': True
            },
            {
                'nome': 'Cartão de Crédito',
                'descricao': 'Pagamento via cartão de crédito',
                'prazo_recebimento': 30,
                'ativo': True
            },
            {
                'nome': 'Boleto 15 dias',
                'descricao': 'Pagamento via boleto bancário com vencimento em 15 dias',
                'prazo_recebimento': 15,
                'ativo': True
            },
            {
                'nome': 'Boleto 30 dias',
                'descricao': 'Pagamento via boleto bancário com vencimento em 30 dias',
                'prazo_recebimento': 30,
                'ativo': True
            },
            {
                'nome': 'Crediário 60 dias',
                'descricao': 'Pagamento parcelado com prazo de 60 dias',
                'prazo_recebimento': 60,
                'ativo': True
            },
            {
                'nome': 'Transferência Bancária',
                'descricao': 'Pagamento via transferência bancária',
                'prazo_recebimento': 1,
                'ativo': True
            }
        ]

        for forma_data in formas_pagamento_data:
            forma_pagamento, created = FormaPagamento.objects.get_or_create(
                nome=forma_data['nome'],
                defaults=forma_data
            )
            if created:
                self.stdout.write(f'Forma de pagamento criada: {forma_pagamento.nome}')

        # Criar fornecedores
        fornecedores_data = [
            {
                'nome': 'Águas Cristalinas Ltda',
                'cnpj': '12.345.678/0001-90',
                'telefone': '(11) 1234-5678',
                'email': 'contato@cristalinas.com.br',
                'endereco': 'Rua das Fontes, 123 - São Paulo/SP'
            },
            {
                'nome': 'Distribuidora Água Pura',
                'cnpj': '98.765.432/0001-10',
                'telefone': '(11) 8765-4321',
                'email': 'vendas@aguapura.com.br',
                'endereco': 'Av. Água Limpa, 456 - São Paulo/SP'
            },
            {
                'nome': 'Fonte Natural Distribuidora',
                'cnpj': '55.444.333/0001-22',
                'telefone': '(11) 5555-4444',
                'email': 'comercial@fontenatural.com.br',
                'endereco': 'Estrada da Serra, 789 - Mogi das Cruzes/SP'
            }
        ]

        for forn_data in fornecedores_data:
            fornecedor, created = Fornecedor.objects.get_or_create(
                cnpj=forn_data['cnpj'],
                defaults=forn_data
            )
            if created:
                self.stdout.write(f'Fornecedor criado: {fornecedor.nome}')

        # Criar clientes
        clientes_data = [
            {
                'nome': 'João Silva',
                'cpf_cnpj': '123.456.789-00',
                'telefone': '(11) 9999-1234',
                'email': 'joao@email.com',
                'endereco': 'Rua A, 123 - São Paulo/SP'
            },
            {
                'nome': 'Maria Santos',
                'cpf_cnpj': '987.654.321-00',
                'telefone': '(11) 8888-5678',
                'email': 'maria@email.com',
                'endereco': 'Rua B, 456 - São Paulo/SP'
            },
            {
                'nome': 'Empresa ABC Ltda',
                'cpf_cnpj': '11.222.333/0001-44',
                'telefone': '(11) 7777-9999',
                'email': 'contato@abc.com.br',
                'endereco': 'Av. Comercial, 789 - São Paulo/SP'
            },
            {
                'nome': 'Carlos Oliveira',
                'cpf_cnpj': '456.789.123-00',
                'telefone': '(11) 6666-3333',
                'email': 'carlos@email.com',
                'endereco': 'Rua C, 321 - São Paulo/SP'
            },
            {
                'nome': 'Restaurante Bom Sabor',
                'cpf_cnpj': '22.333.444/0001-55',
                'telefone': '(11) 5555-2222',
                'email': 'pedidos@bomsabor.com.br',
                'endereco': 'Av. Central, 654 - São Paulo/SP'
            }
        ]

        for cli_data in clientes_data:
            cliente, created = Cliente.objects.get_or_create(
                cpf_cnpj=cli_data['cpf_cnpj'],
                defaults=cli_data
            )
            if created:
                self.stdout.write(f'Cliente criado: {cliente.nome}')

        # Criar produtos
        produtos_data = [
            {
                'nome': 'Água Mineral Crystal 500ml',
                'categoria': 'Água Mineral',
                'codigo': 'AM-500ML-001',
                'preco_venda': Decimal('2.50'),
                'preco_custo': Decimal('1.20'),
                'estoque_minimo': 50,
                'estoque_atual': 120,
                'unidade_medida': 'UN'
            },
            {
                'nome': 'Água Mineral Crystal 1,5L',
                'categoria': 'Água Mineral',
                'codigo': 'AM-1500ML-002',
                'preco_venda': Decimal('4.90'),
                'preco_custo': Decimal('2.30'),
                'estoque_minimo': 30,
                'estoque_atual': 75,
                'unidade_medida': 'UN'
            },
            {
                'nome': 'Água Alcalina pH 9,5 - 500ml',
                'categoria': 'Água Alcalina',
                'codigo': 'AA-500ML-003',
                'preco_venda': Decimal('3.80'),
                'preco_custo': Decimal('2.10'),
                'estoque_minimo': 25,
                'estoque_atual': 45,
                'unidade_medida': 'UN'
            },
            {
                'nome': 'Água com Gás Limão 350ml',
                'categoria': 'Água com Gás',
                'codigo': 'AG-350ML-004',
                'preco_venda': Decimal('3.20'),
                'preco_custo': Decimal('1.80'),
                'estoque_minimo': 20,
                'estoque_atual': 35,
                'unidade_medida': 'UN'
            },
            {
                'nome': 'Água Saborizada Morango 500ml',
                'categoria': 'Água Saborizada',
                'codigo': 'AS-500ML-005',
                'preco_venda': Decimal('4.50'),
                'preco_custo': Decimal('2.70'),
                'estoque_minimo': 15,
                'estoque_atual': 28,
                'unidade_medida': 'UN'
            },
            {
                'nome': 'Galão de Água 20L',
                'categoria': 'Galões',
                'codigo': 'GL-20L-006',
                'preco_venda': Decimal('18.90'),
                'preco_custo': Decimal('12.50'),
                'estoque_minimo': 10,
                'estoque_atual': 25,
                'unidade_medida': 'UN'
            },
            {
                'nome': 'Água Mineral Premium 750ml',
                'categoria': 'Água Premium',
                'codigo': 'AP-750ML-007',
                'preco_venda': Decimal('6.80'),
                'preco_custo': Decimal('4.20'),
                'estoque_minimo': 20,
                'estoque_atual': 15,  # Estoque baixo para demonstração
                'unidade_medida': 'UN'
            },
            {
                'nome': 'Água Alcalina pH 10 - 1L',
                'categoria': 'Água Alcalina',
                'codigo': 'AA-1000ML-008',
                'preco_venda': Decimal('5.90'),
                'preco_custo': Decimal('3.50'),
                'estoque_minimo': 20,
                'estoque_atual': 42,
                'unidade_medida': 'UN'
            },
            {
                'nome': 'Água com Gás Natural 500ml',
                'categoria': 'Água com Gás',
                'codigo': 'AG-500ML-009',
                'preco_venda': Decimal('4.20'),
                'preco_custo': Decimal('2.80'),
                'estoque_minimo': 25,
                'estoque_atual': 18,  # Estoque baixo
                'unidade_medida': 'UN'
            },
            {
                'nome': 'Água Saborizada Coco 350ml',
                'categoria': 'Água Saborizada',
                'codigo': 'AS-350ML-010',
                'preco_venda': Decimal('3.90'),
                'preco_custo': Decimal('2.40'),
                'estoque_minimo': 15,
                'estoque_atual': 33,
                'unidade_medida': 'UN'
            }
        ]

        admin_user = User.objects.get(username='admin')

        for prod_data in produtos_data:
            categoria = Categoria.objects.get(nome=prod_data['categoria'])
            produto, created = Produto.objects.get_or_create(
                codigo=prod_data['codigo'],
                defaults={
                    'nome': prod_data['nome'],
                    'categoria': categoria,
                    'preco_venda': prod_data['preco_venda'],
                    'preco_custo': prod_data['preco_custo'],
                    'estoque_minimo': prod_data['estoque_minimo'],
                    'estoque_atual': prod_data['estoque_atual'],
                    'unidade_medida': prod_data['unidade_medida']
                }
            )
            if created:
                self.stdout.write(f'Produto criado: {produto.nome}')

                # Criar movimentação de entrada inicial
                MovimentacaoEstoque.objects.create(
                    produto=produto,
                    tipo='entrada',
                    quantidade=produto.estoque_atual,
                    preco_unitario=produto.preco_custo,
                    observacao='Estoque inicial',
                    usuario=admin_user
                )

        # Criar algumas movimentações de exemplo
        produtos = Produto.objects.all()
        forma_pagamento_avista = FormaPagamento.objects.get(nome='À Vista')
        forma_pagamento_cartao = FormaPagamento.objects.get(nome='Cartão de Crédito')
        forma_pagamento_boleto = FormaPagamento.objects.get(nome='Boleto 30 dias')
        
        # Criar movimentações de saída variadas
        formas_pagamento = [forma_pagamento_avista, forma_pagamento_cartao, forma_pagamento_boleto]
        
        for i, produto in enumerate(produtos[:5]):  # Primeiros 5 produtos
            # Alternar entre as formas de pagamento
            forma_pagamento = formas_pagamento[i % len(formas_pagamento)]
            quantidade_venda = random.randint(3, 15)
            
            MovimentacaoEstoque.objects.create(
                produto=produto,
                tipo='saida',
                quantidade=quantidade_venda,
                preco_unitario=produto.preco_venda,
                forma_pagamento=forma_pagamento,
                observacao=f'Venda para cliente - {forma_pagamento.nome}',
                usuario=admin_user
            )
            # Atualizar estoque
            produto.estoque_atual -= quantidade_venda
            produto.save()

        # Criar algumas movimentações de ajuste
        for produto in produtos[5:8]:  # Próximos 3 produtos
            quantidade_ajuste = random.randint(-5, 10)
            MovimentacaoEstoque.objects.create(
                produto=produto,
                tipo='ajuste',
                quantidade=quantidade_ajuste,
                observacao='Ajuste de estoque - inventário',
                usuario=admin_user
            )
            # Atualizar estoque
            produto.estoque_atual += quantidade_ajuste
            if produto.estoque_atual < 0:
                produto.estoque_atual = 0
            produto.save()

        self.stdout.write(
            self.style.SUCCESS(
                '\n✅ Dados de exemplo criados com sucesso!\n'
                '\n🔑 CREDENCIAIS DE ACESSO:'
                '\n   Administrador: admin / admin123'
                '\n   Usuário: usuario / usuario123'
                '\n\n📊 DADOS CRIADOS:'
                f'\n   • {Categoria.objects.count()} Categorias'
                f'\n   • {FormaPagamento.objects.count()} Formas de Pagamento'
                f'\n   • {Produto.objects.count()} Produtos'
                f'\n   • {Fornecedor.objects.count()} Fornecedores'
                f'\n   • {Cliente.objects.count()} Clientes'
                f'\n   • {MovimentacaoEstoque.objects.count()} Movimentações'
                '\n\n� DICAS:'
                '\n   • Use --clear para limpar dados existentes'
                '\n   • Produtos com estoque baixo aparecem destacados'
                '\n   • Movimentações incluem vendas, entradas e ajustes'
                '\n\n�🚀 Sistema pronto para uso!'
            )
        )
