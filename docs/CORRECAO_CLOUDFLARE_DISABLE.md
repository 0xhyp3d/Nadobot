# Correção: Desabilitação Temporária de Produtos com Erros do Cloudflare

## 🐛 Problema Identificado

Os bots estavam tentando continuamente operar FARTCoin/USDT0 e ZEC/USDT0 mesmo quando o Cloudflare estava bloqueando todas as requisições para esses produtos. Isso resultava em:

- Muitos erros nos logs
- Bots gastando recursos tentando produtos que não funcionavam
- Nenhum trade sendo executado para esses produtos (conforme reportado pelo usuário)

## ✅ Solução Implementada

Foi implementado um sistema de rastreamento de erros do Cloudflare por produto que:

1. **Conta erros consecutivos**: Cada produto tem um contador de erros do Cloudflare
2. **Desabilita temporariamente**: Após 5 erros consecutivos, o produto é desabilitado por 10 minutos
3. **Reabilita automaticamente**: Após o período de cooldown, o produto é reabilitado
4. **Reseta em caso de sucesso**: Se uma requisição for bem-sucedida, o contador de erros é resetado

### Mudanças no Código

1. **Novos atributos na classe `NadoFuturesBot`**:
   - `product_cloudflare_errors`: Dicionário que rastreia contadores de erros por produto
   - `product_disabled_until`: Dicionário que armazena timestamps de quando produtos serão reabilitados
   - `max_cloudflare_errors`: 5 (máximo de erros antes de desabilitar)
   - `disabled_cooldown`: 600 segundos (10 minutos)

2. **Novos métodos**:
   - `is_product_disabled(product_id)`: Verifica se um produto está desabilitado
   - `record_cloudflare_error(product_id)`: Registra um erro e desabilita se necessário
   - `record_cloudflare_success(product_id)`: Reseta contador de erros em caso de sucesso

3. **Funções atualizadas**:
   - `get_market_price()`: Agora verifica se produto está desabilitado antes de fazer requisição
   - `create_market_making_orders()`: Pula produtos desabilitados
   - `create_grid_trading_orders()`: Pula produtos desabilitados

## 📊 Comportamento Esperado

### Antes (Problema)
- Bots tentavam FARTCoin e ZEC continuamente mesmo com Cloudflare bloqueando
- Muitos erros nos logs
- Nenhum trade sendo executado

### Depois (Solução)
- Após 5 erros consecutivos, FARTCoin e ZEC são desabilitados por 10 minutos
- Bots focam apenas em BTC (que está funcionando)
- Após 10 minutos, tenta novamente
- Se funcionar, continua operando normalmente
- Se continuar bloqueado, desabilita novamente

## 🔄 Próximos Passos

**IMPORTANTE**: Reinicie todos os bots para aplicar a correção:

```bash
./restart_bots.sh
```

## 📝 Observações

- O sistema é automático e não requer intervenção manual
- Produtos desabilitados são automaticamente reabilitados após o cooldown
- O sistema registra logs quando produtos são desabilitados/reabilitados
- BTC continuará funcionando normalmente mesmo se FARTCoin e ZEC estiverem desabilitados


