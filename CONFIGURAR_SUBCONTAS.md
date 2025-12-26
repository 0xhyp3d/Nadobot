# 📋 Como Configurar Subcontas Separadas para Cada Bot

## 🎯 Visão Geral

Para rodar cada bot em uma subconta separada, você precisa alterar o parâmetro `subaccount_name` no arquivo de configuração de cada bot.

## ⚙️ Configuração

### 1. Editar os Arquivos dos Bots

Cada bot tem seu próprio arquivo de configuração onde você pode definir o nome da subconta:

#### Bot 1 (`bot1.py`)
```python
config = {
    'subaccount_name': "bot1",  # ← Alterar de "default" para "bot1"
    # ... outras configurações
}
```

#### Bot 2 (`bot2.py`)
```python
config = {
    'subaccount_name': "bot2",  # ← Alterar de "default" para "bot2"
    # ... outras configurações
}
```

#### Bot 3 (`bot3.py`)
```python
config = {
    'subaccount_name': "bot3",  # ← Alterar de "default" para "bot3"
    # ... outras configurações
}
```

#### Bot 4 (`bot4.py`)
```python
config = {
    'subaccount_name': "bot4",  # ← Alterar de "default" para "bot4"
    # ... outras configurações
}
```

### 2. Criar Subcontas na Nado Protocol

⚠️ **IMPORTANTE**: Você precisa criar as subcontas na Nado Protocol ANTES de iniciar os bots.

As subcontas são criadas usando a mesma chave privada (mesma wallet), mas com nomes diferentes. Cada subconta tem seu próprio saldo e histórico de ordens.

### 3. Distribuir Saldo nas Subcontas

Após criar as subcontas, você precisa distribuir o saldo entre elas. Isso geralmente é feito através da interface da Nado Protocol ou via SDK.

## 📝 Exemplo de Configuração Completa

Aqui está um exemplo de como configurar cada bot com sua própria subconta:

```python
# bot1.py
config = {
    'subaccount_name': "bot1",
    'leverage': 40,
    'products': { ... },
    # ... outras configurações
}

# bot2.py
config = {
    'subaccount_name': "bot2",
    'leverage': 40,
    'products': { ... },
    # ... outras configurações
}

# bot3.py
config = {
    'subaccount_name': "bot3",
    'leverage': 40,
    'products': { ... },
    # ... outras configurações
}

# bot4.py
config = {
    'subaccount_name': "bot4",
    'leverage': 40,
    'products': { ... },
    # ... outras configurações
}
```

## 🔑 Sobre Chaves Privadas

**IMPORTANTE**: Todos os bots podem usar a mesma chave privada (`PRIVATE_KEY`), pois as subcontas pertencem à mesma wallet. A diferença está apenas no nome da subconta.

Cada bot pode usar:
- A mesma chave privada (recomendado para subcontas da mesma wallet)
- OU chaves privadas diferentes (se quiser usar wallets completamente separadas)

## ✅ Benefícios de Usar Subcontas Separadas

1. **Isolamento de Saldo**: Cada bot opera com seu próprio saldo
2. **Isolamento de Ordens**: As ordens de cada bot ficam separadas
3. **Melhor Organização**: Fácil de rastrear o desempenho de cada bot
4. **Controle de Risco**: Limite de perdas por bot através do saldo da subconta

## 🚀 Iniciar os Bots

Após configurar, inicie os bots normalmente:

```bash
# Iniciar todos os bots
./iniciar_bots.sh

# Ou iniciar individualmente
python3 bot1.py &
python3 bot2.py &
python3 bot3.py &
python3 bot4.py &
```

## 📊 Verificar Status

Cada bot vai mostrar no log qual subconta está usando:

```
INICIANDO BOT DE TRADING NADO FUTURES
Subaccount: bot1  ← Nome da subconta
...
```

