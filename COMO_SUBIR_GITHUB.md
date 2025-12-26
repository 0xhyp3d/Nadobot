# 📤 Como Subir o Repositório para o GitHub

Este guia explica como fazer upload do projeto para o GitHub **sem incluir dados sensíveis**.

## ⚠️ IMPORTANTE: Segurança

- **NUNCA** faça commit de arquivos `.env` com credenciais reais
- **NUNCA** compartilhe suas chaves privadas
- O arquivo `.gitignore` já está configurado para proteger seus dados

## 📋 Passo a Passo

### 1. Verificar/Criar Conta no GitHub

Se ainda não tem uma conta:
1. Acesse https://github.com
2. Crie uma conta gratuita
3. Faça login

### 2. Criar Repositório no GitHub

1. Clique no botão **"+"** no canto superior direito
2. Selecione **"New repository"**
3. Preencha:
   - **Repository name**: `nado-trading-bot` (ou o nome que preferir)
   - **Description**: "Bot de trading automatizado para Nado Protocol"
   - **Visibility**: Escolha **Private** (recomendado) ou **Public**
   - **NÃO marque** "Add a README file" (já temos um)
4. Clique em **"Create repository"**

### 3. Configurar Git no Projeto

Execute os seguintes comandos no terminal, dentro da pasta do projeto:

```bash
# Ir para a pasta do projeto
cd /Users/igorbirni/Bot

# Inicializar repositório git (se ainda não foi feito)
git init

# Adicionar todos os arquivos (o .gitignore já protege os arquivos sensíveis)
git add .

# Fazer o primeiro commit
git commit -m "Initial commit: Bot de trading Nado Protocol"

# Renomear branch principal para 'main' (se necessário)
git branch -M main
```

### 4. Conectar ao GitHub

```bash
# Substitua SEU_USUARIO pelo seu nome de usuário do GitHub
# Substitua NOME_DO_REPOSITORIO pelo nome que você criou no passo 2
git remote add origin https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git

# Verificar se foi adicionado corretamente
git remote -v
```

### 5. Enviar para o GitHub

```bash
# Enviar código para o GitHub
git push -u origin main
```

Você será solicitado a fazer login no GitHub. Siga as instruções.

## ✅ Verificação Final

### Arquivos que NÃO devem estar no GitHub:

Execute este comando para verificar se arquivos sensíveis não foram commitados:

```bash
# Verificar se .env está sendo ignorado
git check-ignore -v .env .env.bot1 .env.bot2 .env.bot3 .env.bot4

# Verificar se logs estão sendo ignorados
git check-ignore -v logs/

# Listar todos os arquivos que serão commitados
git ls-files
```

### Arquivos que DEVEM estar no GitHub:

- ✅ `bot.py`, `bot1.py`, `bot2.py`, `bot3.py`, `bot4.py`
- ✅ `requirements.txt`
- ✅ `README.md`
- ✅ `.gitignore`
- ✅ `.env.example` (arquivo de exemplo sem credenciais)
- ✅ Scripts `.sh`
- ✅ Documentação em `docs/`

## 🔒 Checklist de Segurança

Antes de fazer push, verifique:

- [ ] Arquivo `.env` está no `.gitignore` ✅
- [ ] Arquivo `.env.example` existe (sem credenciais reais) ✅
- [ ] Pasta `logs/` está no `.gitignore` ✅
- [ ] Arquivos `*_history.json` estão no `.gitignore` ✅
- [ ] Nenhuma chave privada está hardcoded no código
- [ ] README.md não contém credenciais reais

## 🔄 Atualizações Futuras

Para fazer updates depois:

```bash
# Ver o que mudou
git status

# Adicionar mudanças
git add .

# Fazer commit
git commit -m "Descrição das mudanças"

# Enviar para o GitHub
git push
```

## 🆘 Problemas Comuns

### Erro: "remote origin already exists"

```bash
# Remover remote existente
git remote remove origin

# Adicionar novamente com o URL correto
git remote add origin https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git
```

### Erro: "Authentication failed"

```bash
# Usar token de acesso pessoal ao invés de senha
# Veja: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token
```

### Arquivo sensível foi commitado por engano?

```bash
# Remover do histórico (CUIDADO!)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# Forçar push (apenas se necessário)
git push origin --force --all
```

## 📚 Recursos Adicionais

- [GitHub Docs](https://docs.github.com/)
- [Git Tutorial](https://git-scm.com/docs/gittutorial)
- [Gitignore Patterns](https://git-scm.com/docs/gitignore)

