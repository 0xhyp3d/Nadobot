#!/bin/bash

echo "═══════════════════════════════════════════════════════════"
echo "  🚀 PREPARANDO PROJETO PARA GITHUB"
echo "═══════════════════════════════════════════════════════════"
echo ""

cd "$(dirname "$0")"

# Verificar se já é um repositório git
if [ -d .git ]; then
    echo "⚠️  Repositório git já existe. Continuando..."
else
    echo "1️⃣  Inicializando repositório git..."
    git init
    echo "✅ Repositório git inicializado"
fi

echo ""
echo "2️⃣  Verificando .gitignore..."
if [ -f .gitignore ]; then
    echo "✅ .gitignore encontrado"
    echo ""
    echo "Arquivos protegidos:"
    grep -E "^\.env|^logs/|_history\.json|__pycache__" .gitignore | head -10
else
    echo "❌ .gitignore não encontrado! Criando..."
    cat > .gitignore << 'EOF'
# Arquivos de ambiente e credenciais
.env
.env.*
!.env.example
.env.save
.env.backup

# Logs
logs/
*.log

# Histórico de trades
*_history.json
Bot*_history.json
backup_*/

# Python
__pycache__/
*.py[cod]
*.pyc

# Arquivos temporários
*.tmp
*.backup
*.save
EOF
    echo "✅ .gitignore criado"
fi

echo ""
echo "3️⃣  Verificando .env.example..."
if [ -f .env.example ]; then
    echo "✅ .env.example existe"
else
    echo "⚠️  .env.example não encontrado (será criado no commit)"
fi

echo ""
echo "4️⃣  Verificando arquivos sensíveis que NÃO devem ser commitados..."
SENSITIVE_FILES=(".env" ".env.bot1" ".env.bot2" ".env.bot3" ".env.bot4")
for file in "${SENSITIVE_FILES[@]}"; do
    if [ -f "$file" ]; then
        if git check-ignore -q "$file" 2>/dev/null; then
            echo "✅ $file está sendo ignorado (CORRETO)"
        else
            echo "❌ $file existe mas NÃO está no .gitignore!"
        fi
    else
        echo "ℹ️  $file não existe (OK)"
    fi
done

echo ""
echo "5️⃣  Verificando status do git..."
echo ""
git status --short | head -20

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  📋 PRÓXIMOS PASSOS"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "1. Crie um repositório no GitHub:"
echo "   https://github.com/new"
echo ""
echo "2. Execute os comandos:"
echo ""
echo "   # Adicionar todos os arquivos"
echo "   git add ."
echo ""
echo "   # Fazer commit inicial"
echo "   git commit -m 'Initial commit: Bot de trading Nado Protocol'"
echo ""
echo "   # Renomear branch para main"
echo "   git branch -M main"
echo ""
echo "   # Conectar ao GitHub (substitua SEU_USUARIO e NOME_REPO)"
echo "   git remote add origin https://github.com/SEU_USUARIO/NOME_REPO.git"
echo ""
echo "   # Enviar para o GitHub"
echo "   git push -u origin main"
echo ""
echo "📖 Para mais detalhes, veja: COMO_SUBIR_GITHUB.md"
echo ""
echo "═══════════════════════════════════════════════════════════"

