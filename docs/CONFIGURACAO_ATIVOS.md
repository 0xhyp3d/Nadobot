# Configuração de Ativos nos Bots

## 📊 Ativos Configurados

Todos os 4 bots estão configurados para operar nos seguintes ativos:

| Product ID | Nome | Tipo | Status |
|------------|------|------|--------|
| 2 | BTC/USDT0 | Perpetual | ✅ Confirmado |
| 3 | FARTCoin/USDT0 | Perpetual | ⚠️ Verificar |
| 4 | ZEC/USDT0 | Perpetual | ⚠️ Verificar |

## ⚠️ IMPORTANTE: Verificar Product IDs

Os product_ids podem variar na Nado Protocol. Você precisa confirmar se os IDs estão corretos:

- **Product ID 2 (BTC/USDT0)**: Provavelmente correto, mas confirmar
- **Product ID 3 (FARTCoin/USDT0)**: **VERIFICAR** se está correto
- **Product ID 4 (ZEC/USDT0)**: **VERIFICAR** se está correto

### Como descobrir o Product ID correto:

1. Consulte a documentação da Nado Protocol
2. Verifique na interface web da Nado
3. Teste com diferentes IDs se necessário
4. Os logs mostrarão erros se o product_id estiver incorreto

### Para alterar um Product ID:

Edite os arquivos `bot1.py`, `bot2.py`, `bot3.py`, e `bot4.py` e altere o número na seção `products`:

```python
'products': {
    2: {'name': 'BTC/USDT0'},
    3: {'name': 'FARTCoin/USDT0'},  # <-- Alterar o número se necessário
    4: {'name': 'ZEC/USDT0'},       # <-- Alterar o número se necessário
},
```

## 🚀 Como Funciona

- Os bots operam **simultaneamente** nos 3 produtos
- Cada produto tem seus próprios limites de ordens abertas (`max_open_orders_per_product`)
- O gerenciamento de risco (Stop Loss, Take Profit) é aplicado **por produto**
- Os logs mostrarão qual produto está sendo negociado: `[BTC/USDT0]`, `[FARTCoin/USDT0]`, ou `[ZEC/USDT0]`

## 🔄 Para Aplicar Mudanças

**IMPORTANTE**: Após alterar os product_ids, você precisa **reiniciar os bots**:

```bash
./restart_bots.sh
```

Ou manualmente:
```bash
./stop_bots.sh
sleep 3
./start_all_bots.sh
```

## 📝 Observações Especiais

### Bot4 (Williams %R)

O Bot4 tem uma configuração especial porque precisa coletar candles de 5 minutos para cada produto separadamente:
- Cada produto (BTC, FARTCoin, ZEC) terá seu próprio conjunto de candles
- Cada produto precisa de ~45 minutos (9 candles) antes de começar a gerar sinais
- Os candles são coletados independentemente para cada produto


