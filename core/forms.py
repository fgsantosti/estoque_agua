from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import Produto, MovimentacaoEstoque, Fornecedor, Cliente, Categoria

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
    data_movimentacao = forms.DateTimeField(
        label='Data da Movimentação',
        widget=forms.DateTimeInput(
            attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            },
            format='%Y-%m-%dT%H:%M'
        ),
        input_formats=['%Y-%m-%dT%H:%M'],
        required=False,
        help_text='Deixe em branco para usar data/hora atual'
    )

    class Meta:
        model = MovimentacaoEstoque
        fields = ['produto', 'tipo', 'quantidade', 'preco_unitario', 'data_movimentacao', 'observacao']
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
                Column('data_movimentacao', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'observacao',
            Submit('submit', 'Registrar Movimentação', css_class='btn btn-success')
        )

    def clean_data_movimentacao(self):
        data = self.cleaned_data.get('data_movimentacao')
        if not data:
            from django.utils import timezone
            return timezone.now()
        return data

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

class MovimentacaoFiltroForm(forms.Form):
    data_inicio = forms.DateField(
        label='Data Início',
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date'
            }
        ),
        required=False
    )
    data_fim = forms.DateField(
        label='Data Fim',
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date'
            }
        ),
        required=False
    )
    produto = forms.ModelChoiceField(
        queryset=None,
        label='Produto',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
        empty_label='Todos os produtos'
    )
    tipo = forms.ChoiceField(
        choices=[('', 'Todos os tipos')] + MovimentacaoEstoque.TIPO_CHOICES,
        label='Tipo',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import Produto
        self.fields['produto'].queryset = Produto.objects.filter(ativo=True).order_by('nome')
        # Define data padrão para últimos 30 dias se não informado
        from datetime import date, timedelta
        if not self.data.get('data_fim'):
            self.fields['data_fim'].initial = date.today()
        if not self.data.get('data_inicio'):
            self.fields['data_inicio'].initial = date.today() - timedelta(days=30)
