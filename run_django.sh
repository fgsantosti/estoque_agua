#!/bin/bash

# Script rápido para executar comandos básicos do Django
# Use este script quando o ambiente já estiver configurado

echo "=========================================="
echo "    EXECUÇÃO RÁPIDA - DJANGO COMMANDS"
echo "=========================================="

# Função para verificar sucesso
check_success() {
    if [ $? -eq 0 ]; then
        echo "✅ $1"
    else
        echo "❌ Erro: $1"
        exit 1
    fi
}

# Ativar ambiente virtual se existir
if [ -d "venv" ]; then
    echo "🔌 Ativando ambiente virtual..."
    source venv/bin/activate
    check_success "Ambiente virtual ativado"
fi

# Criar migrações
echo "🗂️ Criando migrações..."
python manage.py makemigrations
check_success "Migrações criadas"

# Aplicar migrações
echo "🗄️ Aplicando migrações..."
python manage.py migrate
check_success "Migrações aplicadas"

# Coletar arquivos estáticos
echo "📁 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput
check_success "Arquivos estáticos coletados"

# Verificar se já existe superusuário
echo "👤 Verificando superusuário..."
if python manage.py shell -c "from django.contrib.auth.models import User; print('Superusuário existe!' if User.objects.filter(is_superuser=True).exists() else 'Nenhum superusuário encontrado')"; then
    read -p "Deseja criar um novo superusuário? (s/N): " create_super
    if [[ $create_super =~ ^[Ss]$ ]]; then
        python manage.py createsuperuser
    fi
else
    echo "Criando superusuário..."
    python manage.py createsuperuser
fi

echo ""
echo "✅ Comandos executados com sucesso!"
echo "🚀 Para iniciar o servidor:"
echo "   python manage.py runserver"
