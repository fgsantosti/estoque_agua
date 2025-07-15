#!/bin/bash

# Script para iniciar o servidor Django
echo "🚀 Iniciando servidor Django..."

# Ativar ambiente virtual se existir
if [ -d "venv" ]; then
    echo "🔌 Ativando ambiente virtual..."
    source venv/bin/activate
fi

# Verificar se o banco está atualizado
echo "🔍 Verificando migrações pendentes..."
if python manage.py showmigrations --plan | grep -q "\[ \]"; then
    echo "⚠️ Existem migrações pendentes. Aplicando..."
    python manage.py migrate
fi

# Iniciar servidor
echo "🌐 Iniciando servidor em http://localhost:8000"
echo "🛠️ Admin disponível em http://localhost:8000/admin"
echo "⌨️ Pressione Ctrl+C para parar o servidor"
echo ""

python manage.py runserver
