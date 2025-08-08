# 🛒 Sistema de Vendas - Manual do Usuário

Este documento detalha o funcionamento do **Sistema de Vendas** integrado ao Sistema de Estoque de Água.

## 🌟 Visão Geral

O sistema de vendas funciona como um **PDV (Ponto de Venda)** completo, permitindo:
- Vendas com múltiplos produtos
- Controle automático de estoque
- Cálculos em tempo real
- Histórico completo de transações

## 📋 Como Usar

### 1. 🛒 Criando uma Nova Venda

1. **Acesse:** Menu lateral → "Vendas" → "Nova Venda"
2. **Interface:** Você verá um formulário tipo "caixa de supermercado"

### 2. 📝 Preenchendo os Dados Básicos

- **Cliente:** (Opcional) Selecione um cliente cadastrado
- **Forma de Pagamento:** (Obrigatório) Escolha como será o pagamento
- **Observação:** (Opcional) Adicione comentários sobre a venda

### 3. ➕ Adicionando Produtos

Para cada item da venda:

1. **Selecione o Produto:**
   - Escolha na lista suspensa
   - O preço será preenchido automaticamente
   - Apenas produtos com estoque aparecem na lista

2. **Informe a Quantidade:**
   - Digite quantos itens quer vender
   - O sistema verifica se há estoque suficiente

3. **Confira o Valor:**
   - Total da linha é calculado automaticamente
   - Total geral é atualizado em tempo real

4. **Adicione Mais Itens:**
   - Clique em "Adicionar Item" para novas linhas
   - Ou use uma das 5 linhas vazias já disponíveis

### 4. ✅ Finalizando a Venda

1. **Confira os Dados:**
   - Total geral deve estar correto
   - Pelo menos um produto deve estar selecionado

2. **Clique em "Finalizar Venda":**
   - O sistema valida estoque disponível
   - Reduz automaticamente o estoque dos produtos
   - Cria movimentações de saída no estoque
   - Gera número sequencial para a venda

3. **Visualize o Comprovante:**
   - Página de detalhes da venda é exibida
   - Todos os itens e valores são mostrados
   - Opção de imprimir disponível

## 📊 Visualizando Vendas

### Lista de Vendas
**Acesso:** Menu → "Vendas" → "Vendas"

**Funcionalidades:**
- Lista paginada de todas as vendas
- Filtros por status, cliente, data
- Busca por nome do cliente
- Estatísticas resumidas (total de vendas, valor total)

**Informações Exibidas:**
- Número da venda
- Data e hora
- Cliente (se informado)
- Forma de pagamento
- Quantidade de itens
- Valor total
- Status da venda

### Detalhes da Venda
**Acesso:** Lista de vendas → Clique no ícone 👁️

**Informações Completas:**
- Dados da venda (número, data, vendedor)
- Cliente e forma de pagamento
- Lista detalhada de todos os itens
- Valores individuais e totais
- Data de vencimento (se pagamento à prazo)
- Informações de auditoria

## 📈 Dashboard - Estatísticas de Vendas

O dashboard foi atualizado com métricas de vendas:

### Cards de Estatísticas
- **Vendas Hoje:** Quantidade de vendas realizadas hoje
- **Faturamento Hoje:** Valor total faturado hoje
- **Vendas/Mês:** Total de vendas dos últimos 30 dias
- **Faturamento Mensal:** Card destacado com total mensal

### Seção de Vendas Recentes
- Lista das 5 vendas mais recentes
- Link direto para ver detalhes
- Link para criar nova venda

## 🔧 Funcionalidades Técnicas

### Controle Automático de Estoque
- Quando uma venda é finalizada:
  - Estoque dos produtos é reduzido automaticamente
  - Movimentações de "saída" são criadas no histórico
  - Sistema impede vendas sem estoque suficiente

### Numeração Sequencial
- Cada venda recebe número único: VD000001, VD000002, etc.
- Numeração é automática e não pode ser alterada

### Validações de Segurança
- Verificação de estoque antes de finalizar
- Pelo menos um item obrigatório
- Transações atômicas (tudo ou nada)

### Status da Venda
- **Aberta:** Venda em criação (não finalizada)
- **Finalizada:** Venda concluída com sucesso
- **Cancelada:** Venda cancelada (funcionalidade futura)

## 🚨 Situações Especiais

### Estoque Insuficiente
- Sistema bloqueia a venda se não houver estoque
- Mensagem de erro específica é exibida
- Venda não é finalizada até resolver o problema

### Produtos Inativos
- Produtos marcados como "inativo" não aparecem na lista
- Produtos com estoque zero não aparecem na lista

### Dados Obrigatórios
- Forma de pagamento é obrigatória
- Pelo menos um produto deve ser selecionado
- Quantidade deve ser maior que zero

## 📱 Interface Responsiva

O sistema de vendas funciona em:
- **Desktop:** Formulário completo com várias colunas
- **Tablet:** Layout adaptado para toque
- **Mobile:** Interface otimizada para tela pequena

## 🎯 Dicas de Uso

### Para Melhor Performance:
1. **Configure Estoque Mínimo:** Defina alertas para cada produto
2. **Use Clientes:** Facilita relatórios e histórico
3. **Categorize Produtos:** Organiza melhor o sistema
4. **Configure Formas de Pagamento:** Inclua prazos corretos

### Para Relatórios:
1. **Use Filtros:** Na lista de vendas para períodos específicos
2. **Exporte Dados:** Via painel administrativo
3. **Monitore Dashboard:** Estatísticas em tempo real

---

## 🛠️ Desenvolvido Para:

- **Distribuidoras de Água**
- **Comércios de Bebidas**
- **Pequenos Mercados**
- **Lanchonetes e Restaurantes**

O sistema combina **simplicidade** de uso com **poder** de gestão, oferecendo uma solução completa para controle de vendas e estoque.

**🚰 Sistema de Estoque de Água - Vendas Inteligentes** 
