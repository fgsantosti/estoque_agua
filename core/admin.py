from django.contrib import admin
from .models import Categoria, Produto, MovimentacaoEstoque, Fornecedor, Cliente

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao']
    search_fields = ['nome']

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'codigo', 'categoria', 'estoque_atual', 'estoque_minimo', 'preco_venda', 'ativo']
    list_filter = ['categoria', 'ativo']
    search_fields = ['nome', 'codigo']
    list_editable = ['estoque_atual', 'preco_venda', 'ativo']

@admin.register(MovimentacaoEstoque)
class MovimentacaoEstoqueAdmin(admin.ModelAdmin):
    list_display = ['produto', 'tipo', 'quantidade', 'usuario', 'data_movimentacao']
    list_filter = ['tipo', 'data_movimentacao']
    search_fields = ['produto__nome']
    readonly_fields = ['data_movimentacao']

@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cnpj', 'telefone', 'email', 'ativo']
    list_filter = ['ativo']
    search_fields = ['nome', 'cnpj']

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cpf_cnpj', 'telefone', 'email', 'ativo']
    list_filter = ['ativo']
    search_fields = ['nome', 'cpf_cnpj']
