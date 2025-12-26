# Configuração do Product ID para FARTCoin/USDT0 Perpetual

## ⚠️ IMPORTANTE: Verificar o Product ID Correto

Os bots foram configurados para usar `product_id: 3` para FARTCoin/USDT0 (Perpetual Futures), mas **você precisa confirmar qual é o product_id correto** na Nado Protocol.

### Como descobrir o Product ID correto:

1. Consulte a documentação da Nado Protocol
2. Ou verifique na interface web da Nado
3. Ou teste com diferentes IDs (3, 4, 5, etc.)
4. Ou consulte os logs quando o bot tentar operar - erros de product_id inválido aparecerão

### Product IDs Configurados:

- `2`: BTC/USDT0 (Perpetual) ✅
- `3`: FARTCoin/USDT0 (Perpetual) ⚠️ **VERIFICAR**

### Para alterar o Product ID do FARTCoin:

Edite os arquivos `bot1.py`, `bot2.py`, `bot3.py`, e `bot4.py` e altere o número na linha `products`:

```python
'products': {
    2: {'name': 'BTC/USDT0'},
    3: {'name': 'FARTCoin/USDT0'},  # <-- Alterar o número 3 para o ID correto
},
```

### Configuração Atual:

Todos os 4 bots agora estão configurados para operar em:
- ✅ **BTC/USDT0 Perpetual** (product_id: 2)
- ✅ **FARTCoin/USDT0 Perpetual** (product_id: 3 - verificar se está correto)
- ✅ **Alavancagem 40x** em ambos
- ✅ **250 USDC por ordem** em ambos

### Observações:

- Os bots operarão **simultaneamente** nos dois produtos
- Cada produto terá seus próprios limites de ordens abertas (max_open_orders_per_product)
- O gerenciamento de risco é aplicado **por produto**
- Os logs mostrarão qual produto está sendo negociado: `[BTC/USDT0]` ou `[FARTCoin/USDT0]`


