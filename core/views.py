from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q, F
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Produto, MovimentacaoEstoque, Fornecedor, Cliente, Categoria, FormaPagamento
from .forms import ProdutoForm, MovimentacaoEstoqueForm, FornecedorForm, ClienteForm, CategoriaForm, FormaPagamentoForm
from django.utils import timezone
from datetime import datetime, timedelta

@login_required
def dashboard(request):
    # Estatísticas gerais
    total_produtos = Produto.objects.filter(ativo=True).count()
    produtos_estoque_baixo = Produto.objects.filter(
        ativo=True, 
        estoque_atual__lte=F('estoque_minimo')
    ).count()

    # Valor total do estoque
    valor_total_estoque = sum([p.valor_total_estoque for p in Produto.objects.filter(ativo=True)])

    # Movimentações recentes
    movimentacoes_recentes = MovimentacaoEstoque.objects.select_related('produto', 'usuario')[:10]

    # Produtos com estoque baixo
    produtos_baixo_estoque = Produto.objects.filter(
        ativo=True,
        estoque_atual__lte=F('estoque_minimo')
    )[:5]

    # Movimentações dos últimos 7 dias
    data_limite = timezone.now() - timedelta(days=7)
    movimentacoes_semana = MovimentacaoEstoque.objects.filter(
        data_movimentacao__gte=data_limite
    ).values('tipo').annotate(
        total=Count('id'),
        quantidade_total=Sum('quantidade')
    )

    # Top 5 produtos mais movimentados
    produtos_mais_movimentados = MovimentacaoEstoque.objects.filter(
        data_movimentacao__gte=data_limite
    ).values('produto__nome').annotate(
        total_movimentacoes=Count('id')
    ).order_by('-total_movimentacoes')[:5]

    context = {
        'total_produtos': total_produtos,
        'produtos_estoque_baixo': produtos_estoque_baixo,
        'valor_total_estoque': valor_total_estoque,
        'movimentacoes_recentes': movimentacoes_recentes,
        'produtos_baixo_estoque': produtos_baixo_estoque,
        'movimentacoes_semana': movimentacoes_semana,
        'produtos_mais_movimentados': produtos_mais_movimentados,
    }

    return render(request, 'core/dashboard.html', context)

@login_required
def produto_list(request):
    produtos = Produto.objects.select_related('categoria').filter(ativo=True)

    # Filtros
    search = request.GET.get('search')
    categoria_id = request.GET.get('categoria')

    if search:
        produtos = produtos.filter(
            Q(nome__icontains=search) | Q(codigo__icontains=search)
        )

    if categoria_id:
        produtos = produtos.filter(categoria_id=categoria_id)

    # Paginação
    paginator = Paginator(produtos, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categorias = Categoria.objects.all()

    context = {
        'page_obj': page_obj,
        'categorias': categorias,
        'search': search,
        'categoria_id': categoria_id,
    }

    return render(request, 'core/produto_list.html', context)

@login_required
def produto_create(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            produto = form.save()
            messages.success(request, f'Produto {produto.nome} criado com sucesso!')
            return redirect('produto_list')
    else:
        form = ProdutoForm()

    return render(request, 'core/produto_form.html', {'form': form, 'title': 'Novo Produto'})

@login_required
def produto_edit(request, pk):
    produto = get_object_or_404(Produto, pk=pk)

    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, f'Produto {produto.nome} atualizado com sucesso!')
            return redirect('produto_list')
    else:
        form = ProdutoForm(instance=produto)

    return render(request, 'core/produto_form.html', {
        'form': form, 
        'title': f'Editar Produto: {produto.nome}',
        'produto': produto
    })

@login_required
def movimentacao_list(request):
    movimentacoes = MovimentacaoEstoque.objects.select_related('produto', 'usuario').all()

    # Filtros
    tipo = request.GET.get('tipo')
    produto_id = request.GET.get('produto')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    if tipo:
        movimentacoes = movimentacoes.filter(tipo=tipo)

    if produto_id:
        movimentacoes = movimentacoes.filter(produto_id=produto_id)

    if data_inicio:
        movimentacoes = movimentacoes.filter(data_movimentacao__date__gte=data_inicio)

    if data_fim:
        movimentacoes = movimentacoes.filter(data_movimentacao__date__lte=data_fim)

    # Paginação
    paginator = Paginator(movimentacoes, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    produtos = Produto.objects.filter(ativo=True)

    context = {
        'page_obj': page_obj,
        'produtos': produtos,
        'tipo': tipo,
        'produto_id': produto_id,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
    }

    return render(request, 'core/movimentacao_list.html', context)

@login_required
def movimentacao_create(request):
    if request.method == 'POST':
        form = MovimentacaoEstoqueForm(request.POST)
        if form.is_valid():
            movimentacao = form.save(commit=False)
            movimentacao.usuario = request.user

            # Atualizar estoque do produto
            produto = movimentacao.produto
            if movimentacao.tipo == 'entrada':
                produto.estoque_atual += movimentacao.quantidade
            elif movimentacao.tipo == 'saida':
                if produto.estoque_atual >= movimentacao.quantidade:
                    produto.estoque_atual -= movimentacao.quantidade
                else:
                    messages.error(request, 'Estoque insuficiente para esta saída!')
                    return render(request, 'core/movimentacao_form.html', {'form': form})
            elif movimentacao.tipo == 'ajuste':
                produto.estoque_atual = movimentacao.quantidade

            produto.save()
            movimentacao.save()

            messages.success(request, 'Movimentação registrada com sucesso!')
            return redirect('movimentacao_list')
    else:
        form = MovimentacaoEstoqueForm()

    return render(request, 'core/movimentacao_form.html', {'form': form})

@login_required
def fornecedor_list(request):
    fornecedores = Fornecedor.objects.filter(ativo=True)

    search = request.GET.get('search')
    if search:
        fornecedores = fornecedores.filter(
            Q(nome__icontains=search) | Q(cnpj__icontains=search)
        )

    paginator = Paginator(fornecedores, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/fornecedor_list.html', {'page_obj': page_obj, 'search': search})

@login_required
def fornecedor_create(request):
    if request.method == 'POST':
        form = FornecedorForm(request.POST)
        if form.is_valid():
            fornecedor = form.save()
            messages.success(request, f'Fornecedor {fornecedor.nome} criado com sucesso!')
            return redirect('fornecedor_list')
    else:
        form = FornecedorForm()

    return render(request, 'core/fornecedor_form.html', {'form': form, 'title': 'Novo Fornecedor'})

@login_required
def cliente_list(request):
    clientes = Cliente.objects.filter(ativo=True)

    search = request.GET.get('search')
    if search:
        clientes = clientes.filter(
            Q(nome__icontains=search) | Q(cpf_cnpj__icontains=search)
        )

    paginator = Paginator(clientes, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/cliente_list.html', {'page_obj': page_obj, 'search': search})

@login_required
def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, f'Cliente {cliente.nome} criado com sucesso!')
            return redirect('cliente_list')
    else:
        form = ClienteForm()

    return render(request, 'core/cliente_form.html', {'form': form, 'title': 'Novo Cliente'})

@login_required
def categoria_list(request):
    categorias = Categoria.objects.all()
    return render(request, 'core/categoria_list.html', {'categorias': categorias})

@login_required
def categoria_create(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save()
            messages.success(request, f'Categoria {categoria.nome} criada com sucesso!')
            return redirect('categoria_list')
    else:
        form = CategoriaForm()

    return render(request, 'core/categoria_form.html', {'form': form, 'title': 'Nova Categoria'})

@login_required
def forma_pagamento_list(request):
    formas_pagamento = FormaPagamento.objects.all()
    return render(request, 'core/forma_pagamento_list.html', {'formas_pagamento': formas_pagamento})

@login_required
def forma_pagamento_create(request):
    if request.method == 'POST':
        form = FormaPagamentoForm(request.POST)
        if form.is_valid():
            forma_pagamento = form.save()
            messages.success(request, f'Forma de pagamento {forma_pagamento.nome} criada com sucesso!')
            return redirect('forma_pagamento_list')
    else:
        form = FormaPagamentoForm()

    return render(request, 'core/forma_pagamento_form.html', {'form': form, 'title': 'Nova Forma de Pagamento'})
