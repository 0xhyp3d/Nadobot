# 🔍 Como Verificar Erros nos Logs dos Bots

Este guia mostra diferentes formas de verificar se há erros nos logs dos bots.

## 📋 Métodos Rápidos

### 1. Script Automático de Verificação de Erros

Execute o script que verifica todos os bots automaticamente:

```bash
./verificar_erros.sh
```

Este script mostra:
- ✅ Quantidade de erros encontrados
- 🌐 Bloqueios do Cloudflare
- ⚠️ Avisos (warnings)
- 📌 Últimos erros encontrados

---

### 2. Ver Últimos Erros Rapidamente

Para ver apenas as últimas linhas com erro de todos os bots:

```bash
./ver_ultimos_erros.sh
```

---

### 3. Ver Logs em Tempo Real

Para acompanhar os logs em tempo real e ver erros conforme aparecem:

**Bot1:**
```bash
./watch_bot1.sh
```

**Bot2:**
```bash
./watch_bot2.sh
```

**Bot3:**
```bash
./watch_bot3.sh
```

**Bot4:**
```bash
./watch_bot4.sh
```

**Todos os bots simultaneamente** (requer múltiplos terminais):
```bash
# Terminal 1
./watch_bot1.sh

# Terminal 2
./watch_bot2.sh

# Terminal 3
./watch_bot3.sh

# Terminal 4
./watch_bot4.sh
```

---

## 🔎 Buscar Erros Específicos

### Ver últimas linhas de um log específico:

```bash
# Últimas 50 linhas do Bot1
tail -50 logs/bot1.log

# Últimas 100 linhas do Bot2
tail -100 logs/bot2.log
```

### Buscar por palavra-chave específica:

```bash
# Buscar "error" no log do Bot1
grep -i "error" logs/bot1.log

# Buscar "cloudflare" em todos os logs
grep -i "cloudflare" logs/*.log

# Buscar "exception" no Bot2
grep -i "exception" logs/bot2.log
```

### Ver últimas linhas com erro:

```bash
# Últimas 20 linhas que contêm "error" ou "exception"
grep -i "error\|exception" logs/bot1.log | tail -20

# Últimas 10 linhas que contêm "cloudflare"
grep -i "cloudflare" logs/bot1.log | tail -10
```

---

## 📊 Tipos Comuns de Erros

### 1. Erros do Cloudflare
**Sintomas:**
```
Cloudflare Challenge
Just a moment...
<!DOCTYPE html>
```

**O que fazer:** O sistema já tem proteção automática que desabilita produtos com muitos erros. Se persistir, pode ser um problema temporário do Cloudflare.

---

### 2. Erros de Produto Desabilitado
**Sintomas:**
```
Product ID X está temporariamente desabilitado devido a erros do Cloudflare
```

**O que fazer:** Normal - o produto será reabilitado automaticamente após 10 minutos.

---

### 3. Erros de Size Increment
**Sintomas:**
```
Invalid order amount: Order amount must be divisible by the size_increment
```

**O que fazer:** Verifique se o `size_increment` está correto no código para o produto específico.

---

### 4. Erros de Saldo Insuficiente
**Sintomas:**
```
Insufficient balance
Not enough funds
```

**O que fazer:** Verifique o saldo da conta.

---

### 5. Erros de Conexão/API
**Sintomas:**
```
Connection error
API error
Network error
```

**O que fazer:** Verifique sua conexão com a internet e se a API da Nado está funcionando.

---

## 🔍 Comandos Úteis Adicionais

### Contar erros:
```bash
# Contar quantas vezes "error" aparece no log do Bot1
grep -i "error" logs/bot1.log | wc -l

# Contar "cloudflare" em todos os logs
grep -i "cloudflare" logs/*.log | wc -l
```

### Ver log completo desde o início:
```bash
# Ver todo o log do Bot1
cat logs/bot1.log

# Ver log com numeração de linhas
cat -n logs/bot1.log
```

### Filtrar apenas linhas importantes:
```bash
# Ver apenas linhas com ERROR, WARNING ou INFO de nível importante
grep -E "ERROR|WARNING|P/L|Total acumulado" logs/bot1.log
```

---

## 🚨 Quando Preocupar-se com Erros

✅ **Não se preocupe com:**
- Avisos (warnings) ocasionais
- Erros do Cloudflare que aparecem raramente
- Mensagens de produto temporariamente desabilitado (sistema automático funcionando)

❌ **Preocupe-se com:**
- Muitos erros consecutivos do mesmo tipo
- Erros que impedem o bot de operar
- Erros que aparecem em todos os bots simultaneamente
- Erros de autenticação ou permissão

---

## 📝 Exemplo de Uso Completo

```bash
# 1. Verificar erros rapidamente
./verificar_erros.sh

# 2. Se encontrar erros, ver detalhes
./ver_ultimos_erros.sh

# 3. Acompanhar em tempo real para ver se o erro persiste
./watch_bot1.sh

# 4. Se necessário, ver contexto completo do erro
grep -B 10 -A 10 "erro específico" logs/bot1.log
```

---

## 💡 Dica Final

Mantenha um terminal aberto com `./watch_bot1.sh` (ou outro bot) para monitorar em tempo real. Assim você verá os erros conforme eles aparecem e poderá identificar padrões.

