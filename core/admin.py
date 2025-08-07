from django.contrib import admin
from .models import Categoria, Produto, MovimentacaoEstoque, Fornecedor, Cliente, FormaPagamento, Venda, ItemVenda

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
    list_display = ['produto', 'tipo', 'quantidade', 'forma_pagamento', 'usuario', 'data_movimentacao']
    list_filter = ['tipo', 'forma_pagamento', 'data_movimentacao']
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

@admin.register(FormaPagamento)
class FormaPagamentoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'prazo_recebimento', 'ativo', 'data_criacao']
    list_filter = ['ativo', 'prazo_recebimento']
    search_fields = ['nome']
    list_editable = ['ativo']


class ItemVendaInline(admin.TabularInline):
    model = ItemVenda
    extra = 1
    fields = ['produto', 'quantidade', 'preco_unitario', 'valor_total']
    readonly_fields = ['valor_total']

    def valor_total(self, obj):
        if obj.quantidade and obj.preco_unitario:
            return f"R$ {obj.valor_total:.2f}"
        return "R$ 0,00"
    valor_total.short_description = "Total"


@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ['numero_venda', 'data_venda', 'cliente', 'forma_pagamento', 'total_itens', 'valor_total_display', 'status', 'usuario']
    list_filter = ['status', 'forma_pagamento', 'data_venda', 'usuario']
    search_fields = ['numero_venda', 'cliente__nome', 'usuario__username']
    readonly_fields = ['numero_venda', 'data_criacao', 'data_atualizacao', 'valor_total_display']
    inlines = [ItemVendaInline]
    
    fieldsets = (
        ('Informações da Venda', {
            'fields': ('numero_venda', 'status', 'data_venda')
        }),
        ('Cliente e Pagamento', {
            'fields': ('cliente', 'forma_pagamento')
        }),
        ('Observações', {
            'fields': ('observacao', 'usuario')
        }),
        ('Sistema', {
            'fields': ('data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )

    def valor_total_display(self, obj):
        return f"R$ {obj.valor_total:.2f}"
    valor_total_display.short_description = "Valor Total"
    valor_total_display.admin_order_field = 'valor_total'

    def total_itens(self, obj):
        return obj.total_itens
    total_itens.short_description = "Itens"

    def save_model(self, request, obj, form, change):
        if not change:  # Novo objeto
            obj.usuario = request.user
        super().save_model(request, obj, form, change)
