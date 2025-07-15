from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Categoria, Produto, Fornecedor, Cliente, MovimentacaoEstoque
from django.utils import timezone
from decimal import Decimal

class Command(BaseCommand):
    help = 'Cria dados de exemplo para o sistema de estoque de água'

    def handle(self, *args, **options):
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
            {'nome': 'Água Mineral', 'descricao': 'Águas minerais em diversos formatos'},
            {'nome': 'Água Alcalina', 'descricao': 'Águas com pH alcalino'},
            {'nome': 'Água com Gás', 'descricao': 'Águas gaseificadas'},
            {'nome': 'Água Saborizada', 'descricao': 'Águas com sabores diversos'},
            {'nome': 'Galões', 'descricao': 'Galões de 20 litros'},
        ]

        for cat_data in categorias_data:
            categoria, created = Categoria.objects.get_or_create(
                nome=cat_data['nome'],
                defaults={'descricao': cat_data['descricao']}
            )
            if created:
                self.stdout.write(f'Categoria criada: {categoria.nome}')

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
                'categoria': 'Água Mineral',
                'codigo': 'AM-750ML-007',
                'preco_venda': Decimal('6.80'),
                'preco_custo': Decimal('4.20'),
                'estoque_minimo': 20,
                'estoque_atual': 15,  # Estoque baixo para demonstração
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
        produtos = Produto.objects.all()[:3]
        for produto in produtos:
            # Movimentação de saída
            MovimentacaoEstoque.objects.create(
                produto=produto,
                tipo='saida',
                quantidade=10,
                observacao='Venda para cliente',
                usuario=admin_user
            )
            # Atualizar estoque
            produto.estoque_atual -= 10
            produto.save()

        self.stdout.write(
            self.style.SUCCESS(
                '\n✅ Dados de exemplo criados com sucesso!\n'
                '\n🔑 CREDENCIAIS DE ACESSO:'
                '\n   Administrador: admin / admin123'
                '\n   Usuário: usuario / usuario123'
                '\n\n📊 DADOS CRIADOS:'
                f'\n   • {Categoria.objects.count()} Categorias'
                f'\n   • {Produto.objects.count()} Produtos'
                f'\n   • {Fornecedor.objects.count()} Fornecedores'
                f'\n   • {Cliente.objects.count()} Clientes'
                f'\n   • {MovimentacaoEstoque.objects.count()} Movimentações'
                '\n\n🚀 Sistema pronto para uso!'
            )
        )
