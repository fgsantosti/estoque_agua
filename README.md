# 🚰 Sistema de Estoque de Água

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2.7-green.svg)](https://djangoproject.com)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple.svg)](https://getbootstrap.com)
[![License](https://img.shields.io/badge/License-MIT-orange.svg)](LICENSE)

Sistema completo de gerenciamento de estoque e vendas para distribuidoras de água, desenvolvido em Django com interface moderna e responsiva.

## 🎯 **Versão Atual: 2.1 (Dezembro 2025)**

### 🆕 Últimas Atualizações
- ✨ **Sistema de Vendas PDV** com múltiplos itens
- 💰 **Controle Financeiro** com valores e resumos em movimentações  
- 📊 **Dashboard Aprimorado** com métricas de vendas e faturamento
- 🧾 **Comprovantes de Venda** com impressão
- 📈 **Relatórios Avançados** por período e forma de pagamento

## ✨ Funcionalidades Principais

### 🛒 Sistema de Vendas (PDV)
- **Interface tipo Caixa:** Similar a um ponto de venda real
- **Múltiplos Itens:** Uma venda pode conter vários produtos diferentes
- **Cálculos Automáticos:** Preços e totais em tempo real
- **Controle de Estoque:** Redução automática ao finalizar venda
- **Numeração Sequencial:** Controle único para cada venda
- **Comprovantes Detalhados:** Visualização e impressão completa

### 📊 Dashboard Inteligente
- **Estatísticas em Tempo Real:** Estoque, vendas e faturamento
- **Métricas de Vendas:** Vendas do dia, mês e totais acumulados
- **Alertas de Estoque:** Produtos com estoque baixo destacados
- **Movimentações Recentes:** Últimas transações do sistema
- **Vendas Recentes:** Histórico das últimas vendas realizadas
- **Valor Total do Estoque:** Cálculo automático do patrimônio

### 📦 Gestão Completa
- **Produtos:** CRUD completo com categorias e preços
- **Clientes:** Cadastro de pessoas físicas e jurídicas
- **Fornecedores:** Gestão de parceiros comerciais
- **Categorias:** Organização hierárquica de produtos
- **Formas de Pagamento:** Controle de prazos e condições

### 💰 Controle Financeiro
- **Movimentações com Valores:** Controle de custos por transação
- **Resumos por Período:** Totalizadores automáticos
- **Relatórios de Faturamento:** Vendas por forma de pagamento
- **Controle de Preços:** Margem entre custo e venda

### � Recursos Técnicos
- **Interface Responsiva:** Bootstrap 5 para todos os dispositivos
- **Design Moderno:** Gradientes e animações suaves
- **Segurança:** Autenticação Django e proteção CSRF
- **Performance:** Consultas otimizadas e cache inteligente

## 🛠️ Tecnologias e Dependências

### Backend
- **Django 4.2.7** - Framework web robusto e seguro
- **Python 3.13** - Linguagem principal
- **SQLite** - Banco de dados para desenvolvimento
- **Python-decouple** - Gerenciamento de configurações

### Frontend
- **Bootstrap 5** - Framework CSS responsivo  
- **Font Awesome** - Ícones e elementos visuais
- **JavaScript Vanilla** - Interatividade sem dependências externas

### Formulários e Interface
- **Django Crispy Forms** - Renderização avançada de formulários
- **Crispy Bootstrap 5** - Integração com Bootstrap
- **Pillow** - Processamento de imagens

### Estrutura do Banco de Dados
- **8 Modelos Principais:** Categoria, Produto, Cliente, Fornecedor, FormaPagamento, MovimentacaoEstoque, Venda, ItemVenda
- **Relacionamentos Otimizados:** ForeignKeys com select_related para performance
- **Campos Calculados:** Propriedades automáticas para totais e estatísticas

## 🚀 Instalação e Configuração

### ⚡ Método Rápido: Script Automático (Recomendado)

```bash
# 1. Clone ou baixe o projeto
git clone <repository-url>
cd estoque_agua

# 2. Execute o script de configuração completa
chmod +x setup_django.sh
./setup_django.sh
```

O script automático executa:
- ✅ Criação do ambiente virtual Python
- ✅ Instalação de todas as dependências
- ✅ Configuração do banco de dados
- ✅ Criação de dados de exemplo
- ✅ Verificação de funcionalidades
- ✅ Inicialização do servidor

### 🔧 Método Manual: Passo a Passo

```bash
# 1. Criar e ativar ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 2. Atualizar pip e instalar dependências
pip install --upgrade pip
pip install -r requirements.txt

# 3. Configurar banco de dados
python manage.py makemigrations
python manage.py migrate

# 4. Criar sistema completo com dados de exemplo
python manage.py criar_sistema_completo

# 5. Coletar arquivos estáticos
python manage.py collectstatic --noinput

# 6. Iniciar servidor de desenvolvimento
python manage.py runserver
```

### 🐳 Opção Docker (Futuro)
```bash
# Em desenvolvimento - Docker Compose
docker-compose up --build
```

## 🛒 Sistema de Vendas - Guia Completo

### 🌟 Principais Características
- **Interface PDV Profissional:** Semelhante a sistemas de supermercado
- **Múltiplos Produtos:** Até 10+ itens diferentes por venda
- **Validação de Estoque:** Só permite venda com estoque disponível
- **Cálculos Inteligentes:** Preços e totais atualizados automaticamente
- **Controle Automático:** Reduz estoque ao finalizar venda
- **Numeração Única:** Cada venda recebe número sequencial
- **Comprovante Completo:** Visualização detalhada com opção de impressão

### 📋 Como Realizar uma Venda

#### 1. **Iniciar Nova Venda**
- Acesse: `Menu Lateral → Vendas → Nova Venda`
- Interface clara tipo "caixa registradora"

#### 2. **Preencher Dados Básicos**
- **Cliente:** (Opcional) Selecione da lista cadastrada
- **Forma de Pagamento:** (Obrigatório) À vista, cartão, boleto, etc.
- **Observações:** (Opcional) Comentários sobre a venda

#### 3. **Adicionar Produtos**
Para cada item:
- **Selecionar Produto:** Lista suspensa com produtos em estoque
- **Preço Automático:** Preenchido automaticamente do cadastro
- **Informar Quantidade:** Digite a quantidade desejada
- **Validação:** Sistema verifica disponibilidade em estoque
- **Total da Linha:** Calculado automaticamente (Qtd × Preço)

#### 4. **Adicionar Mais Itens**
- **Múltiplas Linhas:** Use as 5 linhas pré-carregadas
- **Botão "Adicionar Item":** Para mais linhas dinamicamente
- **Total Geral:** Soma automática de todos os itens

#### 5. **Finalizar Venda**
- **Revisar Dados:** Conferir produtos, quantidades e total
- **Botão "Finalizar Venda":** Confirma e processa a transação
- **Resultado:** Redução automática do estoque
- **Comprovante:** Geração automática para visualização/impressão

### 📊 Acompanhamento de Vendas

#### **No Dashboard:**
- **Vendas Hoje:** Quantidade e valor faturado no dia atual
- **Vendas do Mês:** Total dos últimos 30 dias
- **Faturamento:** Valores totais por período selecionado
- **Vendas Recentes:** Lista das 5 últimas vendas com links diretos

#### **Na Lista de Vendas:**
- **Filtros Avançados:** Por data, cliente, forma de pagamento
- **Ordenação:** Por número, data, valor, cliente
- **Ações Rápidas:** Visualizar, editar, duplicar venda
- **Exportação:** Relatórios em PDF/Excel (em desenvolvimento)

### 🧾 Comprovante de Venda

O sistema gera comprovantes completos contendo:
- **Cabeçalho:** Dados da empresa e número da venda
- **Cliente:** Informações quando informado
- **Itens:** Tabela detalhada com produtos, quantidades, preços e totais
- **Totais:** Subtotal, descontos (futuro), total geral
- **Pagamento:** Forma de pagamento selecionada
- **Rodapé:** Data/hora, vendedor, observações

### ⚡ Recursos Avançados
- **API AJAX:** Busca automática de preços sem recarregar página
- **Validações JavaScript:** Feedback instantâneo para o usuário
- **Responsivo:** Funciona perfeitamente em tablets e smartphones
- **Histórico Completo:** Todas as vendas ficam armazenadas permanentemente
- **Integração Total:** Conectado com estoque, clientes, produtos

## 🔑 Credenciais e Acesso

### **Usuários Pré-configurados:**

| Tipo | Usuário | Senha | Permissões |
|------|---------|-------|------------|
| **Administrador** | `admin` | `admin123` | Acesso total ao sistema e Django Admin |
| **Vendedor** | `usuario` | `usuario123` | Acesso completo às funcionalidades de venda |

### **URLs de Acesso:**

| Recurso | URL | Descrição |
|---------|-----|-----------|
| **Sistema Principal** | http://localhost:8000 | Dashboard e funcionalidades principais |
| **Painel Admin** | http://localhost:8000/admin | Interface administrativa do Django |
| **Sistema de Login** | http://localhost:8000/accounts/login | Tela de autenticação |
| **Nova Venda** | http://localhost:8000/vendas/nova | Acesso direto ao PDV |

⚠️ **Importante:** Altere as senhas padrão em ambiente de produção!

## 📋 Scripts e Comandos de Gestão

### 🔧 **Scripts Shell Disponíveis**

#### `setup_django.sh` - **Configuração Completa** ⭐
Executa configuração inicial completa do projeto:
```bash
chmod +x setup_django.sh && ./setup_django.sh
```
**Executa:**
- ✅ Criação do ambiente virtual
- ✅ Instalação de dependências
- ✅ Migrações do banco de dados
- ✅ Criação de dados de exemplo
- ✅ Coleta de arquivos estáticos
- ✅ Execução de testes
- ✅ Inicialização do servidor

#### `run_django.sh` - **Execução para Desenvolvimento**
Para execuções subsequentes após a configuração inicial:
```bash
./run_django.sh
```
**Executa:**
- ✅ Ativação do ambiente virtual
- ✅ Aplicação de migrações pendentes
- ✅ Coleta de arquivos estáticos
- ✅ Verificação/criação de superusuário
- ✅ Inicialização do servidor

#### `start_server.sh` - **Inicialização Rápida**
Apenas inicia o servidor (projeto já configurado):
```bash
./start_server.sh
```

### 🎯 **Comandos Django Personalizados**

#### `criar_sistema_completo` - **Comando Principal** ⭐
Cria todo o sistema com dados realísticos:
```bash
# Criação completa (recomendado para primeira execução)
python manage.py criar_sistema_completo

# Limpar dados existentes e criar novo sistema
python manage.py criar_sistema_completo --clear

# Criar apenas vendas adicionais (sistema já existe)
python manage.py criar_sistema_completo --only-vendas

# Especificar quantidade de vendas
python manage.py criar_sistema_completo --vendas 50
```

#### Comandos Individuais (Legados)
```bash
# Criar apenas dados básicos (sem vendas)
python manage.py criar_dados_exemplo

# Criar apenas vendas de exemplo
python manage.py criar_dados_vendas --clear --vendas 25
```

### 🧪 **Testes e Diagnósticos**

```bash
# Executar todos os testes
python manage.py test

# Verificar integridade do projeto
python manage.py check

# Verificar migrações pendentes
python manage.py showmigrations

# Shell interativo Django
python manage.py shell

# Criar superusuário manualmente
python manage.py createsuperuser
```

### 📊 **Comandos de Manutenção**

```bash
# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Limpar sessões expiradas
python manage.py clearsessions

# Backup do banco de dados (SQLite)
cp db.sqlite3 backup_$(date +%Y%m%d_%H%M%S).sqlite3

# Aplicar migrações específicas
python manage.py migrate core 0001

# Ver SQL das migrações
python manage.py sqlmigrate core 0001
```

## 🌐 Acessando o Sistema

### **Após Inicialização Bem-sucedida:**

1. **Abra seu navegador**
2. **Acesse:** http://localhost:8000
3. **Faça login** com as credenciais fornecidas
4. **Explore o sistema:**
   - 📊 **Dashboard:** Visão geral e estatísticas
   - 🛒 **Nova Venda:** Acesso direto ao PDV
   - 📦 **Produtos:** Gestão do catálogo
   - 📈 **Relatórios:** Movimentações e vendas

### **Páginas Principais:**

| Funcionalidade | URL Direta | Descrição |
|----------------|------------|-----------|
| **Dashboard** | `/` | Tela inicial com métricas |
| **Nova Venda** | `/vendas/nova/` | Sistema PDV |
| **Lista de Vendas** | `/vendas/` | Histórico de vendas |
| **Produtos** | `/produtos/` | Catálogo de produtos |
| **Estoque** | `/movimentacoes/` | Movimentações |
| **Clientes** | `/clientes/` | Cadastro de clientes |
| **Relatórios** | `/relatorios/` | Análises e relatórios |

## 📊 Dados de Exemplo e Demonstração

### 🎯 **Sistema Pré-povoado**
O comando `criar_sistema_completo` gera um ambiente completo para demonstração:

### 📈 **Dados Criados Automaticamente:**

| Categoria | Quantidade | Exemplos |
|-----------|------------|----------|
| **📂 Categorias** | 6 tipos | Água Mineral, Alcalina, com Gás, Saborizada, Galões, Premium |
| **📦 Produtos** | 12 itens | Água Crystal 500ml, Água Premium 1L, Galão 20L, etc. |
| **🏭 Fornecedores** | 4 empresas | Distribuidora Crystal, Fonte Pura, AquaBrasil, Premium Water |
| **👥 Clientes** | 8 cadastros | Pessoas físicas e jurídicas com dados completos |
| **💳 Formas Pagamento** | 6 opções | À Vista, Cartão Débito/Crédito, Boleto, PIX, Conta Corrente |
| **📈 Movimentações** | 25+ registros | Entradas, saídas e ajustes de estoque distribuídos |
| **🛒 Vendas** | 15+ transações | Vendas variadas com múltiplos produtos |
| **📋 Itens de Venda** | 40+ linhas | Produtos diversos distribuídos nas vendas |

### 🔑 **Credenciais Criadas:**
- **👨‍💼 Administrador:** `admin` / `admin123` (Acesso total)
- **👩‍💼 Vendedor:** `usuario` / `usuario123` (Operacional)

### 🛒 **Exemplos Realísticos de Vendas:**
- **Vendas Variadas:** 1 a 5 produtos por transação
- **Clientes Diversos:** Com e sem cliente informado
- **Pagamentos Variados:** Todas as formas de pagamento
- **Datas Distribuídas:** Últimos 30 dias para análises
- **Valores Realísticos:** R$ 15,00 a R$ 250,00 por venda
- **Quantidades Variadas:** 1 a 10 unidades por item

### 📊 **Cenários de Demonstração:**
1. **📈 Dashboard:** Métricas e estatísticas em tempo real
2. **🛒 Vendas:** Transações do dia, semana e mês
3. **⚠️ Alertas:** Produtos com estoque baixo
4. **💰 Faturamento:** Análise por forma de pagamento
5. **📦 Movimentações:** Histórico completo de estoque
6. **🧾 Relatórios:** Dados prontos para análise

## 💳 Gestão Financeira e Formas de Pagamento

### 🏦 **Controle de Pagamentos**
- **Cadastro Flexível:** Diferentes formas com prazos personalizados
- **Controle de Prazos:** 0 dias = à vista, 30+ dias = parcelado
- **Status Ativo/Inativo:** Habilitar/desabilitar conforme necessidade
- **Integração Total:** Vinculação com vendas e movimentações
- **Relatórios Detalhados:** Análise por forma de pagamento

### 💰 **Controle de Valores em Movimentações**
- **Valores por Transação:** Preço unitário e total por movimentação
- **Resumos Automáticos:** Cards com totalizadores por período
- **Análise por Tipo:** Separação entre entradas, saídas e ajustes
- **Filtros Avançados:** Por data, produto, tipo, forma de pagamento
- **Indicadores Visuais:** Status diferenciado por tipo de movimentação

### 📈 **Relatórios Financeiros**
- **Faturamento Diário:** Vendas e valores do dia atual
- **Faturamento Mensal:** Totais dos últimos 30 dias
- **Análise de Margem:** Diferença entre custo e venda
- **Valor do Estoque:** Patrimônio total em produtos
- **Movimentação Financeira:** Entradas e saídas de capital

## 🎯 Funcionalidades Detalhadas

### 📊 **Dashboard Inteligente**
- **📈 Métricas em Tempo Real:**
  - Estatísticas gerais do estoque atual
  - Vendas do dia: quantidade e faturamento
  - Vendas mensais: últimos 30 dias
  - Valor total do patrimônio em estoque
  
- **⚠️ Alertas e Indicadores:**
  - Produtos com estoque baixo destacados
  - Notificações visuais de status crítico
  - Cards coloridos por nível de urgência
  
- **📋 Atividades Recentes:**
  - Últimas 5 movimentações de estoque
  - Vendas recentes com links diretos
  - Acesso rápido a ações principais

### 🛒 **Sistema de Vendas Profissional**
- **🎯 Interface PDV Avançada:**
  - Layout similar a sistemas comerciais
  - Múltiplos produtos por transação
  - Cálculos automáticos em tempo real
  - Validação de estoque antes da venda
  
- **🧾 Gestão de Comprovantes:**
  - Numeração sequencial automática
  - Comprovantes detalhados para impressão
  - Histórico permanente de transações
  - Visualização completa com dados do cliente
  
- **📊 Controle de Performance:**
  - Relatórios de vendas por período
  - Análise de produtos mais vendidos
  - Faturamento por forma de pagamento
  - Métricas de performance de vendedor

### 📦 **Gestão Completa de Estoque**
- **📋 Controle de Produtos:**
  - Cadastro completo com categorias
  - Controle de preços (custo vs. venda)
  - Definição de estoque mínimo
  - Status ativo/inativo
  - Código único por produto
  
- **📈 Movimentações Detalhadas:**
  - Entrada, saída e ajuste de estoque
  - Histórico completo com usuário responsável
  - Observações detalhadas por movimentação
  - Controle de valores por transação
  
- **⚠️ Sistema de Alertas:**
  - Notificação automática de estoque baixo
  - Dashboard com produtos críticos
  - Relatórios de reposição necessária

### 👥 **Gestão de Relacionamentos**
- **🤝 Cadastro de Clientes:**
  - Pessoas físicas e jurídicas
  - Dados de contato completos
  - Histórico de compras por cliente
  - Análise de perfil de consumo
  
- **🏭 Controle de Fornecedores:**
  - Dados comerciais detalhados
  - Histórico de fornecimentos
  - Avaliação de performance
  - Controle de prazos e condições

## 🔧 Arquitetura e Estrutura do Projeto

### 📁 **Estrutura de Diretórios**
```
estoque_agua/
├── 🔧 manage.py                    # Utilitário principal Django
├── 📋 requirements.txt             # Dependências Python
├── 🗃️ db.sqlite3                  # Banco de dados SQLite
├── ⚙️ setup_django.sh             # Script de configuração automática
├── 🚀 run_django.sh               # Script para desenvolvimento
├── ▶️ start_server.sh             # Script de inicialização rápida
│
├── 📂 estoque_agua/               # Configurações Django
│   ├── ⚙️ settings.py             # Configurações principais
│   ├── 🌐 urls.py                 # URLs principais
│   ├── 🚀 wsgi.py                 # Interface WSGI
│   └── ⚡ asgi.py                 # Interface ASGI
│
├── 📂 core/                       # App principal do sistema
│   ├── 📋 models.py               # Modelos de dados
│   ├── 👁️ views.py                # Lógica de negócio
│   ├── 📝 forms.py                # Formulários Django
│   ├── 🔧 admin.py                # Interface administrativa
│   ├── 🌐 urls.py                 # URLs do app
│   ├── 📂 templates/              # Templates HTML
│   ├── 🎨 static/                 # Arquivos CSS/JS
│   ├── 🏷️ templatetags/           # Tags personalizadas
│   ├── 📂 management/commands/    # Comandos personalizados
│   └── 📂 migrations/             # Migrações do banco
│
├── 📂 accounts/                   # App de autenticação
│   ├── 👁️ views.py                # Views de login/logout
│   ├── 🌐 urls.py                 # URLs de autenticação
│   └── 📋 models.py               # Modelos de usuário
│
├── 📂 templates/                  # Templates globais
│   ├── 🏠 base.html               # Template base
│   └── 📂 registration/           # Templates de login
│       └── 🔐 login.html
│
├── 📂 static/                     # Arquivos estáticos
│   ├── 🎨 css/custom.css          # Estilos personalizados
│   └── 🖼️ imagens/                # Imagens do sistema
│
└── 📂 staticfiles/                # Arquivos coletados (produção)
    ├── 🔧 admin/                  # Assets do Django Admin
    └── 🎨 css/                    # CSS coletado
```

### 🏗️ **Modelos de Dados (Models)**

#### 📊 **Principais Entidades:**

1. **🏷️ Categoria**
   - Organização hierárquica de produtos
   - Nome e descrição
   
2. **📦 Produto**
   - Catálogo completo de itens
   - Preços, estoque, códigos únicos
   - Relacionamento com categoria

3. **👤 Cliente**
   - Pessoas físicas e jurídicas
   - Dados de contato e endereço

4. **🏭 Fornecedor**
   - Parceiros comerciais
   - Dados para fornecimento

5. **💳 FormaPagamento**
   - Métodos de pagamento
   - Controle de prazos

6. **📈 MovimentacaoEstoque**
   - Entrada, saída, ajuste
   - Controle de valores e usuários

7. **🛒 Venda**
   - Cabeçalho das transações
   - Cliente, forma pagamento, totais

8. **📋 ItemVenda**
   - Produtos individuais de cada venda
   - Quantidade, preço, totais

### 🔄 **Relacionamentos**
- **Produto ↔ Categoria:** ManyToOne
- **Venda ↔ Cliente:** ManyToOne (opcional)
- **Venda ↔ FormaPagamento:** ManyToOne
- **ItemVenda ↔ Venda:** ManyToOne
- **ItemVenda ↔ Produto:** ManyToOne
- **MovimentacaoEstoque ↔ Produto:** ManyToOne

## 📱 Interface e Experiência do Usuário

### 🎨 **Design Moderno**
- **🌈 Paleta de Cores:** Gradientes azul/roxo profissionais
- **📱 Responsividade Total:** Bootstrap 5 para todos os dispositivos
- **🎯 UX Intuitiva:** Navegação clara e objetiva
- **⚡ Performance:** Carregamento rápido e otimizado
- **🔄 Animações Suaves:** Transições elegantes entre páginas

### 🧭 **Navegação Inteligente**
- **📋 Sidebar Fixo:** Links diretos para todas as funcionalidades
- **🏠 Breadcrumbs:** Localização clara na navegação
- **🔍 Busca Rápida:** Pesquisa em produtos, clientes, vendas
- **⚡ Acesso Rápido:** Botões destacados para ações principais
- **📊 Dashboard Central:** Hub de informações e acesso

### 🔔 **Feedback Visual**
- **✅ Alertas de Sucesso:** Confirmações claras de ações
- **⚠️ Avisos Importantes:** Alertas de estoque baixo
- **❌ Tratamento de Erros:** Mensagens explicativas
- **🔄 Loading States:** Indicadores de carregamento
- **🎨 Icons Consistentes:** Font Awesome em toda interface

### 📊 **Dashboards e Relatórios**
- **📈 Gráficos Dinâmicos:** Visualizações de dados em tempo real
- **📋 Tabelas Responsivas:** Dados organizados e filtráveis
- **🎯 Cards Informativos:** Métricas importantes destacadas
- **📱 Mobile First:** Interface otimizada para dispositivos móveis
- **🖨️ Preparado para Impressão:** Relatórios e comprovantes

## 🛡️ Segurança e Performance

### 🔐 **Segurança Implementada**
- **🎫 Autenticação Django:** Sistema robusto de login/logout
- **🛡️ Proteção CSRF:** Tokens automáticos em formulários
- **🔒 Login Obrigatório:** Acesso restrito a usuários autenticados
- **👥 Controle de Permissões:** Diferentes níveis de acesso
- **🔐 Senhas Seguras:** Hash automático pelo Django
- **🚫 Validações Backend:** Dupla validação de dados

### ⚡ **Otimizações de Performance**
- **📊 Queries Otimizadas:** `select_related` e `prefetch_related`
- **💾 Cache Inteligente:** Dados frequentes em cache
- **📱 Assets Minificados:** CSS e JS otimizados
- **🗄️ Índices de Banco:** Consultas rápidas em campos críticos
- **⏱️ Lazy Loading:** Carregamento sob demanda
- **📊 Agregações Eficientes:** Cálculos otimizados no banco

### 🔧 **Monitoramento e Debug**
- **📝 Logs Detalhados:** Registro de ações importantes
- **🐛 Debug Mode:** Informações detalhadas em desenvolvimento
- **🔍 Django Debug Toolbar:** Análise de performance (dev)
- **📊 Métricas de Sistema:** Monitoramento de recursos
- **⚠️ Tratamento de Exceções:** Erros capturados e logados

## 🧪 Testes e Qualidade

### ✅ **Testes Automatizados**
```bash
# Executar todos os testes
python manage.py test

# Testes com verbosidade
python manage.py test --verbosity=2

# Testes específicos de uma app
python manage.py test core

# Testes com cobertura
coverage run manage.py test
coverage report
```

### 📊 **Cobertura de Testes**
- **Modelos:** Validações e métodos personalizados
- **Views:** Lógica de negócio e permissões
- **Forms:** Validações e limpeza de dados
- **APIs:** Endpoints e retornos JSON
- **Comandos:** Scripts de management

### 🔍 **Ferramentas de Qualidade**
```bash
# Verificar problemas no projeto
python manage.py check

# Análise de código (se instalado)
flake8 .
black . --check
pylint core/

# Verificar migrações
python manage.py makemigrations --dry-run
```

## 🔧 Comandos Úteis para Desenvolvedores

### 🛠️ **Comandos de Desenvolvimento**
```bash
# Criar e aplicar migrações
python manage.py makemigrations
python manage.py migrate

# Verificar migrações pendentes
python manage.py showmigrations

# Reverter migrações
python manage.py migrate core 0001

# Ver SQL das migrações
python manage.py sqlmigrate core 0001_initial
```

### 👑 **Gestão de Usuários**
```bash
# Criar superusuário
python manage.py createsuperuser

# Alterar senha de usuário
python manage.py changepassword admin

# Shell interativo com contexto Django
python manage.py shell

# Shell com Django Extensions (se instalado)
python manage.py shell_plus
```

### 🗄️ **Gestão de Banco de Dados**
```bash
# Backup do banco SQLite
cp db.sqlite3 backup_$(date +%Y%m%d_%H%M%S).sqlite3

# Restaurar backup
cp backup_20251208_143000.sqlite3 db.sqlite3

# Executar SQL personalizado
python manage.py dbshell

# Limpar dados de uma tabela (cuidado!)
python manage.py shell -c "from core.models import Venda; Venda.objects.all().delete()"
```

### 📁 **Arquivos Estáticos e Mídia**
```bash
# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Limpar arquivos antigos
python manage.py collectstatic --clear --noinput

# Verificar arquivos estáticos
python manage.py findstatic css/custom.css
```

### 🧹 **Limpeza e Manutenção**
```bash
# Limpar sessões expiradas
python manage.py clearsessions

# Otimizar banco SQLite
python manage.py dbshell -c ".vacuum"

# Ver tamanho do banco
ls -lh db.sqlite3

# Verificar integridade
python manage.py check --deploy
```

## � Roadmap e Próximas Funcionalidades

### 📋 **Em Desenvolvimento**
- [ ] 🐳 **Containerização Docker** - Deploy simplificado
- [ ] 📊 **Relatórios PDF** - Exportação de vendas e estoque
- [ ] 📱 **API REST** - Integração com aplicativos móveis
- [ ] 🔔 **Notificações** - Alertas via email/SMS
- [ ] 📈 **Dashboard Analytics** - Gráficos avançados com Chart.js

### 🎯 **Futuras Melhorias**
- [ ] 💾 **Backup Automático** - Rotinas de backup programadas
- [ ] 🔄 **Sincronização** - Multi-filiais conectadas
- [ ] 💳 **Integração Pagamento** - APIs de pagamento online
- [ ] 📦 **Código de Barras** - Leitura e geração automática
- [ ] 🤖 **Automações** - Reposição automática de estoque

### 🌟 **Versões Planejadas**
- **v2.2:** Relatórios PDF e exportação Excel
- **v2.3:** API REST completa
- **v2.4:** Dashboard analytics avançado
- **v3.0:** Arquitetura multi-tenant

## 📞 Suporte e Comunidade

### 🆘 **Obtendo Ajuda**
1. **📖 Documentação:** Consulte os arquivos `.md` do projeto
2. **🔍 Issues:** Verifique problemas conhecidos no repositório
3. **💬 Discussões:** Participe das discussões da comunidade
4. **📧 Contato Direto:** Para suporte empresarial

### 🐛 **Reportando Bugs**
```bash
# 1. Verificar logs do Django
tail -f logs/django.log

# 2. Executar diagnóstico
python manage.py check --deploy

# 3. Coletar informações do sistema
python --version
pip list
```

### 🤝 **Contribuindo com o Projeto**
1. **🍴 Fork** o repositório
2. **🌿 Branch** para sua feature: `git checkout -b feature/nova-funcionalidade`
3. **💻 Código** seguindo os padrões do projeto
4. **✅ Testes** para suas alterações
5. **📝 Commit** com mensagens claras
6. **🔄 Pull Request** detalhado

### 📋 **Padrões de Contribuição**
- **🐍 PEP 8:** Estilo de código Python
- **🧪 Testes:** Cobertura mínima de 80%
- **📝 Documentação:** Docstrings em funções
- **🔒 Segurança:** Validações adequadas
- **📱 Responsivo:** Interface mobile-friendly

## 📄 Licença e Créditos

### 📋 **Licença**
Este projeto está sob a **Licença MIT** - use livremente para fins educacionais e comerciais.

### 👨‍💻 **Créditos e Tecnologias**
- **⚡ Django Framework** - Base robusta para desenvolvimento web
- **🎨 Bootstrap 5** - Framework CSS responsivo e moderno  
- **🔧 Font Awesome** - Biblioteca de ícones profissionais
- **🐍 Python Community** - Bibliotecas e ferramentas incríveis
- **💡 Open Source** - Inspirado pela comunidade de código aberto

### 🏆 **Reconhecimentos**
- Desenvolvido para a comunidade de pequenos negócios
- Inspirado pelas necessidades reais de distribuidoras de água
- Focado na simplicidade e eficiência operacional

---

<div align="center">

# 🚰 **Sistema de Estoque de Água**
### *Gestão Inteligente para seu Negócio*

[![⭐ Stars](https://img.shields.io/github/stars/fgsantosti/estoque_agua?style=social)](https://github.com/fgsantosti/estoque_agua)
[![🍴 Forks](https://img.shields.io/github/forks/fgsantosti/estoque_agua?style=social)](https://github.com/fgsantosti/estoque_agua)
[![👁️ Watchers](https://img.shields.io/github/watchers/fgsantosti/estoque_agua?style=social)](https://github.com/fgsantosti/estoque_agua)

**📅 Última Atualização:** Dezembro 2025 | **🏷️ Versão:** 2.1  
**👨‍💼 Desenvolvido por:** [@fgsantosti](https://github.com/fgsantosti)

---

### 🎯 **Transforme sua distribuidora com tecnologia profissional!**

*Sistema completo, gratuito e pronto para usar.*

**[� Download](https://github.com/fgsantosti/estoque_agua/archive/main.zip)** | 
**[📖 Documentação](VENDAS.md)** | 
**[🐛 Issues](https://github.com/fgsantosti/estoque_agua/issues)** |
**[💬 Discussions](https://github.com/fgsantosti/estoque_agua/discussions)**

</div>
