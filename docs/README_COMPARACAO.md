# Comparação de Estratégias - Bot 1 vs Bot 2

Este projeto permite executar dois bots simultaneamente em contas diferentes para comparar estratégias.

## Estrutura

- `bot.py` - Classe base do bot (não execute diretamente)
- `bot1.py` - Bot 1 com estratégia original
- `bot2.py` - Bot 2 com estratégia customizável

## Configuração

### Arquivos .env

Você pode usar um dos seguintes métodos:

#### Método 1: Arquivos .env separados (Recomendado)

Crie dois arquivos `.env`:

**`.env.bot1`** (para Bot 1):
```env
PRIVATE_KEY=chave_privada_conta_1_aqui
NADO_NETWORK=mainnet
```

**`.env.bot2`** (para Bot 2):
```env
PRIVATE_KEY=chave_privada_conta_2_aqui
NADO_NETWORK=mainnet
```

#### Método 2: Variáveis no .env padrão

Crie um arquivo `.env`:
```env
PRIVATE_KEY_BOT1=chave_privada_conta_1_aqui
PRIVATE_KEY_BOT2=chave_privada_conta_2_aqui
NADO_NETWORK=mainnet
```

## Estratégias

### Bot 1 - Estratégia Original
- Grid Spacing: 0.05%
- Max Ordens: 5 por produto
- Stop Loss: 2%
- Take Profit: 4% (R:R 2:1)
- Grid Levels: 3
- Alavancagem: 40x

### Bot 2 - Estratégia Customizável
Edite os parâmetros em `bot2.py`:

```python
config = {
    'grid_spacing': 0.10,  # Ajuste o spread
    'max_open_orders_per_product': 10,  # Mais ordens
    'stop_loss_pct': 0.01,  # Stop Loss mais restritivo
    'take_profit_pct': 0.03,  # Take Profit (R:R 3:1)
    'grid_levels': 5,  # Mais níveis
    # ... outros parâmetros
}
```

## Como Executar

### Executar Bot 1:
```bash
python3 bot1.py
```

### Executar Bot 2:
```bash
python3 bot2.py
```

### Executar Ambos Simultaneamente:

Em terminais separados:
```bash
# Terminal 1
python3 bot1.py

# Terminal 2
python3 bot2.py
```

Ou usando `nohup` para executar em background:
```bash
nohup python3 bot1.py > bot1.log 2>&1 &
nohup python3 bot2.py > bot2.log 2>&1 &
```

## Logs

Cada bot tem seu próprio identificador nos logs:
- Bot1: `[Bot1]` no início de cada linha de log
- Bot2: `[Bot2]` no início de cada linha de log

Isso permite diferenciar facilmente as operações de cada bot mesmo quando executados simultaneamente.

## Comparação de Resultados

Monitore:
- Total de trades por bot
- Lucro/Prejuízo acumulado
- Taxa de sucesso
- Drawdown máximo
- Volume negociado

## Parâmetros Customizáveis

Você pode ajustar em `bot2.py`:

- `grid_spacing`: Espaçamento entre ordens (0.05 = 0.05%)
- `max_open_orders_per_product`: Máximo de ordens abertas
- `stop_loss_pct`: Stop Loss (0.02 = 2%)
- `take_profit_pct`: Take Profit (0.04 = 4%)
- `grid_levels`: Níveis de grid acima/abaixo do mercado
- `order_expiration`: Tempo de expiração das ordens (segundos)
- `leverage`: Alavancagem (40 = 40x)
- `min_balance`: Saldo mínimo necessário (USDT)

## Dicas

1. Comece com valores pequenos para testar
2. Monitore ambos os bots regularmente
3. Ajuste os parâmetros gradualmente
4. Mantenha logs separados para análise posterior
5. Use contas diferentes para evitar conflitos






