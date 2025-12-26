# 📚 Documentação Completa da Nado Protocol

## Links Importantes

- **Documentação Principal**: https://docs.nado.xyz/
- **Documentação de Símbolos (Product IDs)**: https://docs.nado.xyz/developer-resources/api/symbols
- **Python SDK**: https://docs.nado.xyz/developer-resources/python-sdk

## Product IDs Configurados

Conforme a documentação oficial em https://docs.nado.xyz/developer-resources/api/symbols:

| Product ID | Símbolo | Nome Configurado | Tipo |
|------------|---------|------------------|------|
| 2 | BTC-PERP | BTC/USDT0 | Perpetual ✅ |
| 18 | ZEC-PERP | ZEC/USDT0 | Perpetual ✅ |
| 22 | FARTCOIN-PERP | FARTCoin/USDT0 | Perpetual ✅ |

## Verificação de Configuração

✅ Todos os bots estão configurados com os product_ids corretos conforme a documentação oficial.

✅ Os arquivos de configuração (`bot1.py`, `bot2.py`, `bot3.py`, `bot4.py`) estão usando os product_ids corretos.

## Observações Importantes

1. **Documentação de Referência**: Sempre consulte https://docs.nado.xyz/ para qualquer dúvida sobre a API ou SDK.

2. **Product IDs**: Os product_ids podem mudar com o tempo. Sempre consulte https://docs.nado.xyz/developer-resources/api/symbols para verificar os IDs atuais.

3. **Preços**: Se os preços parecerem incorretos, verifique:
   - Se os product_ids estão corretos
   - Se a conversão de x18 para float está sendo feita corretamente
   - Se a API está retornando os dados esperados

4. **Troubleshooting**: Em caso de problemas, consulte:
   - Logs dos bots em `logs/`
   - Documentação da API: https://docs.nado.xyz/developer-resources/api
   - Documentação do Python SDK: https://docs.nado.xyz/developer-resources/python-sdk


