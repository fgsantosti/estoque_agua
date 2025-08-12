# Exemplos de Uso do Comando criar_sistema_completo.py

O comando `criar_sistema_completo.py` foi atualizado para incluir as novas funcionalidades do sistema de estoque de água. Aqui estão alguns exemplos de como utilizá-lo:

## Comandos Básicos

### 1. Criar sistema completo com dados padrão
```bash
python manage.py criar_sistema_completo
```
Este comando cria:
- Dados base (categorias, produtos, clientes, fornecedores, formas de pagamento)
- 15 vendas de exemplo
- 10 contas a receber avulsas

### 2. Limpar tudo e recriar
```bash
python manage.py criar_sistema_completo --clear
```
⚠️ **ATENÇÃO**: Este comando remove TODOS os dados existentes antes de criar novos!

### 3. Criar apenas vendas
```bash
python manage.py criar_sistema_completo --only-vendas
```
Útil quando você já tem produtos e clientes cadastrados.

## Comandos Avançados

### 4. Personalizar quantidades
```bash
python manage.py criar_sistema_completo --vendas 25 --contas 20
```
Cria 25 vendas e 20 contas a receber.

### 5. Incluir pagamentos de exemplo
```bash
python manage.py criar_sistema_completo --pagamentos
```
Além dos dados básicos, cria também:
- Pagamentos para algumas vendas (70% das vendas com cliente)
- Pagamentos para contas a receber avulsas (60% das contas)

### 6. Sistema completo com muitos dados
```bash
python manage.py criar_sistema_completo --clear --vendas 50 --contas 30 --pagamentos
```
Limpa tudo e cria um sistema completo com:
- 50 vendas
- 30 contas a receber
- Pagamentos de exemplo
- Todos os dados base

## Novidades do Comando Atualizado

### ✨ Novas Models Incluídas
- **Pagamento**: Pagamentos de vendas com múltiplas formas de pagamento
- **ContasReceber**: Controle de contas a receber de clientes
- **PagamentoConta**: Pagamentos diretos em contas avulsas

### 🎯 Melhorias na Geração de Dados

#### Vendas Mais Realistas:
- Vendas com e sem cliente (80% com cliente)
- Status automático baseado na forma de pagamento:
  - Pagamento à vista sem cliente: `finalizada`
  - Pagamento a prazo com cliente: cria conta a receber automaticamente
  - Diferentes status: `aberta`, `finalizada`, `paga`

#### Contas a Receber Diversificadas:
- Contas avulsas (não vinculadas a vendas)
- Diferentes status: `aberto`, `parcial`, `vencido`, `quitado`
- Algumas contas já vencidas para testes
- Valores entre R$ 50,00 e R$ 500,00

#### Pagamentos Realistas:
- 70% das vendas com cliente recebem pagamentos
- 60% das contas avulsas recebem pagamentos
- Pagamentos parciais e totais
- Diferentes formas de pagamento
- Datas realistas (alguns dias após venda/conta)

#### Formas de Pagamento Expandidas:
- Dinheiro (à vista)
- PIX (à vista)
- Cartão de débito (à vista)
- Cartão de crédito (30 dias)
- Boleto 15 dias
- Boleto 30 dias
- Boleto 60 dias
- Crediário 30 dias

### 📊 Estatísticas Detalhadas
O comando agora mostra estatísticas completas:
- Categorias, Produtos, Clientes, Fornecedores
- Formas de Pagamento
- Vendas e Movimentações de Estoque
- **NOVO**: Contas a Receber
- **NOVO**: Pagamentos de Vendas
- **NOVO**: Pagamentos de Contas

## Casos de Uso Recomendados

### Para Desenvolvimento:
```bash
python manage.py criar_sistema_completo --clear --vendas 30 --contas 15 --pagamentos
```

### Para Testes de Performance:
```bash
python manage.py criar_sistema_completo --clear --vendas 100 --contas 50 --pagamentos
```

### Para Demo/Apresentação:
```bash
python manage.py criar_sistema_completo --clear --vendas 20 --contas 10 --pagamentos
```

### Para Adicionar Mais Dados:
```bash
python manage.py criar_sistema_completo --only-vendas --vendas 20
python manage.py criar_sistema_completo --pagamentos  # Adiciona pagamentos aos dados existentes
```

## ⚠️ Considerações Importantes

1. **Backup**: Sempre faça backup antes de usar `--clear`
2. **Estoque**: Os produtos terão estoque reduzido após as vendas
3. **Usuários**: O comando não exclui usuários por segurança
4. **Performance**: Para muitos dados (>100 vendas), o comando pode demorar alguns minutos
5. **Dados Realistas**: Os dados são gerados para parecer com situações reais de negócio

## 🛠️ Troubleshooting

Se encontrar erros:
1. Verifique se as migrations estão aplicadas: `python manage.py migrate`
2. Certifique-se que existe pelo menos um usuário no sistema
3. Para problemas de estoque, use `--clear` para resetar tudo
4. Verifique as permissões do banco de dados

---

Este comando é ideal para desenvolvimento, testes e demonstrações do sistema de estoque de água! 🚰💧
