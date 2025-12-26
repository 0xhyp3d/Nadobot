#!/bin/bash

echo "═══════════════════════════════════════════════════════════"
echo "  🚀 ENVIANDO PROJETO PARA GITHUB"
echo "═══════════════════════════════════════════════════════════"
echo ""

cd "$(dirname "$0")"

# Verificar se é repositório git
if [ ! -d .git ]; then
    echo "⚠️  Inicializando repositório git..."
    git init
fi

# Verificar .env.example
if [ ! -f .env.example ]; then
    echo "📝 Criando .env.example..."
    cat > .env.example << 'EOF'
# Configuração do Bot - Nado Protocol
NADO_NETWORK=mainnet
PRIVATE_KEY=sua_chave_privada_aqui
PRIVATE_KEY_BOT1=
PRIVATE_KEY_BOT2=
PRIVATE_KEY_BOT3=
PRIVATE_KEY_BOT4=
RESET_HISTORY=false
EOF
fi

echo "✅ Verificando arquivos sensíveis..."
SENSITIVE_FOUND=0
for file in .env .env.bot1 .env.bot2 .env.bot3 .env.bot4; do
    if [ -f "$file" ]; then
        if git check-ignore -q "$file" 2>/dev/null; then
            echo "  ✅ $file está sendo ignorado (CORRETO)"
        else
            echo "  ❌ $file existe mas NÃO está no .gitignore!"
            SENSITIVE_FOUND=1
        fi
    fi
done

if [ $SENSITIVE_FOUND -eq 1 ]; then
    echo ""
    echo "❌ ERRO: Arquivos sensíveis não estão sendo ignorados!"
    echo "   Verifique seu .gitignore antes de continuar."
    exit 1
fi

echo ""
echo "📦 Adicionando arquivos ao git..."
git add .

echo ""
echo "🔍 Verificando o que será commitado..."
echo ""
git status --short | head -20

echo ""
read -p "Continuar com o commit? (s/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Ss]$ ]]; then
    echo "Operação cancelada."
    exit 1
fi

echo ""
echo "📝 Fazendo commit..."
git commit -m "Initial commit: Bot de trading Nado Protocol" || {
    echo "⚠️  Nada para commitar ou commit já existe"
}

echo ""
echo "🔀 Configurando branch main..."
git branch -M main 2>/dev/null || echo "Branch já está como main"

echo ""
echo "🔗 Configurando repositório remoto..."
git remote remove origin 2>/dev/null
git remote add origin https://github.com/0xhyp3d/Nadobot.git
git remote -v

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  📤 ENVIANDO PARA O GITHUB..."
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Executando: git push -u origin main"
echo ""
echo "⚠️  Você pode precisar autenticar:"
echo "   - Se usar HTTPS, pode solicitar usuário/senha"
echo "   - Ou use um token de acesso pessoal"
echo ""

git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "═══════════════════════════════════════════════════════════"
    echo "  ✅ SUCESSO! Código enviado para o GitHub"
    echo "═══════════════════════════════════════════════════════════"
    echo ""
    echo "🌐 Acesse: https://github.com/0xhyp3d/Nadobot"
    echo ""
else
    echo ""
    echo "❌ Erro ao fazer push. Verifique:"
    echo "   1. Repositório existe no GitHub: https://github.com/0xhyp3d/Nadobot"
    echo "   2. Você tem permissão para fazer push"
    echo "   3. Credenciais estão corretas"
    echo ""
fi


