# 🚰 Sistema de Estoque de Água

Sistema completo de gerenciamento de estoque para distribuidoras de água, desenvolvido em Django.

## ✨ Funcionalidades

- 🔐 **Sistema de Login/Logout** com autenticação
- 📊 **Dashboard** com estatísticas em tempo real
- 📦 **Gestão de Produtos** (CRUD completo)
- 📈 **Controle de Movimentações** (Entrada/Saída/Ajuste)
- 🏷️ **Categorização de Produtos**
- 🚚 **Cadastro de Fornecedores**
- 👥 **Cadastro de Clientes**
- 💳 **Formas de Pagamento** com controle de prazo
- ⚠️ **Alertas de Estoque Baixo**
- 💰 **Controle de Preços** (Custo/Venda)
- 📱 **Interface Responsiva** (Bootstrap 5)
- 🎨 **Design Moderno** com gradientes e animações

## 🛠️ Tecnologias Utilizadas

- **Backend:** Django 4.2.7
- **Frontend:** Bootstrap 5, Font Awesome
- **Forms:** Django Crispy Forms + Bootstrap 5
- **Database:** SQLite (desenvolvimento)
- **Autenticação:** Django Auth System

## 🚀 Instalação e Configuração

### Método 1: Configuração Automática (Recomendado)

```bash
# Clone ou baixe o projeto
cd estoque_agua

# Execute o script de configuração completa
./setup_django.sh
```

### Método 2: Configuração Manual

```bash
# 1. Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Aplicar migrações
python manage.py migrate

# 4. Coletar arquivos estáticos
python manage.py collectstatic --noinput

# 5. Criar dados de exemplo
python manage.py criar_dados_exemplo

# 6. Iniciar servidor
python manage.py runserver
```

## 🔑 Credenciais de Acesso

Após executar os scripts ou criar os dados de exemplo:

- **Administrador:** `admin` / `admin123`
- **Usuário:** `usuario` / `usuario123`

## 📋 Scripts Disponíveis

### `setup_django.sh` - Configuração Completa
Executa toda a configuração inicial do projeto:
- Cria ambiente virtual
- Instala dependências
- Configura banco de dados
- Cria dados de exemplo
- Executa testes

### `run_django.sh` - Execução Rápida
Para desenvolvimentos futuros:
- Aplica migrações pendentes
- Coleta arquivos estáticos
- Verifica/cria superusuário

### `start_server.sh` - Iniciar Servidor
Apenas inicia o servidor de desenvolvimento:
- Ativa ambiente virtual
- Verifica migrações
- Inicia servidor Django

## 🌐 Acessando o Sistema

Após iniciar o servidor:

- **Sistema:** http://localhost:8000
- **Painel Admin:** http://localhost:8000/admin
- **Login:** http://localhost:8000/accounts/login

## 📊 Dados de Exemplo
O sistema vem com dados pré-configurados para demonstração:

### 📈 Dados Criados Automaticamente:
- **6 Categorias** de produtos (Água Mineral, Alcalina, com Gás, Saborizada, Galões, Premium)
- **10 Produtos** diversos com preços e estoques variados
- **3 Fornecedores** com dados completos
- **5 Clientes** (pessoas físicas e jurídicas)
- **6 Formas de Pagamento** (À Vista, Cartão, Boletos, etc.)
- **18+ Movimentações** de entrada, saída e ajuste

### 🔑 Credenciais de Acesso:
- **Administrador:** `admin` / `admin123`
- **Usuário:** `usuario` / `usuario123`

## 💳 Gerenciamento de Formas de Pagamento

- Cadastro de diferentes formas de pagamento
- Controle de prazo de recebimento (0 = à vista)
- Vinculação com movimentações de saída/venda
- Status ativo/inativo para cada forma
- Relatórios por forma de pagamento

## 🎯 Principais Funcionalidades

### Dashboard
- Estatísticas gerais do estoque
- Produtos com estoque baixo
- Valor total do estoque
- Movimentações recentes
- Gráficos e métricas

### Gestão de Produtos
- Cadastro completo com categoria
- Controle de preço de custo e venda
- Definição de estoque mínimo
- Status ativo/inativo
- Código único por produto

### Controle de Estoque
- Movimentações de entrada, saída e ajuste
- Histórico completo de movimentações
- Usuário responsável por cada movimentação
- Observações detalhadas

### Alertas Inteligentes
- Notificação automática de estoque baixo
- Dashboard com produtos críticos
- Sinais visuais de status

## 🔧 Estrutura do Projeto

```
estoque_agua/
├── core/                    # App principal
│   ├── models.py           # Modelos de dados
│   ├── views.py            # Lógica de negócio
│   ├── forms.py            # Formulários
│   ├── admin.py            # Interface admin
│   └── templates/          # Templates do core
├── accounts/               # App de autenticação
├── templates/              # Templates globais
│   ├── base.html          # Template base
│   └── registration/      # Templates de login
├── static/                 # Arquivos estáticos
├── requirements.txt        # Dependências
└── manage.py              # Utilitário Django
```

## 📱 Recursos da Interface

- **Design Responsivo:** Funciona em desktop, tablet e mobile
- **Navegação Intuitiva:** Sidebar com links diretos
- **Cores Modernas:** Gradientes azul/roxo
- **Feedback Visual:** Alertas e confirmações
- **Ícones Consistentes:** Font Awesome em toda interface

## 🛡️ Segurança

- Sistema de autenticação Django
- Proteção CSRF ativa
- Login obrigatório para todas as funcionalidades
- Controle de permissões por usuário

## 🧪 Comandos de Gestão

### Criação de Dados de Exemplo
```bash
# Criar dados de exemplo (mantém dados existentes)
python manage.py criar_dados_exemplo

# Limpar dados existentes e criar novos
python manage.py criar_dados_exemplo --clear
```

### Testes do Sistema
Execute os testes do sistema:

```bash
python manage.py test
```

## 🔧 Comandos Úteis

```bash
# Verificar migrações pendentes
python manage.py showmigrations

# Criar superusuário
python manage.py createsuperuser

# Coletar arquivos estáticos
python manage.py collectstatic

# Shell interativo
python manage.py shell
```

## 📄 Licença

Este projeto é de uso educacional e comercial livre.

## 🤝 Contribuição

1. Faça fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📞 Suporte

Para dúvidas ou problemas:
- Verifique os logs do Django
- Execute `python manage.py check` para diagnóstico
- Consulte a documentação do Django

---

**Sistema de Estoque de Água - Gestão Inteligente para seu Negócio** 🚰
