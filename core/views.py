from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q, F
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db import transaction
from .models import Produto, MovimentacaoEstoque, Fornecedor, Cliente, Categoria, FormaPagamento, Venda, ItemVenda
from .forms import ProdutoForm, MovimentacaoEstoqueForm, FornecedorForm, ClienteForm, CategoriaForm, FormaPagamentoForm, VendaForm, ItemVendaFormSet
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
        
        if venda_form.is_valid():
            with transaction.atomic():
                venda = venda_form.save(commit=False)
                venda.usuario = request.user
                venda.save()
                
                formset = ItemVendaFormSet(request.POST, instance=venda)
                
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
                            venda.status = 'finalizada'
                            venda.save()
                            messages.success(request, f'Venda {venda.numero_venda} finalizada com sucesso! Total: R$ {venda.valor_total:.2f}')
                            return redirect('venda_detail', pk=venda.pk)
                        else:
                            venda.delete()
                            messages.error(request, 'Adicione pelo menos um item à venda')
                    else:
                        venda.delete()
                else:
                    venda.delete()
                    messages.error(request, 'Erro nos itens da venda. Verifique os dados informados.')
    else:
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
