from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q, F
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db import transaction
from .models import (Produto, MovimentacaoEstoque, Fornecedor, Cliente, Categoria, 
                    FormaPagamento, Venda, ItemVenda, Pagamento, ContasReceber, PagamentoConta)
from .forms import (ProdutoForm, MovimentacaoEstoqueForm, FornecedorForm, ClienteForm, 
                   CategoriaForm, FormaPagamentoForm, VendaForm, ItemVendaFormSet, 
                   PagamentoForm, ContasReceberForm, PagamentoContaForm)
from django.utils import timezone
from datetime import datetime, timedelta

def homepage(request):
    """Homepage pública da Império das Águas"""
    return render(request, 'core/homepage.html', {
        'title': 'Império das Águas - Água Mineral de Qualidade'
    })

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

    # Estatísticas de vendas
    data_limite = timezone.now() - timedelta(days=30)
    vendas_mes = Venda.objects.filter(data_venda__gte=data_limite, status='finalizada')
    total_vendas_mes = vendas_mes.count()
    valor_vendas_mes = sum(v.valor_total for v in vendas_mes)
    
    # Vendas de hoje
    hoje = timezone.now().date()
    vendas_hoje = Venda.objects.filter(data_venda__date=hoje, status='finalizada')
    total_vendas_hoje = vendas_hoje.count()
    valor_vendas_hoje = sum(v.valor_total for v in vendas_hoje)

    # Movimentações recentes
    movimentacoes_recentes = MovimentacaoEstoque.objects.select_related('produto', 'usuario')[:10]

    # Vendas recentes
    vendas_recentes = Venda.objects.select_related('cliente', 'usuario').filter(status='finalizada')[:5]

    # Produtos com estoque baixo
    produtos_baixo_estoque = Produto.objects.filter(
        ativo=True,
        estoque_atual__lte=F('estoque_minimo')
    )[:5]

    # Movimentações dos últimos 7 dias
    data_limite_semana = timezone.now() - timedelta(days=7)
    movimentacoes_semana = MovimentacaoEstoque.objects.filter(
        data_movimentacao__gte=data_limite_semana
    ).values('tipo').annotate(
        total=Count('id'),
        quantidade_total=Sum('quantidade')
    )

    # Top 5 produtos mais movimentados
    produtos_mais_movimentados = MovimentacaoEstoque.objects.filter(
        data_movimentacao__gte=data_limite_semana
    ).values('produto__nome').annotate(
        total_movimentacoes=Count('id')
    ).order_by('-total_movimentacoes')[:5]

    context = {
        'total_produtos': total_produtos,
        'produtos_estoque_baixo': produtos_estoque_baixo,
        'valor_total_estoque': valor_total_estoque,
        'total_vendas_mes': total_vendas_mes,
        'valor_vendas_mes': valor_vendas_mes,
        'total_vendas_hoje': total_vendas_hoje,
        'valor_vendas_hoje': valor_vendas_hoje,
        'movimentacoes_recentes': movimentacoes_recentes,
        'vendas_recentes': vendas_recentes,
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
def produto_detail(request, pk):
    """Visualizar detalhes de um produto"""
    produto = get_object_or_404(Produto, pk=pk)
    
    # Movimentações recentes do produto
    movimentacoes_recentes = MovimentacaoEstoque.objects.filter(
        produto=produto
    ).select_related('usuario', 'forma_pagamento').order_by('-data_movimentacao')[:10]
    
    # Estatísticas do produto
    total_entradas = MovimentacaoEstoque.objects.filter(
        produto=produto, tipo='entrada'
    ).aggregate(total=Sum('quantidade'))['total'] or 0
    
    total_saidas = MovimentacaoEstoque.objects.filter(
        produto=produto, tipo='saida'
    ).aggregate(total=Sum('quantidade'))['total'] or 0
    
    context = {
        'produto': produto,
        'movimentacoes_recentes': movimentacoes_recentes,
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
        'title': f'Produto: {produto.nome}'
    }
    
    return render(request, 'core/produto_detail.html', context)

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
def produto_delete(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    
    if request.method == 'POST':
        nome_produto = produto.nome
        produto.delete()
        messages.success(request, f'Produto {nome_produto} deletado com sucesso!')
        return redirect('produto_list')
    
    return render(request, 'core/confirm_delete.html', {
        'object': produto,
        'title': f'Deletar Produto: {produto.nome}',
        'cancel_url': 'produto_list'
    })

@login_required
def movimentacao_list(request):
    movimentacoes = MovimentacaoEstoque.objects.select_related('produto', 'usuario', 'forma_pagamento').all()

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

    # Calcular totais das movimentações filtradas
    total_quantidade = sum(mov.quantidade for mov in movimentacoes)
    total_valor = sum(mov.valor_total for mov in movimentacoes if mov.preco_unitario)
    total_movimentacoes = movimentacoes.count()
    
    # Calcular totais por tipo de movimentação
    totais_por_tipo = {
        'entrada': {
            'quantidade': sum(mov.quantidade for mov in movimentacoes if mov.tipo == 'entrada'),
            'valor': sum(mov.valor_total for mov in movimentacoes if mov.tipo == 'entrada' and mov.preco_unitario),
            'count': movimentacoes.filter(tipo='entrada').count()
        },
        'saida': {
            'quantidade': sum(mov.quantidade for mov in movimentacoes if mov.tipo == 'saida'),
            'valor': sum(mov.valor_total for mov in movimentacoes if mov.tipo == 'saida' and mov.preco_unitario),
            'count': movimentacoes.filter(tipo='saida').count()
        },
        'ajuste': {
            'quantidade': sum(mov.quantidade for mov in movimentacoes if mov.tipo == 'ajuste'),
            'valor': sum(mov.valor_total for mov in movimentacoes if mov.tipo == 'ajuste' and mov.preco_unitario),
            'count': movimentacoes.filter(tipo='ajuste').count()
        }
    }

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
        'total_quantidade': total_quantidade,
        'total_valor': total_valor,
        'total_movimentacoes': total_movimentacoes,
        'totais_por_tipo': totais_por_tipo,
    }

    return render(request, 'core/movimentacao_list.html', context)

@login_required
def movimentacao_detail(request, pk):
    """Visualizar detalhes de uma movimentação"""
    movimentacao = get_object_or_404(MovimentacaoEstoque, pk=pk)
    
    context = {
        'movimentacao': movimentacao,
        'title': f'Movimentação: {movimentacao.get_tipo_display()}'
    }
    
    return render(request, 'core/movimentacao_detail.html', context)

@login_required
def movimentacao_edit(request, pk):
    """Editar movimentação (apenas ajustes ou observações)"""
    movimentacao = get_object_or_404(MovimentacaoEstoque, pk=pk)
    
    if request.method == 'POST':
        # Permitir apenas edição de observação para evitar problemas no estoque
        observacao = request.POST.get('observacao', '')
        movimentacao.observacao = observacao
        movimentacao.save()
        messages.success(request, 'Movimentação atualizada com sucesso!')
        return redirect('movimentacao_detail', pk=pk)
    
    context = {
        'movimentacao': movimentacao,
        'title': f'Editar Movimentação: {movimentacao.get_tipo_display()}'
    }
    
    return render(request, 'core/movimentacao_edit.html', context)

@login_required
def movimentacao_delete(request, pk):
    """Deletar movimentação (com cuidado no estoque)"""
    movimentacao = get_object_or_404(MovimentacaoEstoque, pk=pk)
    
    if request.method == 'POST':
        # Reverter o efeito no estoque
        produto = movimentacao.produto
        if movimentacao.tipo == 'entrada':
            produto.estoque_atual -= movimentacao.quantidade
        elif movimentacao.tipo == 'saida':
            produto.estoque_atual += movimentacao.quantidade
        
        produto.save()
        movimentacao.delete()
        messages.success(request, 'Movimentação deletada e estoque ajustado!')
        return redirect('movimentacao_list')
    
    context = {
        'movimentacao': movimentacao,
        'title': f'Deletar Movimentação: {movimentacao.get_tipo_display()}'
    }
    
    return render(request, 'core/movimentacao_confirm_delete.html', context)

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
def fornecedor_detail(request, pk):
    """Visualizar detalhes de um fornecedor"""
    fornecedor = get_object_or_404(Fornecedor, pk=pk)
    
    # Produtos do fornecedor (se houver relacionamento)
    # Assumindo que existe um campo fornecedor no modelo Produto
    try:
        produtos = Produto.objects.filter(fornecedor=fornecedor, ativo=True)
    except:
        produtos = []  # Caso não exista o relacionamento
    
    # Movimentações de entrada relacionadas
    entradas = MovimentacaoEstoque.objects.filter(
        tipo='entrada', 
        observacao__icontains=fornecedor.nome
    ).order_by('-data_movimentacao')[:10]
    
    context = {
        'fornecedor': fornecedor,
        'produtos': produtos[:10] if produtos else [],
        'entradas': entradas,
        'total_produtos': len(produtos) if produtos else 0,
        'title': f'Fornecedor: {fornecedor.nome}'
    }
    
    return render(request, 'core/fornecedor_detail.html', context)

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
def fornecedor_edit(request, pk):
    fornecedor = get_object_or_404(Fornecedor, pk=pk)
    if request.method == 'POST':
        form = FornecedorForm(request.POST, instance=fornecedor)
        if form.is_valid():
            fornecedor = form.save()
            messages.success(request, f'Fornecedor {fornecedor.nome} atualizado com sucesso!')
            return redirect('fornecedor_list')
    else:
        form = FornecedorForm(instance=fornecedor)
    
    return render(request, 'core/fornecedor_form.html', {'form': form, 'title': f'Editar Fornecedor: {fornecedor.nome}'})

@login_required  
def fornecedor_delete(request, pk):
    fornecedor = get_object_or_404(Fornecedor, pk=pk)
    if request.method == 'POST':
        nome = fornecedor.nome
        fornecedor.delete()
        messages.success(request, f'Fornecedor {nome} deletado com sucesso!')
        return redirect('fornecedor_list')
    
    return render(request, 'core/confirm_delete.html', {
        'object': fornecedor,
        'title': f'Deletar Fornecedor: {fornecedor.nome}',
        'cancel_url': 'fornecedor_list'
    })

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
def cliente_detail(request, pk):
    """Visualizar detalhes de um cliente"""
    cliente = get_object_or_404(Cliente, pk=pk)
    
    # Vendas do cliente
    vendas = Venda.objects.filter(cliente=cliente).order_by('-data_venda')[:10]
    
    # Estatísticas do cliente
    total_vendas = Venda.objects.filter(cliente=cliente, status='finalizada').count()
    valor_total_compras = sum(v.valor_total for v in Venda.objects.filter(cliente=cliente, status='finalizada'))
    
    context = {
        'cliente': cliente,
        'vendas': vendas,
        'total_vendas': total_vendas,
        'valor_total_compras': valor_total_compras,
        'title': f'Cliente: {cliente.nome}'
    }
    
    return render(request, 'core/cliente_detail.html', context)

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
def cliente_edit(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, f'Cliente {cliente.nome} atualizado com sucesso!')
            return redirect('cliente_list')
    else:
        form = ClienteForm(instance=cliente)
    
    return render(request, 'core/cliente_form.html', {'form': form, 'title': f'Editar Cliente: {cliente.nome}'})

@login_required  
def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        nome = cliente.nome
        cliente.delete()
        messages.success(request, f'Cliente {nome} deletado com sucesso!')
        return redirect('cliente_list')
    
    return render(request, 'core/confirm_delete.html', {
        'object': cliente,
        'title': f'Deletar Cliente: {cliente.nome}',
        'cancel_url': 'cliente_list'
    })

@login_required
def categoria_list(request):
    categorias = Categoria.objects.all()
    return render(request, 'core/categoria_list.html', {'categorias': categorias})

@login_required
def categoria_detail(request, pk):
    """Visualizar detalhes de uma categoria"""
    categoria = get_object_or_404(Categoria, pk=pk)
    
    # Produtos da categoria
    produtos = Produto.objects.filter(categoria=categoria, ativo=True)
    total_produtos = produtos.count()
    
    # Valor total do estoque da categoria
    valor_total_estoque = sum(p.valor_total_estoque for p in produtos)
    
    context = {
        'categoria': categoria,
        'produtos': produtos[:10],  # Mostrar apenas os primeiros 10
        'total_produtos': total_produtos,
        'valor_total_estoque': valor_total_estoque,
        'title': f'Categoria: {categoria.nome}'
    }
    
    return render(request, 'core/categoria_detail.html', context)

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
def categoria_edit(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            categoria = form.save()
            messages.success(request, f'Categoria {categoria.nome} atualizada com sucesso!')
            return redirect('categoria_list')
    else:
        form = CategoriaForm(instance=categoria)
    
    return render(request, 'core/categoria_form.html', {'form': form, 'title': f'Editar Categoria: {categoria.nome}'})

@login_required  
def categoria_delete(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        nome = categoria.nome
        categoria.delete()
        messages.success(request, f'Categoria {nome} deletada com sucesso!')
        return redirect('categoria_list')
    
    return render(request, 'core/confirm_delete.html', {
        'object': categoria,
        'title': f'Deletar Categoria: {categoria.nome}',
        'cancel_url': 'categoria_list'
    })

@login_required
def forma_pagamento_list(request):
    formas_pagamento = FormaPagamento.objects.all()
    return render(request, 'core/forma_pagamento_list.html', {'formas_pagamento': formas_pagamento})

@login_required
def forma_pagamento_detail(request, pk):
    """Visualizar detalhes de uma forma de pagamento"""
    forma_pagamento = get_object_or_404(FormaPagamento, pk=pk)
    
    # Vendas com esta forma de pagamento
    vendas = Venda.objects.filter(forma_pagamento=forma_pagamento).order_by('-data_venda')[:10]
    total_vendas = Venda.objects.filter(forma_pagamento=forma_pagamento, status='finalizada').count()
    valor_total = sum(v.valor_total for v in Venda.objects.filter(forma_pagamento=forma_pagamento, status='finalizada'))
    
    # Movimentações com esta forma de pagamento
    movimentacoes = MovimentacaoEstoque.objects.filter(
        forma_pagamento=forma_pagamento
    ).order_by('-data_movimentacao')[:10]
    
    context = {
        'forma_pagamento': forma_pagamento,
        'vendas': vendas,
        'total_vendas': total_vendas,
        'valor_total': valor_total,
        'movimentacoes': movimentacoes,
        'title': f'Forma de Pagamento: {forma_pagamento.nome}'
    }
    
    return render(request, 'core/forma_pagamento_detail.html', context)

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

@login_required
def forma_pagamento_edit(request, pk):
    forma_pagamento = get_object_or_404(FormaPagamento, pk=pk)
    if request.method == 'POST':
        form = FormaPagamentoForm(request.POST, instance=forma_pagamento)
        if form.is_valid():
            forma_pagamento = form.save()
            messages.success(request, f'Forma de pagamento {forma_pagamento.nome} atualizada com sucesso!')
            return redirect('forma_pagamento_list')
    else:
        form = FormaPagamentoForm(instance=forma_pagamento)
    
    return render(request, 'core/forma_pagamento_form.html', {'form': form, 'title': f'Editar Forma de Pagamento: {forma_pagamento.nome}'})

@login_required  
def forma_pagamento_delete(request, pk):
    forma_pagamento = get_object_or_404(FormaPagamento, pk=pk)
    if request.method == 'POST':
        nome = forma_pagamento.nome
        forma_pagamento.delete()
        messages.success(request, f'Forma de pagamento {nome} deletada com sucesso!')
        return redirect('forma_pagamento_list')
    
    return render(request, 'core/confirm_delete.html', {
        'object': forma_pagamento,
        'title': f'Deletar Forma de Pagamento: {forma_pagamento.nome}',
        'cancel_url': 'forma_pagamento_list'
    })


# ===== VIEWS DE VENDAS =====

@login_required
def venda_list(request):
    """Lista todas as vendas"""
    vendas = Venda.objects.select_related('cliente', 'forma_pagamento', 'usuario').prefetch_related('itens__produto')
    
    # Filtros
    status_filter = request.GET.get('status', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    cliente_filter = request.GET.get('cliente', '')
    
    if status_filter:
        vendas = vendas.filter(status=status_filter)
    
    if data_inicio:
        try:
            data_inicio_obj = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            vendas = vendas.filter(data_venda__date__gte=data_inicio_obj)
        except ValueError:
            pass
    
    if data_fim:
        try:
            data_fim_obj = datetime.strptime(data_fim, '%Y-%m-%d').date()
            vendas = vendas.filter(data_venda__date__lte=data_fim_obj)
        except ValueError:
            pass
    
    if cliente_filter:
        vendas = vendas.filter(cliente__nome__icontains=cliente_filter)
    
    # Paginação
    paginator = Paginator(vendas, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Estatísticas
    total_vendas = vendas.count()
    valor_total = sum(v.valor_total for v in vendas)
    
    context = {
        'page_obj': page_obj,
        'vendas': page_obj,
        'total_vendas': total_vendas,
        'valor_total': valor_total,
        'status_filter': status_filter,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'cliente_filter': cliente_filter,
        'clientes': Cliente.objects.filter(ativo=True),
    }
    
    return render(request, 'core/venda_list.html', context)


@login_required
def venda_create(request):
    """Criar nova venda"""
    if request.method == 'POST':
        venda_form = VendaForm(request.POST)
        formset = ItemVendaFormSet(request.POST)  # Inicializar formset sempre que for POST
        
        if venda_form.is_valid():
            with transaction.atomic():
                venda = venda_form.save(commit=False)
                venda.usuario = request.user
                venda.save()
                
                formset = ItemVendaFormSet(request.POST, instance=venda)  # Reatribuir com instance
                
                if formset.is_valid():
                    itens_salvos = []
                    erro_estoque = False
                    
                    # Validar estoque antes de salvar
                    for form in formset:
                        if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                            produto = form.cleaned_data['produto']
                            quantidade = form.cleaned_data['quantidade']
                            
                            if produto.estoque_atual < quantidade:
                                messages.error(request, f'Estoque insuficiente para {produto.nome}. Disponível: {produto.estoque_atual}')
                                erro_estoque = True
                    
                    if not erro_estoque:
                        # Salvar itens e atualizar estoque
                        for form in formset:
                            if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                                item = form.save()
                                itens_salvos.append(item)
                                
                                # Atualizar estoque
                                produto = item.produto
                                produto.estoque_atual -= item.quantidade
                                produto.save()
                                
                                # Criar movimentação de estoque
                                MovimentacaoEstoque.objects.create(
                                    produto=produto,
                                    tipo='saida',
                                    quantidade=item.quantidade,
                                    preco_unitario=item.preco_unitario,
                                    forma_pagamento=venda.forma_pagamento,
                                    observacao=f'Venda {venda.numero_venda}',
                                    usuario=request.user
                                )
                        
                        if itens_salvos:
                            # Se tem cliente, criar conta a receber automaticamente
                            if venda.cliente:
                                ContasReceber.objects.create(
                                    cliente=venda.cliente,
                                    venda=venda,
                                    valor_total=venda.valor_total,
                                    valor_pago=0,  # Inicia sem pagamento
                                    data_vencimento=venda.data_vencimento,
                                    status='aberto',
                                    observacao=f'Venda {venda.numero_venda} - Aguardando pagamento',
                                    usuario=request.user
                                )
                                venda.status = 'aberta'  # Venda fica em aberto para pagamento
                                messages.success(request, f'Venda {venda.numero_venda} criada! Cliente pode pagar em "Contas a Receber". Total: R$ {venda.valor_total:.2f}')
                            else:
                                venda.status = 'finalizada'  # Sem cliente = venda balcão finalizada
                                messages.success(request, f'Venda {venda.numero_venda} finalizada com sucesso! Total: R$ {venda.valor_total:.2f}')
                            
                            venda.save()
                            return redirect('venda_detail', pk=venda.pk)
                        else:
                            venda.delete()
                            messages.error(request, 'Adicione pelo menos um item à venda')
                    else:
                        # Erro de estoque - manter formset para mostrar erros
                        venda.delete()
                else:
                    # Formset inválido - manter formset para mostrar erros
                    venda.delete()
                    messages.error(request, 'Erro nos itens da venda. Verifique os dados informados.')
        # Se venda_form não é válido, formset já foi inicializado no início
    else:
        # Requisição GET - inicializar formulários vazios
        venda_form = VendaForm()
        formset = ItemVendaFormSet()
    
    return render(request, 'core/venda_form.html', {
        'venda_form': venda_form,
        'formset': formset,
        'title': 'Nova Venda'
    })


@login_required
def venda_detail(request, pk):
    """Detalhar venda específica"""
    venda = get_object_or_404(
        Venda.objects.select_related('cliente', 'forma_pagamento', 'usuario')
                    .prefetch_related('itens__produto'), 
        pk=pk
    )
    
    return render(request, 'core/venda_detail.html', {
        'venda': venda,
        'title': f'Venda {venda.numero_venda}'
    })


@login_required
def produto_preco_api(request, pk):
    """API para retornar preço do produto (AJAX)"""
    try:
        produto = Produto.objects.get(pk=pk, ativo=True)
        return JsonResponse({
            'preco_venda': float(produto.preco_venda),
            'estoque_atual': produto.estoque_atual,
            'nome': produto.nome
        })
    except Produto.DoesNotExist:
        return JsonResponse({'error': 'Produto não encontrado'}, status=404)


@login_required
def venda_edit(request, pk):
    """Editar venda existente"""
    venda = get_object_or_404(Venda, pk=pk)
    
    # Vendas canceladas não podem ser editadas
    if venda.status == 'cancelada':
        messages.error(request, 'Vendas canceladas não podem ser editadas.')
        return redirect('venda_detail', pk=pk)
    
    if request.method == 'POST':
        status_anterior = venda.status  # Guardar o status anterior
        venda_form = VendaForm(request.POST, instance=venda)
        
        if venda_form.is_valid():
            with transaction.atomic():
                venda = venda_form.save()
                
                # Verificar se houve mudança de status
                if status_anterior != venda.status:
                    if venda.status == 'finalizada' and status_anterior == 'aberta':
                        # Venda foi finalizada - criar movimentações se necessário
                        for item in venda.itens.all():
                            # Verificar se já existe movimentação para este item
                            movimentacao_existente = MovimentacaoEstoque.objects.filter(
                                produto=item.produto,
                                tipo='saida',
                                quantidade=item.quantidade,
                                observacao=f'Venda {venda.numero_venda}'
                            ).exists()
                            
                            if not movimentacao_existente:
                                MovimentacaoEstoque.objects.create(
                                    produto=item.produto,
                                    tipo='saida',
                                    quantidade=item.quantidade,
                                    preco_unitario=item.preco_unitario,
                                    forma_pagamento=venda.forma_pagamento,
                                    observacao=f'Venda {venda.numero_venda}',
                                    usuario=request.user
                                )
                        messages.success(request, f'Venda {venda.numero_venda} finalizada com sucesso!')
                        
                        # Se tem cliente, criar conta a receber automaticamente
                        if venda.cliente:
                            conta, created = ContasReceber.objects.get_or_create(
                                venda=venda,
                                cliente=venda.cliente,
                                defaults={
                                    'valor_total': venda.valor_total,
                                    'valor_pago': venda.valor_total_pago,
                                    'data_vencimento': venda.data_vencimento,
                                    'usuario': request.user
                                }
                            )
                    
                    elif venda.status == 'aberta' and status_anterior == 'finalizada':
                        # Venda foi reaberta - remover movimentações
                        MovimentacaoEstoque.objects.filter(
                            observacao=f'Venda {venda.numero_venda}',
                            tipo='saida'
                        ).delete()
                        
                        # Restaurar estoque
                        for item in venda.itens.all():
                            produto = item.produto
                            produto.estoque_atual += item.quantidade
                            produto.save()
                        messages.warning(request, f'Venda {venda.numero_venda} reaberta. Estoque restaurado.')
                
                formset = ItemVendaFormSet(request.POST, instance=venda)
                
                if formset.is_valid():
                    # Primeiro, restaurar estoque dos itens que serão removidos/modificados
                    for form in formset.deleted_forms:
                        if form.instance.pk:
                            item = form.instance
                            produto = item.produto
                            produto.estoque_atual += item.quantidade
                            produto.save()
                            
                            # Remover movimentação correspondente
                            movimentacao = MovimentacaoEstoque.objects.filter(
                                produto=produto,
                                tipo='saida',
                                quantidade=item.quantidade,
                                observacao=f'Venda {venda.numero_venda}'
                            ).first()
                            if movimentacao:
                                movimentacao.delete()
                    
                    # Processar itens modificados/novos
                    erro_estoque = False
                    for form in formset:
                        if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                            produto = form.cleaned_data['produto']
                            quantidade_nova = form.cleaned_data['quantidade']
                            
                            # Se é item existente, calcular diferença
                            if form.instance.pk:
                                quantidade_antiga = form.instance.quantidade
                                diferenca = quantidade_nova - quantidade_antiga
                                
                                if diferenca > 0 and produto.estoque_atual < diferenca:
                                    messages.error(request, f'Estoque insuficiente para {produto.nome}. Disponível: {produto.estoque_atual}')
                                    erro_estoque = True
                            else:
                                # Item novo
                                if produto.estoque_atual < quantidade_nova:
                                    messages.error(request, f'Estoque insuficiente para {produto.nome}. Disponível: {produto.estoque_atual}')
                                    erro_estoque = True
                    
                    if not erro_estoque:
                        # Salvar itens e ajustar estoque
                        for form in formset:
                            if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                                item = form.save()
                                produto = item.produto
                                
                                if form.instance.pk and form.instance.pk == item.pk:
                                    # Item editado - ajustar apenas a diferença
                                    if hasattr(form, '_original_quantidade'):
                                        diferenca = item.quantidade - form._original_quantidade
                                        produto.estoque_atual -= diferenca
                                    else:
                                        # Primeira vez editando, usar quantidade total
                                        produto.estoque_atual -= item.quantidade
                                else:
                                    # Item novo
                                    produto.estoque_atual -= item.quantidade
                                    
                                    # Criar movimentação
                                    MovimentacaoEstoque.objects.create(
                                        produto=produto,
                                        tipo='saida',
                                        quantidade=item.quantidade,
                                        preco_unitario=item.preco_unitario,
                                        forma_pagamento=venda.forma_pagamento,
                                        observacao=f'Venda {venda.numero_venda}',
                                        usuario=request.user
                                    )
                                
                                produto.save()
                        
                        messages.success(request, f'Venda {venda.numero_venda} atualizada com sucesso!')
                        return redirect('venda_detail', pk=venda.pk)
                else:
                    messages.error(request, 'Erro nos itens da venda. Verifique os dados informados.')
    else:
        venda_form = VendaForm(instance=venda)
        formset = ItemVendaFormSet(instance=venda)
    
    return render(request, 'core/venda_form.html', {
        'venda_form': venda_form,
        'formset': formset,
        'title': f'Editar Venda {venda.numero_venda}',
        'editing': True
    })


@login_required
def venda_cancel(request, pk):
    """Cancelar/deletar venda"""
    venda = get_object_or_404(Venda, pk=pk)
    
    if request.method == 'POST':
        with transaction.atomic():
            # Se venda está finalizada, restaurar estoque
            if venda.status == 'finalizada':
                for item in venda.itens.all():
                    produto = item.produto
                    produto.estoque_atual += item.quantidade
                    produto.save()
                    
                    # Remover movimentações relacionadas
                    MovimentacaoEstoque.objects.filter(
                        produto=produto,
                        tipo='saida',
                        observacao=f'Venda {venda.numero_venda}'
                    ).delete()
            
            numero_venda = venda.numero_venda
            venda.delete()
            
            messages.success(request, f'Venda {numero_venda} cancelada/deletada com sucesso! Estoque restaurado.')
            return redirect('venda_list')
    
    return render(request, 'core/confirm_delete.html', {
        'object': venda,
        'title': f'Cancelar/Deletar Venda {venda.numero_venda}',
        'cancel_url': 'venda_list',
        'delete_message': 'Esta ação irá cancelar a venda e restaurar o estoque dos produtos.',
        'items_count': venda.itens.count(),
        'valor_total': venda.valor_total
    })


# ============================================================================
# VIEWS DE PAGAMENTOS E CONTAS A RECEBER
# ============================================================================

@login_required
def pagamento_create(request, venda_id):
    """Criar novo pagamento para uma venda"""
    venda = get_object_or_404(Venda, pk=venda_id)
    
    if venda.valor_pendente <= 0:
        messages.error(request, 'Esta venda já está totalmente paga!')
        return redirect('venda_detail', pk=venda.pk)
    
    if request.method == 'POST':
        form = PagamentoForm(request.POST, venda=venda)
        if form.is_valid():
            with transaction.atomic():
                pagamento = form.save(commit=False)
                pagamento.venda = venda
                pagamento.usuario = request.user
                pagamento.save()
                
                # Atualizar status da venda
                venda.atualizar_status_pagamento()
                
                # Se cliente existe, criar/atualizar conta a receber automaticamente
                if venda.cliente:
                    conta, created = ContasReceber.objects.get_or_create(
                        venda=venda,
                        cliente=venda.cliente,
                        defaults={
                            'valor_total': venda.valor_total,
                            'valor_pago': venda.valor_total_pago,
                            'data_vencimento': venda.data_vencimento,
                            'usuario': request.user
                        }
                    )
                    if not created:
                        # Atualizar conta existente
                        conta.valor_pago = venda.valor_total_pago
                        if venda.valor_pendente <= 0:
                            conta.status = 'quitado'
                        elif conta.valor_pago > 0:
                            conta.status = 'parcial'
                        else:
                            conta.status = 'aberto'
                        conta.save()
                
                messages.success(request, f'Pagamento de R$ {pagamento.valor_pago:.2f} registrado com sucesso!')
                return redirect('venda_detail', pk=venda.pk)
    else:
        form = PagamentoForm(venda=venda)
    
    return render(request, 'core/pagamento_form.html', {
        'form': form,
        'venda': venda,
        'title': f'Novo Pagamento - Venda {venda.numero_venda}'
    })


@login_required
def venda_checkout(request, venda_id):
    """Tela de checkout com múltiplas formas de pagamento - permite pagamentos parciais"""
    venda = get_object_or_404(Venda, pk=venda_id)
    
    # Permitir pagamentos para vendas abertas, finalizadas ou com pagamento parcial
    if venda.status not in ['aberta', 'finalizada', 'parcial']:
        messages.error(request, 'Esta venda não pode receber pagamentos!')
        return redirect('venda_detail', pk=venda.pk)
    
    # Verificar se ainda há valor a pagar
    if venda.valor_pendente <= 0:
        messages.info(request, 'Esta venda já está totalmente paga!')
        return redirect('venda_detail', pk=venda.pk)
    
    if request.method == 'POST':
        # Processar múltiplos pagamentos
        formas_pagamento = request.POST.getlist('forma_pagamento')
        valores = request.POST.getlist('valor_pagamento')
        
        # Filtrar valores vazios
        pagamentos_dados = [(f, v) for f, v in zip(formas_pagamento, valores) if f and v and float(v) > 0]
        
        if not pagamentos_dados:
            messages.error(request, 'É necessário informar pelo menos uma forma de pagamento!')
        else:
            total_pagamentos = sum(float(v) for f, v in pagamentos_dados)
            valor_devido = float(venda.valor_pendente)
            
            # Validar se não está pagando mais que o devido
            if total_pagamentos > valor_devido + 0.01:  # Tolerância de 1 centavo
                messages.error(request, 
                    f'Total dos pagamentos (R$ {total_pagamentos:.2f}) não pode ser maior que o valor devido (R$ {valor_devido:.2f})')
            else:
                with transaction.atomic():
                    # Criar pagamentos
                    for forma_id, valor in pagamentos_dados:
                        Pagamento.objects.create(
                            venda=venda,
                            forma_pagamento_id=forma_id,
                            valor_pago=valor,
                            usuario=request.user
                        )
                    
                    # Atualizar status da venda
                    venda.atualizar_status_pagamento()
                    
                    # Se cliente existe, criar/atualizar conta a receber automaticamente
                    if venda.cliente:
                        conta, created = ContasReceber.objects.get_or_create(
                            venda=venda,
                            cliente=venda.cliente,
                            defaults={
                                'valor_total': venda.valor_total,
                                'valor_pago': venda.valor_total_pago,
                                'data_vencimento': venda.data_vencimento,
                                'usuario': request.user
                            }
                        )
                        if not created:
                            # Atualizar conta existente
                            conta.valor_pago = venda.valor_total_pago
                            if venda.valor_pendente <= 0:
                                conta.status = 'quitado'
                            elif conta.valor_pago > 0:
                                conta.status = 'parcial'
                            else:
                                conta.status = 'aberto'
                            conta.save()
                    
                    # Mensagem baseada no status final
                    if venda.valor_pendente <= 0:
                        messages.success(request, f'Venda {venda.numero_venda} totalmente paga! Pagamento de R$ {total_pagamentos:.2f} registrado.')
                    else:
                        messages.success(request, f'Pagamento parcial de R$ {total_pagamentos:.2f} registrado! Restam R$ {venda.valor_pendente:.2f} a pagar.')
                    
                    return redirect('venda_detail', pk=venda.pk)
    
    formas_pagamento = FormaPagamento.objects.filter(ativo=True)
    
    return render(request, 'core/venda_checkout.html', {
        'venda': venda,
        'formas_pagamento': formas_pagamento,
        'title': f'Pagamento - Venda {venda.numero_venda}'
    })


@login_required
def contas_receber_list(request):
    """Lista de contas a receber"""
    contas = ContasReceber.objects.select_related('cliente', 'venda').all()
    
    # Filtros
    cliente_id = request.GET.get('cliente')
    status = request.GET.get('status')
    vencidas = request.GET.get('vencidas')
    
    if cliente_id:
        contas = contas.filter(cliente_id=cliente_id)
    if status:
        contas = contas.filter(status=status)
    if vencidas == 'sim':
        contas = [c for c in contas if c.esta_vencido]
    
    # Paginação
    paginator = Paginator(contas, 20)
    page = request.GET.get('page')
    contas_paginadas = paginator.get_page(page)
    
    # Estatísticas
    todas_contas = ContasReceber.objects.filter(status__in=['aberto', 'parcial'])
    total_em_aberto = sum(c.valor_pendente for c in todas_contas)
    contas_vencidas = [c for c in todas_contas if c.esta_vencido]
    total_vencidas = sum(c.valor_pendente for c in contas_vencidas)
    contas_parciais = ContasReceber.objects.filter(status='parcial')
    quitadas_mes = ContasReceber.objects.filter(
        status='quitado',
        data_criacao__month=timezone.now().month,
        data_criacao__year=timezone.now().year
    )
    
    context = {
        'contas': contas_paginadas,
        'clientes': Cliente.objects.all(),
        'total_em_aberto': total_em_aberto,
        'total_vencidas': total_vencidas,
        'count_vencidas': len(contas_vencidas),
        'contas_parciais': contas_parciais,
        'quitadas_mes': quitadas_mes,
        'title': 'Contas a Receber'
    }
    
    return render(request, 'core/contas_receber_list.html', context)


@login_required
def conta_receber_detail(request, pk):
    """Detalhes de uma conta a receber"""
    conta = get_object_or_404(ContasReceber, pk=pk)
    pagamentos = []
    
    if conta.venda:
        pagamentos = conta.venda.pagamentos.all()
    
    return render(request, 'core/conta_receber_detail.html', {
        'conta': conta,
        'pagamentos': pagamentos,
        'title': f'Conta a Receber - {conta.cliente.nome}'
    })


@login_required
def contas_receber_create(request):
    """Criar nova conta a receber (sem venda vinculada)"""
    if request.method == 'POST':
        form = ContasReceberForm(request.POST)
        if form.is_valid():
            conta = form.save(commit=False)
            conta.usuario = request.user
            conta.save()
            messages.success(request, 'Conta a receber criada com sucesso!')
            return redirect('contas_receber_list')
    else:
        form = ContasReceberForm()
    
    return render(request, 'core/conta_receber_form.html', {
        'form': form,
        'title': 'Nova Conta a Receber'
    })


@login_required
def conta_receber_pagamento(request, pk):
    """Fazer pagamento parcial em conta a receber"""
    conta = get_object_or_404(ContasReceber, pk=pk)
    
    if conta.status == 'quitado':
        messages.error(request, 'Esta conta já está quitada!')
        return redirect('conta_receber_detail', pk=pk)
    
    if request.method == 'POST':
        form = PagamentoContaForm(request.POST, conta=conta)
        if form.is_valid():
            with transaction.atomic():
                valor_pago = form.cleaned_data['valor_pago']
                
                if conta.venda:
                    # Conta vinculada a uma venda - usar modelo Pagamento
                    pagamento = Pagamento.objects.create(
                        venda=conta.venda,
                        forma_pagamento=form.cleaned_data['forma_pagamento'],
                        valor_pago=valor_pago,
                        observacao=form.cleaned_data.get('observacao', ''),
                        usuario=request.user
                    )
                    # Atualizar venda
                    conta.venda.atualizar_status_pagamento()
                else:
                    # Conta avulsa - usar modelo PagamentoConta
                    pagamento = PagamentoConta.objects.create(
                        conta_receber=conta,
                        forma_pagamento=form.cleaned_data['forma_pagamento'],
                        valor_pago=valor_pago,
                        observacao=form.cleaned_data.get('observacao', ''),
                        usuario=request.user
                    )
                
                # Atualizar conta a receber
                conta.valor_pago += valor_pago
                
                # Atualizar status baseado no pagamento
                if conta.valor_pago >= conta.valor_total:
                    conta.status = 'quitado'
                    if conta.venda:
                        conta.venda.status = 'paga'
                        conta.venda.save()
                elif conta.valor_pago > 0:
                    conta.status = 'parcial'
                    if conta.venda:
                        conta.venda.status = 'parcial'
                        conta.venda.save()
                
                conta.save()
                
                valor_restante = conta.valor_pendente
                if valor_restante <= 0:
                    messages.success(request, f'🎉 Conta quitada! Pagamento de R$ {valor_pago:.2f} registrado com sucesso!')
                else:
                    messages.success(request, f'✅ Pagamento de R$ {valor_pago:.2f} registrado! Resta pagar: R$ {valor_restante:.2f}')
                
                return redirect('conta_receber_detail', pk=conta.pk)
                
                # Atualizar conta a receber
                conta.valor_pago += form.cleaned_data['valor_pago']
                
                # Atualizar status baseado no pagamento
                if conta.valor_pago >= conta.valor_total:
                    conta.status = 'quitado'
                    conta.venda.status = 'paga'
                elif conta.valor_pago > 0:
                    conta.status = 'parcial'
                    conta.venda.status = 'parcial'
                
                conta.save()
                conta.venda.save()
                
                valor_restante = conta.valor_pendente
                if valor_restante <= 0:
                    messages.success(request, f'🎉 Conta quitada! Pagamento de R$ {pagamento.valor_pago:.2f} registrado com sucesso!')
                else:
                    messages.success(request, f'✅ Pagamento de R$ {pagamento.valor_pago:.2f} registrado! Resta pagar: R$ {valor_restante:.2f}')
                
                return redirect('conta_receber_detail', pk=conta.pk)
    else:
        form = PagamentoContaForm(conta=conta)
    
    return render(request, 'core/conta_receber_pagamento.html', {
        'form': form,
        'conta': conta,
        'title': f'Pagamento - {conta.cliente.nome}'
    })


@login_required
def pagamento_delete(request, pk):
    """Excluir um pagamento"""
    pagamento = get_object_or_404(Pagamento, pk=pk)
    venda = pagamento.venda
    
    if request.method == 'POST':
        with transaction.atomic():
            pagamento.delete()
            # Atualizar status da venda
            venda.atualizar_status_pagamento()
            
            messages.success(request, 'Pagamento excluído com sucesso!')
            return redirect('venda_detail', pk=venda.pk)
    
    return render(request, 'core/confirm_delete.html', {
        'object': pagamento,
        'title': 'Excluir Pagamento',
        'cancel_url': 'venda_detail',
        'cancel_id': venda.pk
    })
