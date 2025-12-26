# Configuração do Product ID para BTC/USDT0 Perpetual

## ⚠️ IMPORTANTE: Verificar o Product ID Correto

Os bots foram configurados para usar `product_id: 2` para BTC/USDT0 (Perpetual Futures), mas **você precisa confirmar qual é o product_id correto** na Nado Protocol.

### Como descobrir o Product ID correto:

1. Consulte a documentação da Nado Protocol
2. Ou verifique na interface web da Nado
3. Ou teste com diferentes IDs (1, 2, 3, etc.)

### Product IDs Comuns:
- `0`: USDT0 (moeda de margem)
- `1`: KBTC (Spot) - **não é este que queremos**
- `2`: BTC/USDT0 (Perpetual) - **provavelmente este, mas confirmar**

### Para alterar o Product ID:

Edite os arquivos `bot1.py`, `bot2.py`, e `bot3.py` e altere o número na linha `products`:

```python
'products': {
    2: {'name': 'BTC/USDT0', ...},  # <-- Alterar o número 2 para o ID correto
},
```

### Configuração Atual:

Todos os bots estão configurados para:
- ✅ **BTC/USDT0 Perpetual** (não KBTC spot)
- ✅ **Alavancagem 40x**
- ✅ Product ID: 2 (ajustar se necessário)




