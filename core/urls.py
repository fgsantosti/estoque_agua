from django.urls import path

from . import views

urlpatterns = [
    # Homepage pública
    path('', views.homepage, name='homepage'),
    
    # Dashboard do sistema (requer login)
    path('sistema/', views.dashboard, name='dashboard'),

    # Produtos
    path('produtos/', views.produto_list, name='produto_list'),
    path('produtos/novo/', views.produto_create, name='produto_create'),
    path('produtos/<int:pk>/', views.produto_detail, name='produto_detail'),
    path('produtos/<int:pk>/editar/', views.produto_edit, name='produto_edit'),
    path('produtos/<int:pk>/deletar/', views.produto_delete, name='produto_delete'),

    # Movimentações
    path('movimentacoes/', views.movimentacao_list, name='movimentacao_list'),
    path('movimentacoes/nova/', views.movimentacao_create,
         name='movimentacao_create'),
    path('movimentacoes/<int:pk>/', views.movimentacao_detail, name='movimentacao_detail'),
    path('movimentacoes/<int:pk>/editar/', views.movimentacao_edit, name='movimentacao_edit'),
    path('movimentacoes/<int:pk>/deletar/', views.movimentacao_delete, name='movimentacao_delete'),

    # Fornecedores
    path('fornecedores/', views.fornecedor_list, name='fornecedor_list'),
    path('fornecedores/novo/', views.fornecedor_create, name='fornecedor_create'),
    path('fornecedores/<int:pk>/', views.fornecedor_detail, name='fornecedor_detail'),
    path('fornecedores/<int:pk>/editar/', views.fornecedor_edit, name='fornecedor_edit'),
    path('fornecedores/<int:pk>/deletar/', views.fornecedor_delete, name='fornecedor_delete'),

    # Clientes
    path('clientes/', views.cliente_list, name='cliente_list'),
    path('clientes/novo/', views.cliente_create, name='cliente_create'),
    path('clientes/<int:pk>/', views.cliente_detail, name='cliente_detail'),
    path('clientes/<int:pk>/editar/', views.cliente_edit, name='cliente_edit'),
    path('clientes/<int:pk>/deletar/', views.cliente_delete, name='cliente_delete'),

    # Categorias
    path('categorias/', views.categoria_list, name='categoria_list'),
    path('categorias/nova/', views.categoria_create, name='categoria_create'),
    path('categorias/<int:pk>/', views.categoria_detail, name='categoria_detail'),
    path('categorias/<int:pk>/editar/', views.categoria_edit, name='categoria_edit'),
    path('categorias/<int:pk>/deletar/', views.categoria_delete, name='categoria_delete'),

    # Formas de Pagamento
    path('formas-pagamento/', views.forma_pagamento_list, name='forma_pagamento_list'),
    path('formas-pagamento/nova/', views.forma_pagamento_create, name='forma_pagamento_create'),
    path('formas-pagamento/<int:pk>/', views.forma_pagamento_detail, name='forma_pagamento_detail'),
    path('formas-pagamento/<int:pk>/editar/', views.forma_pagamento_edit, name='forma_pagamento_edit'),
    path('formas-pagamento/<int:pk>/deletar/', views.forma_pagamento_delete, name='forma_pagamento_delete'),

    # Vendas
    path('vendas/', views.venda_list, name='venda_list'),
    path('vendas/nova/', views.venda_create, name='venda_create'),
    path('vendas/<int:pk>/', views.venda_detail, name='venda_detail'),
    path('vendas/<int:pk>/editar/', views.venda_edit, name='venda_edit'),
    path('vendas/<int:pk>/cancelar/', views.venda_cancel, name='venda_cancel'),
    
    # Pagamentos
    path('vendas/<int:venda_id>/checkout/', views.venda_checkout, name='venda_checkout'),
    path('vendas/<int:venda_id>/pagamento/', views.pagamento_create, name='pagamento_create'),
    path('pagamentos/<int:pk>/deletar/', views.pagamento_delete, name='pagamento_delete'),
    
    # Contas a Receber
    path('contas-receber/', views.contas_receber_list, name='contas_receber_list'),
    path('contas-receber/nova/', views.contas_receber_create, name='contas_receber_create'),
    path('contas-receber/<int:pk>/', views.conta_receber_detail, name='conta_receber_detail'),
    path('contas-receber/<int:pk>/pagamento/', views.conta_receber_pagamento, name='conta_receber_pagamento'),
    
    # APIs
    path('api/produto/<int:pk>/preco/', views.produto_preco_api, name='produto_preco_api'),
]
