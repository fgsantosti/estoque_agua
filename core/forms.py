from django import forms
from django.forms import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import (Produto, MovimentacaoEstoque, Fornecedor, Cliente, Categoria, 
                    FormaPagamento, Venda, ItemVenda, Pagamento, ContasReceber)

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'categoria', 'codigo', 'preco_venda', 'preco_custo', 
                 'estoque_minimo', 'estoque_atual', 'unidade_medida', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'preco_venda': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'preco_custo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'estoque_minimo': forms.NumberInput(attrs={'class': 'form-control'}),
            'estoque_atual': forms.NumberInput(attrs={'class': 'form-control'}),
            'unidade_medida': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('nome', css_class='form-group col-md-6 mb-0'),
                Column('categoria', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('codigo', css_class='form-group col-md-4 mb-0'),
                Column('unidade_medida', css_class='form-group col-md-4 mb-0'),
                Column('ativo', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('preco_custo', css_class='form-group col-md-6 mb-0'),
                Column('preco_venda', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('estoque_atual', css_class='form-group col-md-6 mb-0'),
                Column('estoque_minimo', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Salvar', css_class='btn btn-primary')
        )

class MovimentacaoEstoqueForm(forms.ModelForm):
    class Meta:
        model = MovimentacaoEstoque
        fields = ['produto', 'tipo', 'quantidade', 'preco_unitario', 'forma_pagamento', 'observacao']
        widgets = {
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
            'preco_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'produto',
            Row(
                Column('tipo', css_class='form-group col-md-6 mb-0'),
                Column('quantidade', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('preco_unitario', css_class='form-group col-md-6 mb-0'),
                Column('forma_pagamento', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'observacao',
            Submit('submit', 'Registrar Movimentação', css_class='btn btn-success')
        )

class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = ['nome', 'cnpj', 'telefone', 'email', 'endereco', 'ativo']
        widgets = {
            'endereco': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Salvar'))

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cpf_cnpj', 'telefone', 'email', 'endereco', 'ativo']
        widgets = {
            'endereco': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Salvar'))

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'descricao']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Salvar'))

class FormaPagamentoForm(forms.ModelForm):
    class Meta:
        model = FormaPagamento
        fields = ['nome', 'descricao', 'prazo_recebimento', 'ativo']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
            'prazo_recebimento': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'nome',
            'descricao',
            Row(
                Column('prazo_recebimento', css_class='form-group col-md-6 mb-0'),
                Column('ativo', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Salvar', css_class='btn btn-primary')
        )


class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['cliente', 'forma_pagamento', 'data_venda', 'observacao', 'status']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'forma_pagamento': forms.Select(attrs={'class': 'form-control'}),
            'data_venda': forms.DateTimeInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Definir formato de entrada
        self.fields['data_venda'].input_formats = ['%Y-%m-%dT%H:%M']
        
        # Filtrar apenas formas de pagamento ativas
        self.fields['forma_pagamento'].queryset = FormaPagamento.objects.filter(ativo=True)
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('data_venda', css_class='form-group col-md-6 mb-0'),
                Column('status', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('cliente', css_class='form-group col-md-6 mb-0'),
                Column('forma_pagamento', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'observacao',
            Submit('submit', 'Salvar Venda', css_class='btn btn-success btn-lg')
        )

    def clean_data_venda(self):
        """Validar data da venda"""
        data_venda = self.cleaned_data.get('data_venda')
        if data_venda:
            from django.utils import timezone
            agora = timezone.now()
            
            # Permitir até 1 hora no futuro para compensar diferenças de fuso horário
            if data_venda > agora + timezone.timedelta(hours=1):
                raise forms.ValidationError("A data da venda não pode estar no futuro.")
        
        return data_venda


class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = ['forma_pagamento', 'valor_pago', 'observacao']
        widgets = {
            'forma_pagamento': forms.Select(attrs={'class': 'form-control'}),
            'valor_pago': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'placeholder': '0.00'
            }),
            'observacao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Observações do pagamento (opcional)'
            })
        }
    
    def __init__(self, *args, **kwargs):
        self.venda = kwargs.pop('venda', None)
        super().__init__(*args, **kwargs)
        
        # Se temos a venda, calcular valor máximo permitido
        if self.venda:
            valor_pendente = self.venda.valor_pendente
            self.fields['valor_pago'].widget.attrs.update({
                'max': str(valor_pendente),
                'placeholder': f'Máximo: R$ {valor_pendente:.2f}'
            })
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'forma_pagamento',
            'valor_pago',
            'observacao',
            Submit('submit', 'Registrar Pagamento', css_class='btn btn-success')
        )
    
    def clean_valor_pago(self):
        valor = self.cleaned_data.get('valor_pago')
        if self.venda and valor:
            if valor > self.venda.valor_pendente:
                raise forms.ValidationError(
                    f'Valor não pode ser maior que o pendente: R$ {self.venda.valor_pendente:.2f}'
                )
        return valor


class ContasReceberForm(forms.ModelForm):
    class Meta:
        model = ContasReceber
        fields = ['cliente', 'valor_total', 'data_vencimento', 'observacao']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'data_vencimento': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'valor_total': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01'
            }),
            'observacao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'cliente',
            'valor_total',
            'data_vencimento',
            'observacao',
            Submit('submit', 'Criar Conta a Receber', css_class='btn btn-success')
        )

class ItemVendaForm(forms.ModelForm):
    class Meta:
        model = ItemVenda
        fields = ['produto', 'quantidade', 'preco_unitario']
        widgets = {
            'produto': forms.Select(attrs={
                'class': 'form-control',
                'onchange': 'updatePrice(this)'
            }),
            'quantidade': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'onchange': 'updateRowTotal(this)'
            }),
            'preco_unitario': forms.NumberInput(attrs={
                'class': 'form-control', 
                'step': '0.01',
                'onchange': 'updateRowTotal(this)'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['produto'].queryset = Produto.objects.filter(ativo=True, estoque_atual__gt=0)
        self.fields['produto'].empty_label = "Selecione um produto..."
        
        # Definir preço inicial se produto já selecionado
        try:
            if self.instance and self.instance.pk and self.instance.produto:
                self.fields['preco_unitario'].initial = self.instance.produto.preco_venda
        except:
            # Ignorar se não há produto associado (formulário vazio)
            pass


# Formset para múltiplos itens da venda
ItemVendaFormSet = inlineformset_factory(
    Venda, ItemVenda, 
    form=ItemVendaForm,
    extra=5,  # 5 linhas vazias por padrão
    can_delete=True,
    min_num=1,  # Pelo menos 1 item obrigatório
    validate_min=True
)


class PagamentoContaForm(forms.Form):
    """Formulário para pagamento em contas a receber"""
    forma_pagamento = forms.ModelChoiceField(
        queryset=FormaPagamento.objects.filter(ativo=True),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Forma de Pagamento',
        empty_label="Selecione a forma de pagamento..."
    )
    valor_pago = forms.DecimalField(
        max_digits=10, 
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0.01',
            'placeholder': '0,00'
        }),
        label='Valor do Pagamento'
    )
    observacao = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Observações do pagamento (opcional)'
        }),
        label='Observações'
    )
    
    def __init__(self, *args, **kwargs):
        self.conta = kwargs.pop('conta', None)
        super().__init__(*args, **kwargs)
        
        if self.conta:
            valor_pendente = self.conta.valor_pendente
            self.fields['valor_pago'].widget.attrs.update({
                'max': str(valor_pendente),
                'placeholder': f'Máximo: R$ {valor_pendente:.2f}'
            })
            self.fields['valor_pago'].help_text = f'Valor pendente: R$ {valor_pendente:.2f}'
    
    def clean_valor_pago(self):
        valor = self.cleaned_data.get('valor_pago')
        if self.conta and valor:
            if valor > self.conta.valor_pendente:
                raise forms.ValidationError(
                    f'Valor não pode ser maior que o pendente: R$ {self.conta.valor_pendente:.2f}'
                )
            if valor <= 0:
                raise forms.ValidationError('Valor deve ser maior que zero')
        return valor
