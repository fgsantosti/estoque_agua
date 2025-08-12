from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import (
    Categoria, Produto, Fornecedor, Cliente, FormaPagamento, 
    MovimentacaoEstoque, Venda, ItemVenda, Pagamento, 
    ContasReceber, PagamentoConta
)
from django.utils import timezone
from decimal import Decimal
import random
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Cria dados de exemplo completos para o sistema de estoque de água (produtos, clientes, vendas)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Limpa todos os dados existentes antes de criar novos',
        )
        parser.add_argument(
            '--only-vendas',
            action='store_true',
            help='Cria apenas vendas de exemplo (assume que produtos já existem)',
        )
        parser.add_argument(
            '--vendas',
            type=int,
            default=15,
            help='Número de vendas a serem criadas (padrão: 15)',
        )
        parser.add_argument(
            '--contas',
            type=int,
            default=10,
            help='Número de contas a receber a serem criadas (padrão: 10)',
        )
        parser.add_argument(
            '--pagamentos',
            action='store_true',
            help='Criar pagamentos de exemplo para as vendas e contas',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Limpando todos os dados existentes...'))
            # Ordem de exclusão para evitar problemas de foreign key
            PagamentoConta.objects.all().delete()
            Pagamento.objects.all().delete()
            ContasReceber.objects.all().delete()
            MovimentacaoEstoque.objects.all().delete()
            ItemVenda.objects.all().delete()
            Venda.objects.all().delete()
            Produto.objects.all().delete()
            Cliente.objects.all().delete()
            Fornecedor.objects.all().delete()
            FormaPagamento.objects.all().delete()
            Categoria.objects.all().delete()
            # Não excluir usuários para segurança
            self.stdout.write(self.style.SUCCESS('Dados existentes removidos!'))

        if not options['only_vendas']:
            self.criar_dados_base()
        
        self.criar_vendas_exemplo(options['vendas'])
        
        # Criar contas a receber se solicitado
        if not options['only_vendas']:
            self.criar_contas_receber_exemplo(options['contas'])
        
        # Criar pagamentos se solicitado
        if options['pagamentos']:
            self.criar_pagamentos_exemplo()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n🎉 Dados de exemplo criados com sucesso!\n'
                f'📊 Estatísticas:\n'
                f'   - Categorias: {Categoria.objects.count()}\n'
                f'   - Produtos: {Produto.objects.count()}\n'
                f'   - Clientes: {Cliente.objects.count()}\n'
                f'   - Fornecedores: {Fornecedor.objects.count()}\n'
                f'   - Formas de Pagamento: {FormaPagamento.objects.count()}\n'
                f'   - Vendas: {Venda.objects.count()}\n'
                f'   - Contas a Receber: {ContasReceber.objects.count()}\n'
                f'   - Pagamentos: {Pagamento.objects.count()}\n'
                f'   - Pagamentos de Contas: {PagamentoConta.objects.count()}\n'
                f'   - Movimentações: {MovimentacaoEstoque.objects.count()}\n'
            )
        )

    def criar_dados_base(self):
        self.stdout.write('📦 Criando dados base do sistema...')
        
        # Criar superusuário se não existir
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@estoque.com',
                password='admin123',
                first_name='Administrador'
            )
            self.stdout.write(self.style.SUCCESS('👤 Superusuário criado: admin/admin123'))

        # Criar usuário comum se não existir
        if not User.objects.filter(username='usuario').exists():
            User.objects.create_user(
                username='usuario',
                email='usuario@estoque.com',
                password='usuario123',
                first_name='Usuário Comum'
            )
            self.stdout.write(self.style.SUCCESS('👤 Usuário comum criado: usuario/usuario123'))

        # Criar categorias
        self.stdout.write('🏷️ Criando categorias...')
        categorias_data = [
            {'nome': 'Água Mineral', 'descricao': 'Águas minerais naturais em diversos formatos'},
            {'nome': 'Água Alcalina', 'descricao': 'Águas com pH alcalino para melhor hidratação'},
            {'nome': 'Água com Gás', 'descricao': 'Águas gaseificadas naturalmente ou artificialmente'},
            {'nome': 'Água Saborizada', 'descricao': 'Águas com sabores naturais diversos'},
            {'nome': 'Galões', 'descricao': 'Galões de 20 litros para uso doméstico e comercial'},
            {'nome': 'Copos Descartáveis', 'descricao': 'Copos plásticos descartáveis'},
            {'nome': 'Acessórios', 'descricao': 'Bombas, suportes e outros acessórios'},
        ]

        for cat_data in categorias_data:
            categoria, created = Categoria.objects.get_or_create(
                nome=cat_data['nome'],
                defaults={'descricao': cat_data['descricao']}
            )
            if created:
                self.stdout.write(f'   ✅ {categoria.nome}')

        # Criar formas de pagamento
        self.stdout.write('💳 Criando formas de pagamento...')
        formas_pagamento_data = [
            {
                'nome': 'Dinheiro',
                'descricao': 'Pagamento em dinheiro à vista',
                'prazo_recebimento': 0,
            },
            {
                'nome': 'PIX',
                'descricao': 'Pagamento via PIX instantâneo',
                'prazo_recebimento': 0,
            },
            {
                'nome': 'Cartão de Débito',
                'descricao': 'Pagamento via cartão de débito',
                'prazo_recebimento': 0,
            },
            {
                'nome': 'Cartão de Crédito',
                'descricao': 'Pagamento via cartão de crédito',
                'prazo_recebimento': 30,
            },
            {
                'nome': 'Boleto 15 dias',
                'descricao': 'Pagamento via boleto com vencimento em 15 dias',
                'prazo_recebimento': 15,
            },
            {
                'nome': 'Boleto 60 dias',
                'descricao': 'Pagamento via boleto com vencimento em 60 dias',
                'prazo_recebimento': 60,
            },
            {
                'nome': 'Crediário 30 dias',
                'descricao': 'Pagamento a prazo em 30 dias',
                'prazo_recebimento': 30,
            },
        ]

        for forma_data in formas_pagamento_data:
            forma, created = FormaPagamento.objects.get_or_create(
                nome=forma_data['nome'],
                defaults=forma_data
            )
            if created:
                self.stdout.write(f'   ✅ {forma.nome}')

        # Criar fornecedores
        self.stdout.write('🚚 Criando fornecedores...')
        fornecedores_data = [
            {
                'nome': 'Águas Cristalinas Ltda',
                'cnpj': '12.345.678/0001-90',
                'telefone': '(11) 3333-4444',
                'email': 'vendas@cristalinas.com.br',
                'endereco': 'Av. das Fontes, 1000 - São Paulo/SP',
            },
            {
                'nome': 'Fonte Pura Distribuidora',
                'cnpj': '98.765.432/0001-10',
                'telefone': '(21) 2222-5555',
                'email': 'comercial@fontepura.com.br',
                'endereco': 'Rua da Natureza, 500 - Rio de Janeiro/RJ',
            },
            {
                'nome': 'Água Viva Comércio',
                'cnpj': '11.222.333/0001-44',
                'telefone': '(31) 1111-6666',
                'email': 'contato@aguaviva.com.br',
                'endereco': 'Praça das Águas, 200 - Belo Horizonte/MG',
            },
        ]

        for forn_data in fornecedores_data:
            fornecedor, created = Fornecedor.objects.get_or_create(
                cnpj=forn_data['cnpj'],
                defaults=forn_data
            )
            if created:
                self.stdout.write(f'   ✅ {fornecedor.nome}')

        # Criar produtos
        self.stdout.write('📦 Criando produtos...')
        categoria_agua = Categoria.objects.get(nome='Água Mineral')
        categoria_alcalina = Categoria.objects.get(nome='Água Alcalina')
        categoria_com_gas = Categoria.objects.get(nome='Água com Gás')
        categoria_saborizada = Categoria.objects.get(nome='Água Saborizada')
        categoria_galoes = Categoria.objects.get(nome='Galões')
        categoria_copos = Categoria.objects.get(nome='Copos Descartáveis')
        categoria_acessorios = Categoria.objects.get(nome='Acessórios')

        produtos_data = [
            # Água Mineral
            {
                'nome': 'Água Mineral Crystal 500ml',
                'categoria': categoria_agua,
                'codigo': 'CRYSTAL-500',
                'preco_venda': Decimal('2.50'),
                'preco_custo': Decimal('1.20'),
                'estoque_minimo': 100,
                'estoque_atual': 500,
                'unidade_medida': 'UN'
            },
            {
                'nome': 'Água Mineral Crystal 1,5L',
                'categoria': categoria_agua,
                'codigo': 'CRYSTAL-1500',
                'preco_venda': Decimal('4.00'),
                'preco_custo': Decimal('2.00'),
                'estoque_minimo': 50,
                'estoque_atual': 300,
                'unidade_medida': 'UN'
            },
            {
                'nome': 'Água Mineral Premium 500ml',
                'categoria': categoria_agua,
                'codigo': 'PREMIUM-500',
                'preco_venda': Decimal('3.50'),
                'preco_custo': Decimal('1.80'),
                'estoque_minimo': 50,
                'estoque_atual': 200,
                'unidade_medida': 'UN'
            },
            
            # Água Alcalina
            {
                'nome': 'Água Alcalina pH 9.5 - 500ml',
                'categoria': categoria_alcalina,
                'codigo': 'ALCALINA-500',
                'preco_venda': Decimal('5.00'),
                'preco_custo': Decimal('2.50'),
                'estoque_minimo': 30,
                'estoque_atual': 150,
                'unidade_medida': 'UN'
            },
            
            # Água com Gás
            {
                'nome': 'Água com Gás Natural 500ml',
                'categoria': categoria_com_gas,
                'codigo': 'GAS-500',
                'preco_venda': Decimal('3.00'),
                'preco_custo': Decimal('1.50'),
                'estoque_minimo': 40,
                'estoque_atual': 180,
                'unidade_medida': 'UN'
            },
            
            # Água Saborizada
            {
                'nome': 'Água Saborizada Limão 500ml',
                'categoria': categoria_saborizada,
                'codigo': 'SABOR-LIMAO',
                'preco_venda': Decimal('4.50'),
                'preco_custo': Decimal('2.20'),
                'estoque_minimo': 30,
                'estoque_atual': 120,
                'unidade_medida': 'UN'
            },
            
            # Galões
            {
                'nome': 'Galão 20L Crystal',
                'categoria': categoria_galoes,
                'codigo': 'GALAO-20L',
                'preco_venda': Decimal('15.00'),
                'preco_custo': Decimal('8.00'),
                'estoque_minimo': 20,
                'estoque_atual': 80,
                'unidade_medida': 'UN'
            },
            {
                'nome': 'Galão 10L Compacto',
                'categoria': categoria_galoes,
                'codigo': 'GALAO-10L',
                'preco_venda': Decimal('10.00'),
                'preco_custo': Decimal('5.50'),
                'estoque_minimo': 15,
                'estoque_atual': 60,
                'unidade_medida': 'UN'
            },
            
            # Copos
            {
                'nome': 'Copos 200ml (Pacote 100un)',
                'categoria': categoria_copos,
                'codigo': 'COPO-200ML',
                'preco_venda': Decimal('12.00'),
                'preco_custo': Decimal('6.00'),
                'estoque_minimo': 10,
                'estoque_atual': 50,
                'unidade_medida': 'PCT'
            },
            {
                'nome': 'Copos 300ml (Pacote 50un)',
                'categoria': categoria_copos,
                'codigo': 'COPO-300ML',
                'preco_venda': Decimal('15.00'),
                'preco_custo': Decimal('8.00'),
                'estoque_minimo': 8,
                'estoque_atual': 30,
                'unidade_medida': 'PCT'
            },
            
            # Acessórios
            {
                'nome': 'Bomba Manual para Galão',
                'categoria': categoria_acessorios,
                'codigo': 'BOMBA-MANUAL',
                'preco_venda': Decimal('25.00'),
                'preco_custo': Decimal('12.00'),
                'estoque_minimo': 5,
                'estoque_atual': 20,
                'unidade_medida': 'UN'
            },
            {
                'nome': 'Suporte para Galão',
                'categoria': categoria_acessorios,
                'codigo': 'SUPORTE-GALAO',
                'preco_venda': Decimal('35.00'),
                'preco_custo': Decimal('18.00'),
                'estoque_minimo': 3,
                'estoque_atual': 15,
                'unidade_medida': 'UN'
            },
        ]

        for prod_data in produtos_data:
            produto, created = Produto.objects.get_or_create(
                codigo=prod_data['codigo'],
                defaults=prod_data
            )
            if created:
                self.stdout.write(f'   ✅ {produto.nome}')

        # Criar clientes
        self.stdout.write('👥 Criando clientes...')
        clientes_data = [
            {
                'nome': 'João da Silva',
                'cpf_cnpj': '123.456.789-10',
                'telefone': '(11) 99999-1111',
                'email': 'joao.silva@email.com',
                'endereco': 'Rua das Flores, 123 - Centro - São Paulo/SP'
            },
            {
                'nome': 'Maria Santos',
                'cpf_cnpj': '987.654.321-00',
                'telefone': '(11) 88888-2222',
                'email': 'maria.santos@email.com',
                'endereco': 'Av. Brasil, 456 - Jardim América - São Paulo/SP'
            },
            {
                'nome': 'Pedro Oliveira',
                'cpf_cnpj': '456.789.123-45',
                'telefone': '(11) 77777-3333',
                'email': 'pedro.oliveira@email.com',
                'endereco': 'Praça da Liberdade, 789 - Vila Nova - São Paulo/SP'
            },
            {
                'nome': 'Ana Costa',
                'cpf_cnpj': '321.654.987-12',
                'telefone': '(11) 66666-4444',
                'email': 'ana.costa@email.com',
                'endereco': 'Rua da Paz, 101 - Bela Vista - São Paulo/SP'
            },
            {
                'nome': 'Carlos Ferreira',
                'cpf_cnpj': '159.753.486-89',
                'telefone': '(11) 55555-5555',
                'email': 'carlos.ferreira@email.com',
                'endereco': 'Alameda dos Anjos, 202 - Morumbi - São Paulo/SP'
            },
            {
                'nome': 'Empresa ABC Ltda',
                'cpf_cnpj': '12.345.678/0001-90',
                'telefone': '(11) 4444-6666',
                'email': 'financeiro@empresaabc.com.br',
                'endereco': 'Av. Paulista, 1000 - Bela Vista - São Paulo/SP'
            },
            {
                'nome': 'Restaurante Bom Sabor',
                'cpf_cnpj': '98.765.432/0001-11',
                'telefone': '(11) 3333-7777',
                'email': 'contato@bomsabor.com.br',
                'endereco': 'Rua dos Comerciantes, 500 - Centro - São Paulo/SP'
            },
        ]

        for cliente_data in clientes_data:
            cliente, created = Cliente.objects.get_or_create(
                cpf_cnpj=cliente_data['cpf_cnpj'],
                defaults=cliente_data
            )
            if created:
                self.stdout.write(f'   ✅ {cliente.nome}')

    def criar_vendas_exemplo(self, num_vendas):
        self.stdout.write(f'🛒 Criando {num_vendas} vendas de exemplo...')
        
        # Buscar usuário admin
        try:
            admin_user = User.objects.filter(is_superuser=True).first()
            if not admin_user:
                admin_user = User.objects.first()
                if not admin_user:
                    self.stdout.write(self.style.ERROR('❌ Nenhum usuário encontrado!'))
                    return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erro ao buscar usuário: {e}'))
            return
        
        produtos = list(Produto.objects.filter(ativo=True, estoque_atual__gt=5))
        clientes = list(Cliente.objects.filter(ativo=True))
        formas_pagamento = list(FormaPagamento.objects.filter(ativo=True))
        
        if not produtos:
            self.stdout.write(self.style.ERROR('❌ Nenhum produto encontrado com estoque!'))
            return
        
        if not formas_pagamento:
            self.stdout.write(self.style.ERROR('❌ Nenhuma forma de pagamento encontrada!'))
            return

        vendas_criadas = 0
        
        for i in range(num_vendas):
            try:
                # Data aleatória nos últimos 30 dias
                dias_atras = random.randint(0, 30)
                horas_atras = random.randint(8, 18)  # Horário comercial
                data_venda = timezone.now() - timezone.timedelta(days=dias_atras, hours=horas_atras)
                
                venda = Venda.objects.create(
                    cliente=random.choice(clientes) if random.random() > 0.2 else None,  # 80% com cliente
                    forma_pagamento=random.choice(formas_pagamento),
                    data_venda=data_venda,
                    usuario=admin_user,
                    observacao=f'Venda de exemplo #{i+1} - Gerada automaticamente',
                    status='finalizada'
                )
                
                # Adicionar 1-5 itens aleatórios à venda
                num_itens = random.randint(1, 5)
                produtos_disponiveis = [p for p in produtos if p.estoque_atual > 0]
                
                if not produtos_disponiveis:
                    venda.delete()
                    continue
                
                produtos_selecionados = random.sample(
                    produtos_disponiveis, 
                    min(num_itens, len(produtos_disponiveis))
                )
                
                itens_adicionados = 0
                
                for produto in produtos_selecionados:
                    quantidade_maxima = min(produto.estoque_atual, 10)  # Máximo 10 por item
                    if quantidade_maxima > 0:
                        quantidade = random.randint(1, quantidade_maxima)
                        
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
                        
                        itens_adicionados += 1
                
                # Criar venda com status apropriado baseado na forma de pagamento
                if venda.forma_pagamento.prazo_recebimento > 0 and venda.cliente:
                    # Forma de pagamento a prazo com cliente - criar conta a receber
                    venda.status = 'finalizada'
                    venda.save()
                    
                    # Criar conta a receber automaticamente
                    ContasReceber.objects.create(
                        cliente=venda.cliente,
                        venda=venda,
                        valor_total=venda.valor_total,
                        valor_pago=Decimal('0.00'),
                        data_vencimento=venda.data_vencimento,
                        status='aberto',
                        observacao=f'Venda {venda.numero_venda} - Pagamento a prazo',
                        usuario=admin_user
                    )
                elif venda.cliente:
                    # Com cliente mas pagamento à vista - pode ficar em aberto
                    venda.status = random.choice(['finalizada', 'paga'])
                else:
                    # Sem cliente - venda de balcão
                    venda.status = 'finalizada'
                
                venda.save()
                
                if itens_adicionados > 0:
                    vendas_criadas += 1
                    if vendas_criadas % 5 == 0:
                        self.stdout.write(f'   ✅ {vendas_criadas} vendas criadas...')
                else:
                    venda.delete()
                    
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'⚠️ Erro ao criar venda {i+1}: {e}'))
        
        self.stdout.write(self.style.SUCCESS(f'✅ {vendas_criadas} vendas criadas com sucesso!'))

    def criar_contas_receber_exemplo(self, num_contas):
        """Criar contas a receber avulsas (não vinculadas a vendas)"""
        self.stdout.write(f'💰 Criando {num_contas} contas a receber avulsas...')
        
        # Buscar usuário admin
        try:
            admin_user = User.objects.filter(is_superuser=True).first()
            if not admin_user:
                admin_user = User.objects.first()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erro ao buscar usuário: {e}'))
            return
        
        clientes = list(Cliente.objects.filter(ativo=True))
        
        if not clientes:
            self.stdout.write(self.style.WARNING('⚠️ Nenhum cliente encontrado!'))
            return
            
        contas_criadas = 0
        
        for i in range(num_contas):
            try:
                # Data aleatória nos últimos 60 dias
                dias_atras = random.randint(0, 60)
                data_criacao = timezone.now() - timezone.timedelta(days=dias_atras)
                
                # Data de vencimento entre hoje e 90 dias no futuro
                dias_vencimento = random.randint(-10, 90)  # Algumas podem estar vencidas
                data_vencimento = date.today() + timedelta(days=dias_vencimento)
                
                # Valor aleatório entre R$ 50 e R$ 500
                valor_total = Decimal(random.uniform(50, 500)).quantize(Decimal('0.01'))
                
                # Status baseado na data de vencimento
                if dias_vencimento < 0:
                    status = 'vencido'
                    valor_pago = Decimal('0.00')  # Conta vencida sem pagamento
                else:
                    status = random.choice(['aberto', 'parcial'])
                    if status == 'parcial':
                        valor_pago = (valor_total * Decimal(random.uniform(0.3, 0.8))).quantize(Decimal('0.01'))
                    else:
                        valor_pago = Decimal('0.00')
                
                conta = ContasReceber.objects.create(
                    cliente=random.choice(clientes),
                    venda=None,  # Conta avulsa, não vinculada a venda
                    valor_total=valor_total,
                    valor_pago=valor_pago,
                    data_vencimento=data_vencimento,
                    data_criacao=data_criacao,
                    status=status,
                    observacao=f'Conta avulsa #{i+1} - Serviços diversos',
                    usuario=admin_user
                )
                
                contas_criadas += 1
                
                if contas_criadas % 5 == 0:
                    self.stdout.write(f'   ✅ {contas_criadas} contas criadas...')
                    
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'⚠️ Erro ao criar conta {i+1}: {e}'))
        
        self.stdout.write(self.style.SUCCESS(f'✅ {contas_criadas} contas a receber criadas!'))

    def criar_pagamentos_exemplo(self):
        """Criar pagamentos de exemplo para vendas e contas"""
        self.stdout.write('💳 Criando pagamentos de exemplo...')
        
        # Buscar usuário admin
        try:
            admin_user = User.objects.filter(is_superuser=True).first()
            if not admin_user:
                admin_user = User.objects.first()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erro ao buscar usuário: {e}'))
            return
        
        formas_pagamento = list(FormaPagamento.objects.filter(ativo=True))
        
        if not formas_pagamento:
            self.stdout.write(self.style.WARNING('⚠️ Nenhuma forma de pagamento encontrada!'))
            return
        
        pagamentos_vendas = 0
        pagamentos_contas = 0
        
        # Criar pagamentos para algumas vendas com cliente
        vendas_com_cliente = Venda.objects.filter(
            cliente__isnull=False,
            status__in=['finalizada', 'aberta']
        ).select_related('cliente')[:10]  # Pegar apenas algumas vendas
        
        for venda in vendas_com_cliente:
            # 70% de chance de ter pagamento
            if random.random() < 0.7:
                try:
                    # Valor do pagamento (pode ser parcial)
                    valor_total_venda = venda.valor_total
                    if random.random() < 0.3:  # 30% pagamento parcial
                        valor_pagamento = (valor_total_venda * Decimal(random.uniform(0.3, 0.8))).quantize(Decimal('0.01'))
                    else:  # 70% pagamento total
                        valor_pagamento = valor_total_venda
                    
                    # Data do pagamento (alguns dias após a venda)
                    dias_apos_venda = random.randint(0, 15)
                    data_pagamento = venda.data_venda + timezone.timedelta(days=dias_apos_venda)
                    
                    Pagamento.objects.create(
                        venda=venda,
                        forma_pagamento=random.choice(formas_pagamento),
                        valor_pago=valor_pagamento,
                        data_pagamento=data_pagamento,
                        observacao=f'Pagamento da venda {venda.numero_venda}',
                        usuario=admin_user
                    )
                    
                    # Atualizar status da venda
                    venda.atualizar_status_pagamento()
                    
                    pagamentos_vendas += 1
                    
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'⚠️ Erro ao criar pagamento para venda {venda.numero_venda}: {e}'))
        
        # Criar pagamentos para contas a receber avulsas
        contas_avulsas = ContasReceber.objects.filter(
            venda__isnull=True,
            status__in=['aberto', 'parcial', 'vencido']
        ).select_related('cliente')[:8]  # Pegar algumas contas
        
        for conta in contas_avulsas:
            # 60% de chance de ter pagamento
            if random.random() < 0.6:
                try:
                    # Valor do pagamento
                    valor_pendente = conta.valor_pendente
                    if valor_pendente > 0:
                        if random.random() < 0.4:  # 40% pagamento parcial
                            valor_pagamento = (valor_pendente * Decimal(random.uniform(0.3, 0.9))).quantize(Decimal('0.01'))
                        else:  # 60% pagamento do valor pendente
                            valor_pagamento = valor_pendente
                        
                        # Data do pagamento
                        dias_apos_criacao = random.randint(1, 30)
                        data_pagamento = conta.data_criacao + timezone.timedelta(days=dias_apos_criacao)
                        
                        PagamentoConta.objects.create(
                            conta_receber=conta,
                            forma_pagamento=random.choice(formas_pagamento),
                            valor_pago=valor_pagamento,
                            data_pagamento=data_pagamento,
                            observacao=f'Pagamento da conta {conta.cliente.nome}',
                            usuario=admin_user
                        )
                        
                        # Atualizar valor pago na conta
                        conta.valor_pago += valor_pagamento
                        
                        # Atualizar status da conta
                        if conta.valor_pago >= conta.valor_total:
                            conta.status = 'quitado'
                        elif conta.valor_pago > 0:
                            conta.status = 'parcial'
                        
                        conta.save()
                        
                        pagamentos_contas += 1
                        
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'⚠️ Erro ao criar pagamento para conta {conta.id}: {e}'))
        
        self.stdout.write(self.style.SUCCESS(f'✅ {pagamentos_vendas} pagamentos de vendas e {pagamentos_contas} pagamentos de contas criados!'))
