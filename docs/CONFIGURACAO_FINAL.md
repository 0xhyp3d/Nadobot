# ✅ Configuração Final - Product IDs Corretos

## Status Atual

Todos os bots foram configurados com os **product_ids corretos** conforme a documentação oficial da Nado: https://docs.nado.xyz/

## Product IDs Configurados

| Product ID | Símbolo | Nome Configurado | Tipo | Status |
|------------|---------|------------------|------|--------|
| 2 | BTC-PERP | BTC/USDT0 | Perpetual ✅ | Correto |
| 18 | ZEC-PERP | ZEC/USDT0 | Perpetual ✅ | Correto |
| 22 | FARTCOIN-PERP | FARTCoin/USDT0 | Perpetual ✅ | Correto |

## Arquivos Atualizados

Todos os 4 bots foram atualizados:

- ✅ **`bot1.py`** - Configurado com product_ids: 2, 18, 22
- ✅ **`bot2.py`** - Configurado com product_ids: 2, 18, 22
- ✅ **`bot3.py`** - Configurado com product_ids: 2, 18, 22
- ✅ **`bot4.py`** - Configurado com product_ids: 2, 18, 22
- ✅ **`bot.py`** - Função `get_size_increment()` atualizada para product_ids: 2, 18, 22

## Próximo Passo: Reiniciar os Bots

**IMPORTANTE**: Para aplicar as mudanças, você precisa **reiniciar todos os bots**:

```bash
./restart_bots.sh
```

Ou manualmente:
```bash
./stop_bots.sh
sleep 5
./start_all_bots.sh
```

## Como Verificar se Funcionou

Após reiniciar, verifique os logs para confirmar que os bots estão usando os product_ids corretos:

```bash
# Ver logs recentes do Bot1
tail -50 logs/bot1.log | grep -E "Product ID|BTC/USDT0|FARTCoin/USDT0|ZEC/USDT0"

# Ou usar os scripts de watch
./watch_bot1.sh
./watch_bot2.sh
./watch_bot3.sh
./watch_bot4.sh
```

Você deve ver nos logs:
- ✅ Product ID 2: BTC/USDT0 (preço ~87000-90000)
- ✅ Product ID 18: ZEC/USDT0 (preço ~400-500)
- ✅ Product ID 22: FARTCoin/USDT0 (preço ~0.28-0.30)
- ❌ **NÃO deve mais aparecer** Product ID 3 (WETH Spot) ou Product ID 4 (ETH-PERP)

## Referências

- Documentação oficial: https://docs.nado.xyz/
- API Symbols: https://docs.nado.xyz/developer-resources/api/symbols

## Observações

- Os bots estão configurados para operar em **perpetuais** com **40x leverage**
- Tamanho padrão de ordem: **250 USDC** por produto
- Os bots operam simultaneamente nos 3 produtos (BTC, FARTCoin, ZEC)
- Os erros de Cloudflare Challenge são temporários e não impedem o funcionamento dos bots


