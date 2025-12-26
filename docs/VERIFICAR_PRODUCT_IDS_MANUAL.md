# ⚠️ VERIFICAÇÃO URGENTE: Product IDs Incorretos

## Problema Identificado

Os preços mostrados nos logs estão **completamente incorretos**:

- **FARTCoin/USDT0**: Logs mostram ~2923, mas preço real é ~0.28993 (10.000x maior!)
- **ZEC/USDT0**: Logs mostram ~2922, mas preço real é ~438 (6-7x menor!)

Isso indica que os `product_ids` configurados estão **ERRADOS** e os bots estão obtendo preços de outros produtos.

## Product IDs Atualmente Configurados

```
Product ID 2:  BTC/USDT0     ✅ (preço parece correto: ~87000)
Product ID 18: ZEC/USDT0     ❌ (preço incorreto: ~2922, deveria ser ~438)
Product ID 22: FARTCoin/USDT0 ❌ (preço incorreto: ~2923, deveria ser ~0.29)
```

## Como Verificar os Product IDs Corretos

### Opção 1: Consultar Interface Web da Nado
1. Acesse a interface web da Nado Protocol
2. Verifique os símbolos/perpetuais disponíveis
3. Identifique os product_ids corretos para:
   - FARTCoin/USDT0 Perpetual
   - ZEC/USDT0 Perpetual

### Opção 2: Consultar API Diretamente

Execute este comando no terminal (fora do sandbox):

```bash
curl https://gateway.prod.nado.xyz/v1/symbols | python3 -m json.tool
```

Procure por:
- `FARTCOIN-PERP` ou `FART-PERP` ou similar
- `ZEC-PERP`

### Opção 3: Consultar Documentação

A documentação fornecida anteriormente mostra:
- https://docs.nado.xyz/developer-resources/api/symbols

Mas os preços indicam que pode estar desatualizada ou incorreta.

## Próximos Passos

**IMPORTANTE**: Você precisa:

1. **Identificar os product_ids corretos** usando um dos métodos acima
2. **Me informar os product_ids corretos** para que eu possa corrigir
3. **Reiniciar todos os bots** após a correção

## Estrutura Atual dos Arquivos

Os product_ids estão configurados em:
- `bot1.py` linha 27-29
- `bot2.py` linha 27-29  
- `bot3.py` linha 27-29
- `bot4.py` linha 27-29 (se aplicável)
- `bot.py` função `get_size_increment` (linhas 260-264)

## Suspeita

Os preços ~2922-2923 são muito próximos, o que sugere que:
- Ambos os produtos podem estar usando o mesmo product_id incorreto
- Ou ambos estão pegando preço de outro produto (talvez ETH-PERP ou similar)

**Precisamos descobrir os product_ids corretos antes de continuar operando!**


