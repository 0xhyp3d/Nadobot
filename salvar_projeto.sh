#!/bin/bash
# Script para salvar o projeto no Git

echo "💾 Salvando projeto no Git..."
echo ""

# Verificar se já é um repositório Git
if [ ! -d .git ]; then
    echo "📦 Inicializando repositório Git..."
    git init
    echo "✅ Repositório inicializado"
    echo ""
fi

# Verificar arquivos sensíveis
echo "🔒 Verificando segurança..."
if git ls-files 2>/dev/null | grep -q "\.env$"; then
    echo "❌ AVISO: .env está no repositório! Removendo..."
    git rm --cached .env 2>/dev/null
fi

# Adicionar arquivos
echo "📝 Adicionando arquivos..."
git add .gitignore .env.example README.md CONTRIBUTING.md LICENSE SETUP_REPOSITORIO.md RESUMO_ORGANIZACAO.md 2>/dev/null
git add *.py *.sh requirements.txt 2>/dev/null
git add docs/ 2>/dev/null
git add .gitattributes 2>/dev/null

# Verificar o que será commitado
echo ""
echo "📋 Arquivos que serão commitados:"
git status --short | head -20

# Verificar segurança novamente
echo ""
echo "🔒 Verificação de segurança final:"
if git diff --cached --name-only | grep -q "\.env$"; then
    echo "❌ ERRO: .env está prestes a ser commitado! Abortando..."
    exit 1
fi

if git diff --cached --name-only | grep -q "logs/"; then
    echo "⚠️  AVISO: Alguns logs podem estar sendo commitados. Verifique!"
fi

# Fazer commit
echo ""
read -p "💾 Fazer commit? (s/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Ss]$ ]]; then
    git commit -m "Initial commit: Bot de trading Nado Protocol

- Múltiplas estratégias de trading (Grid Trading, Market Making, Williams %R)
- Suporte a múltiplos produtos perpetual
- Modo agressivo configurável
- Proteção contra Cloudflare
- Gerenciamento automático de erros
- Cálculo detalhado de P/L
- Documentação completa
- Scripts de gerenciamento"
    
    echo ""
    echo "✅ Projeto salvo com sucesso!"
    echo ""
    echo "📊 Estatísticas:"
    git ls-files | wc -l | xargs echo "  Arquivos commitados:"
    echo ""
    echo "🚀 Próximo passo:"
    echo "  git remote add origin <url-do-repositorio>"
    echo "  git push -u origin main"
else
    echo "❌ Commit cancelado pelo usuário"
    exit 1
fi




