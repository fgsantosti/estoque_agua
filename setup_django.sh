#!/bin/bash

# Script para configuração completa do projeto Django Estoque Água
# Este script executa todos os comandos necessários em sequência

echo "=========================================="
echo "  CONFIGURAÇÃO DO PROJETO ESTOQUE ÁGUA"
echo "=========================================="

# Função para verificar se o comando anterior foi executado com sucesso
check_success() {
    if [ $? -eq 0 ]; then
        echo "✅ $1 executado com sucesso!"
    else
        echo "❌ Erro ao executar: $1"
        exit 1
    fi
}

# Função para criar arquivo .env se não existir
create_env_file() {
    if [ ! -f .env ]; then
        echo "📝 Criando arquivo .env..."
        cat > .env << EOF
SECRET_KEY=django-insecure-$(python -c 'import secrets; print("".join(secrets.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for i in range(50)))')
DEBUG=True
EOF
        echo "✅ Arquivo .env criado com sucesso!"
    else
        echo "📄 Arquivo .env já existe."
    fi
}

# Verificar se Python está instalado
echo "🔍 Verificando Python..."
python3 --version
check_success "Verificação do Python"

# Criar e ativar ambiente virtual se não existir
if [ ! -d "venv" ]; then
    echo "🐍 Criando ambiente virtual..."
    python3 -m venv venv
    check_success "Criação do ambiente virtual"
fi

echo "🔌 Ativando ambiente virtual..."
source venv/bin/activate
check_success "Ativação do ambiente virtual"

# Atualizar pip
echo "⬆️ Atualizando pip..."
pip install --upgrade pip
check_success "Atualização do pip"

# Instalar dependências
echo "📦 Instalando dependências do requirements.txt..."
pip install -r requirements.txt
check_success "Instalação das dependências"

# Criar arquivo .env
create_env_file

# Verificar configurações do Django
echo "🔧 Verificando configurações do Django..."
python manage.py check
check_success "Verificação das configurações"

# Criar migrações
echo "🗂️ Criando migrações..."
python manage.py makemigrations
check_success "Criação das migrações"

# Aplicar migrações
echo "🗄️ Aplicando migrações ao banco de dados..."
python manage.py migrate
check_success "Aplicação das migrações"

# Coletar arquivos estáticos
echo "📁 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput
check_success "Coleta de arquivos estáticos"

# Criar dados de exemplo
echo "👤 Criando dados de exemplo completos..."
python manage.py criar_sistema_completo
check_success "Criação do sistema completo com dados de exemplo"

# Executar testes (opcional)
echo "🧪 Executando testes do projeto..."
python manage.py test
check_success "Execução dos testes"

echo ""
echo "=========================================="
echo "  ✅ CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!"
echo "=========================================="
echo ""
echo "📋 Resumo do que foi executado:"
echo "   • Ambiente virtual criado e ativado"
echo "   • Dependências instaladas"
echo "   • Arquivo .env criado (se necessário)"
echo "   • Migrações criadas e aplicadas"
echo "   • Arquivos estáticos coletados"
echo "   • Sistema completo com dados de exemplo criado"
echo "   • Vendas e produtos de exemplo gerados"
echo "   • Testes executados"
echo ""
echo "🔑 CREDENCIAIS DE ACESSO:"
echo "   Administrador: admin / admin123"
echo "   Usuário: usuario / usuario123"
echo ""
echo "🛒 RECURSOS DISPONÍVEIS:"
echo "   • Sistema de Vendas (múltiplos itens)"
echo "   • Controle de Estoque automático"
echo "   • Dashboard com estatísticas de vendas"
echo "   • Produtos, Clientes e Fornecedores"
echo "   • Movimentações de estoque"
echo ""
echo "🚀 Para iniciar o servidor de desenvolvimento, execute:"
echo "   source venv/bin/activate"
echo "   python manage.py runserver"
echo ""
echo "🌐 Acesse o projeto em: http://localhost:8000"
echo "🛠️ Admin em: http://localhost:8000/admin"
echo ""
