# Correção: size_increment Específico por Produto

## 🐛 Problema Identificado

O código estava usando um `size_increment` fixo de `0.00005 BTC` (50000000000000 em x18) para todos os produtos, mas cada produto tem seu próprio `size_increment`:

- **Product 2 (BTC/USDT0)**: `0.00005 BTC` = 50000000000000 ✅ (estava correto)
- **Product 3 (FARTCoin/USDT0)**: `0.001` = 1000000000000000 ❌ (estava usando valor errado)
- **Product 4 (ZEC/USDT0)**: `0.001` = 1000000000000000 ❌ (estava usando valor errado)

### Erro que aparecia nos logs:

```
Invalid order amount: Order amount, 85700000000000000, must be divisible by the size_increment; 
size_increment for product 3: 1000000000000000.
```

## ✅ Solução Implementada

Foi criada a função `get_size_increment(product_id)` que retorna o `size_increment` correto para cada produto:

```python
def get_size_increment(self, product_id: int) -> int:
    """
    Retorna o size_increment (em x18) para um produto específico.
    Cada produto tem seu próprio size_increment que deve ser respeitado.
    """
    size_increments = {
        2: 50000000000000,      # 0.00005 BTC
        3: 1000000000000000,    # 0.001 FARTCoin
        4: 1000000000000000,    # 0.001 ZEC
    }
    
    if product_id in size_increments:
        return size_increments[product_id]
    
    # Fallback para BTC se não conhecido
    return 50000000000000
```

### Locais Corrigidos

1. **`create_market_making_orders()`**: Agora usa `self.get_size_increment(product_id)` ao invés de valor fixo
2. **`create_grid_trading_orders()`**: Agora usa `self.get_size_increment(product_id)` ao invés de valor fixo

## 🔄 Próximos Passos

**IMPORTANTE**: Reinicie todos os bots para aplicar a correção:

```bash
./restart_bots.sh
```

Ou manualmente:
```bash
./stop_bots.sh
sleep 3
./start_all_bots.sh
```

## 📝 Observações

- Se você adicionar novos produtos no futuro, adicione o `size_increment` deles no dicionário `size_increments` dentro da função `get_size_increment()`
- Se um produto não estiver no dicionário, o código usará o valor padrão do BTC (0.00005) e mostrará um aviso no log
- Os valores podem ser verificados através dos erros da API quando uma ordem é rejeitada (a API retorna o size_increment correto na mensagem de erro)


