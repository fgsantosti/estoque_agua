from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # Produtos
    path('produtos/', views.produto_list, name='produto_list'),
    path('produtos/novo/', views.produto_create, name='produto_create'),
    path('produtos/<int:pk>/editar/', views.produto_edit, name='produto_edit'),
    path('produtos/<int:pk>/deletar/', views.produto_delete, name='produto_delete'),

    # Movimentações
    path('movimentacoes/', views.movimentacao_list, name='movimentacao_list'),
    path('movimentacoes/nova/', views.movimentacao_create,
         name='movimentacao_create'),

    # Fornecedores
    path('fornecedores/', views.fornecedor_list, name='fornecedor_list'),
    path('fornecedores/novo/', views.fornecedor_create, name='fornecedor_create'),
    path('fornecedores/<int:pk>/editar/', views.fornecedor_edit, name='fornecedor_edit'),
    path('fornecedores/<int:pk>/deletar/', views.fornecedor_delete, name='fornecedor_delete'),

    # Clientes
    path('clientes/', views.cliente_list, name='cliente_list'),
    path('clientes/novo/', views.cliente_create, name='cliente_create'),
    path('clientes/<int:pk>/editar/', views.cliente_edit, name='cliente_edit'),
    path('clientes/<int:pk>/deletar/', views.cliente_delete, name='cliente_delete'),

    # Categorias
    path('categorias/', views.categoria_list, name='categoria_list'),
    path('categorias/nova/', views.categoria_create, name='categoria_create'),
    path('categorias/<int:pk>/editar/', views.categoria_edit, name='categoria_edit'),
    path('categorias/<int:pk>/deletar/', views.categoria_delete, name='categoria_delete'),

    # Formas de Pagamento
    path('formas-pagamento/', views.forma_pagamento_list, name='forma_pagamento_list'),
    path('formas-pagamento/nova/', views.forma_pagamento_create, name='forma_pagamento_create'),
    path('formas-pagamento/<int:pk>/editar/', views.forma_pagamento_edit, name='forma_pagamento_edit'),
    path('formas-pagamento/<int:pk>/deletar/', views.forma_pagamento_delete, name='forma_pagamento_delete'),
]
