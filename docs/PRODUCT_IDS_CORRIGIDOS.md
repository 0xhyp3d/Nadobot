# ✅ Product IDs Corrigidos

## Correção Aplicada

Os product_ids foram corrigidos com base na documentação oficial da Nado Protocol:
https://docs.nado.xyz/developer-resources/api/symbols

## Product IDs Corretos

| Product ID | Símbolo | Nome Configurado | Tipo |
|------------|---------|------------------|------|
| 2 | BTC-PERP | BTC/USDT0 | Perpetual ✅ |
| 18 | ZEC-PERP | ZEC/USDT0 | Perpetual ✅ |
| 22 | FARTCOIN-PERP | FARTCoin/USDT0 | Perpetual ✅ |

## O que foi corrigido

### ❌ Antes (INCORRETO):
- Product ID 3 → WETH (Spot) - **ERRADO!**
- Product ID 4 → ETH-PERP - **ERRADO!**

### ✅ Agora (CORRETO):
- Product ID 2 → BTC-PERP ✅
- Product ID 18 → ZEC-PERP ✅
- Product ID 22 → FARTCOIN-PERP ✅

## Arquivos Atualizados

Todos os 4 bots foram atualizados:
- ✅ `bot1.py`
- ✅ `bot2.py`
- ✅ `bot3.py`
- ✅ `bot4.py`
- ✅ `bot.py` (função `get_size_increment` atualizada)

## Próximos Passos

**IMPORTANTE**: Você precisa reiniciar todos os bots para aplicar as mudanças:

```bash
./restart_bots.sh
```

Ou manualmente:
```bash
./stop_bots.sh
sleep 3
./start_all_bots.sh
```

## Verificação

Após reiniciar, os bots exibirão um log de inicialização mostrando os produtos configurados. Verifique se estão corretos:

```
============================================================
INICIALIZANDO Bot1
============================================================
Produtos configurados: 3 produto(s)
  - Product ID 2: BTC/USDT0
  - Product ID 18: ZEC/USDT0
  - Product ID 22: FARTCoin/USDT0
Alavancagem: 40x
Quantidade por ordem: 250 USDC
============================================================
```

## Observação sobre size_increment

A função `get_size_increment` foi atualizada para os novos product_ids:
- Product 2 (BTC-PERP): 0.00005 BTC
- Product 18 (ZEC-PERP): 0.001 (estimado)
- Product 22 (FARTCOIN-PERP): 0.001 (estimado)

Se houver erros de `size_increment` nos logs, pode ser necessário ajustar os valores para os produtos 18 e 22.


