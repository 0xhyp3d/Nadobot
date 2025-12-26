# 🚀 Guia de Setup para Repositório Público

Este guia ajuda a preparar o projeto para ser compartilhado publicamente, garantindo que dados sensíveis não sejam expostos.

## ✅ Checklist Antes de Fazer Commit

### 1. Verificar Arquivos Sensíveis

```bash
# Verificar se há chaves privadas no código
grep -r "0x[0-9a-fA-F]\{64\}" . --exclude-dir=.git --exclude="*.log" --exclude="*.json"

# Verificar se há arquivos .env no repositório
find . -name ".env*" -not -name ".env.example"

# Verificar se há logs com dados sensíveis
ls -la logs/
```

### 2. Garantir que .gitignore está Funcionando

```bash
# Verificar o que será ignorado
git status --ignored

# Verificar se arquivos sensíveis estão sendo ignorados
git check-ignore -v .env logs/ produtos_funcionais.txt
```

### 3. Limpar Histórico se Necessário

Se você já fez commits com dados sensíveis:

**⚠️ ATENÇÃO**: Isso reescreve o histórico. Use apenas se for necessário.

```bash
# Criar backup primeiro
git clone --mirror . ../Bot-backup

# Remover arquivos sensíveis do histórico (use com cuidado!)
# git filter-branch --force --index-filter \
#   "git rm --cached --ignore-unmatch .env logs/*.log" \
#   --prune-empty --tag-name-filter cat -- --all
```

### 4. Verificar o que Será Commitado

```bash
# Ver o que será adicionado
git status

# Ver as mudanças
git diff

# Ver o que está staged
git diff --staged
```

## 📋 Arquivos que NÃO Devem ser Commitados

Garantido pelo `.gitignore`:

- ✅ `.env` e `.env.*` (exceto `.env.example`)
- ✅ `logs/` e todos os arquivos `.log`
- ✅ `*_history.json` e `Bot*_history.json`
- ✅ `__pycache__/` e `*.pyc`
- ✅ `produtos_funcionais.txt`
- ✅ Arquivos de backup (`.save`, `.backup`)
- ✅ Arquivos de sistema (`.DS_Store`, `Thumbs.db`)

## 🔒 Arquivos que DEVEM ser Commitados

- ✅ `.env.example` (template sem dados sensíveis)
- ✅ `.gitignore`
- ✅ `README.md`
- ✅ `CONTRIBUTING.md`
- ✅ `LICENSE`
- ✅ Código fonte (`.py`)
- ✅ Scripts (`.sh`)
- ✅ `requirements.txt`
- ✅ Documentação (`docs/`)

## 🚀 Primeiro Commit

```bash
# Inicializar repositório Git (se ainda não foi feito)
git init

# Adicionar arquivos
git add .gitignore .env.example README.md CONTRIBUTING.md LICENSE
git add *.py *.sh requirements.txt
git add docs/

# Verificar o que será commitado
git status

# Fazer commit
git commit -m "Initial commit: Bot de trading Nado Protocol"

# Adicionar remote (substitua com sua URL)
git remote add origin <url-do-repositorio>

# Fazer push
git push -u origin main
```

## 🔍 Verificação Final

Antes de fazer push público:

1. ✅ Nenhum arquivo `.env` está no repositório
2. ✅ Nenhuma chave privada está no código
3. ✅ Logs não estão no repositório
4. ✅ `.gitignore` está funcionando corretamente
5. ✅ `.env.example` existe e está configurado corretamente
6. ✅ README.md está completo e atualizado

## 📝 Notas Adicionais

- Use `git-crypt` ou `git-secret` para proteger arquivos sensíveis se necessário
- Considere usar GitHub Secrets para CI/CD se implementar testes automatizados
- Revise periodicamente o `.gitignore` para garantir que novos arquivos sensíveis sejam ignorados

