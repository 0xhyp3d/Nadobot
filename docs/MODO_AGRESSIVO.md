# 🔥 Modo Agressivo - Guia Completo

## 📋 O que é o Modo Agressivo?

O **Modo Agressivo** é uma configuração opcional que otimiza os bots para **maior rentabilidade e volume**, com parâmetros mais agressivos de trading.

### ✅ Modo Padrão (Default - Menos Agressivo)
- Grid spacing: **0.05%** entre grids
- Max ordens: **5** por produto
- Grid levels: **3** níveis
- Quantidade: **200 USDC** por ordem
- Configuração conservadora, mais estável

### 🔥 Modo Agressivo (Turn ON)
- Grid spacing: **0.03%** entre grids (40% mais apertado)
- Max ordens: **8** por produto (60% mais ordens)
- Grid levels: **5** níveis (67% mais níveis)
- Quantidade: **150 USDC** por ordem (reduzido para evitar account health)
- Configuração otimizada para maior volume e rentabilidade

## 🚀 Como Ativar o Modo Agressivo

### Método 1: Via Arquivo .env (Recomendado)

Edite o arquivo `.env` (ou `.env.bot1`, `.env.bot2`, etc.) e adicione:

```bash
# Ativar modo agressivo para todos os bots
AGGRESSIVE_MODE=true
```

### Método 2: Via Arquivo .env Específico por Bot

Para ativar apenas em um bot específico:

**Para Bot1:**
```bash
# Editar .env.bot1 ou .env
AGGRESSIVE_MODE=true
```

**Para Bot2:**
```bash
# Editar .env.bot2 ou .env
AGGRESSIVE_MODE=true
```

### Método 3: Via Código (Avançado)

Edite o arquivo do bot (`bot1.py`, `bot2.py`, etc.) e adicione na configuração:

```python
config = {
    # ... outras configurações ...
    'aggressive_mode': True,  # Ativar modo agressivo
}
```

## 🔄 Como Desativar o Modo Agressivo

### Opção 1: Via .env (Recomendado)

Edite o arquivo `.env` e defina:

```bash
AGGRESSIVE_MODE=false
```

Ou simplesmente remova a linha `AGGRESSIVE_MODE=true`.

### Opção 2: Via Código

Edite o arquivo do bot e defina:

```python
'aggressive_mode': False,  # Desativar modo agressivo
```

## ⚠️ Importante: Reiniciar os Bots

**APÓS alterar o modo agressivo, você DEVE reiniciar os bots:**

```bash
./restart_bots.sh
```

Ou manualmente:
```bash
./stop_bots.sh
sleep 3
./start_all_bots.sh
```

## 📊 Verificar se o Modo Agressivo Está Ativo

Os logs mostrarão qual modo está ativo na inicialização:

### Modo Agressivo Ativo:
```
🔥 MODO AGRESSIVO ATIVADO - Parâmetros otimizados para maior rentabilidade e volume
  - Grid spacing: 0.03% (padrão: 0.05%)
  - Max ordens: 8 (padrão: 5)
  - Grid levels: 5 (padrão: 3)
  - Quantidade por ordem: 150 USDC
```

### Modo Padrão Ativo:
```
✅ MODO PADRÃO - Configuração conservadora ativa
```

## 🎯 Quando Usar Cada Modo?

### ✅ Use Modo Padrão (Default) quando:
- Quiser uma configuração estável e conservadora
- Tiver saldo limitado
- Estiver testando os bots pela primeira vez
- Quiser reduzir o risco de account health errors

### 🔥 Use Modo Agressivo quando:
- Quiser maximizar rentabilidade e volume
- Tiver saldo suficiente para suportar mais ordens
- Estiver confortável com mais trades
- Quiser aumentar a atividade do bot

## 🔍 Diferenças Detalhadas

| Parâmetro | Modo Padrão | Modo Agressivo | Diferença |
|-----------|-------------|----------------|-----------|
| Grid Spacing | 0.05% | 0.03% | 40% mais apertado |
| Max Ordens | 5 | 8 | 60% mais ordens |
| Grid Levels | 3 | 5 | 67% mais níveis |
| Quantidade/Ordem | 200 USDC | 150 USDC | 25% menor (para evitar account health) |
| Frequência de Trades | Normal | Alta | Mais oportunidades |
| Volume Total | Normal | Alto | Mais atividade |

## ⚡ Dicas de Uso

1. **Comece com Modo Padrão**: Se é a primeira vez usando os bots, comece com o modo padrão para entender o comportamento.

2. **Monitore os Erros**: Use `./verificar_erros.sh` para monitorar erros, especialmente "Insufficient account health".

3. **Ajuste a Quantidade**: Se receber muitos erros de account health, você pode reduzir `quantity_per_order_usdc` no código.

4. **Saldo Suficiente**: O modo agressivo cria mais ordens simultaneamente, então certifique-se de ter saldo suficiente.

## 🔧 Customização Avançada

Você pode customizar os parâmetros agressivos editando os arquivos dos bots:

```python
config = {
    'aggressive_mode': True,
    'aggressive_grid_spacing': 0.025,  # Customizar grid spacing agressivo
    'aggressive_max_orders': 10,  # Customizar max ordens agressivo
    'aggressive_grid_levels': 6,  # Customizar grid levels agressivo
    'aggressive_quantity_usdc': 180,  # Customizar quantidade agressiva
}
```

## 📝 Exemplo de Configuração Completa

**Arquivo `.env`:**
```bash
PRIVATE_KEY=0x...
NADO_NETWORK=mainnet
AGGRESSIVE_MODE=true  # <-- Ativar modo agressivo
```

**Reiniciar bots:**
```bash
./restart_bots.sh
```

**Verificar logs:**
```bash
./watch_bot1.sh
```

Você deve ver: `🔥 MODO AGRESSIVO ATIVADO`

