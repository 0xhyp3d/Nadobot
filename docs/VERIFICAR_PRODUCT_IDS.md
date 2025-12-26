# ⚠️ IMPORTANTE: Verificar Product IDs Corretos

## Problema Identificado

Os bots estão operando em produtos incorretos:
- ❌ **WETH/USDT0 (Spot)** - não deveria estar operando
- ❌ **ETH/USDT0 (Perp)** - não deveria estar operando

## Produtos Desejados

Os bots devem operar APENAS em:
- ✅ **BTC/USDT0 (Perp)**
- ✅ **FARTCoin/USDT0 (Perp)**
- ✅ **ZEC/USDT0 (Perp)**

## Como Descobrir os Product IDs Corretos

Você precisa descobrir quais são os product_ids corretos para esses 3 produtos na Nado Protocol. Algumas formas de descobrir:

### Opção 1: Consultar a Documentação/API
1. Acesse a documentação da Nado Protocol
2. Procure pela lista de produtos/perpetuais disponíveis
3. Identifique os product_ids para BTC/USDT0, FARTCoin/USDT0 e ZEC/USDT0

### Opção 2: Verificar na Interface Web
1. Acesse a interface web da Nado
2. Navegue até a seção de trading/perpetuais
3. Inspecione o código da página (F12) ou verifique os IDs dos produtos

### Opção 3: Testar Product IDs
Você pode testar diferentes product_ids. Os logs mostrarão erros se o product_id estiver incorreto.

### Opção 4: Consultar Logs de Ordens
Se você souber qual product_id corresponde a cada produto que está sendo tradado incorretamente, podemos fazer o mapeamento reverso.

## Product IDs Atualmente Configurados

Atualmente os bots estão configurados com:
- `product_id: 2` → mas está operando em WETH/USDT0 ou ETH/USDT0 (precisa corrigir)
- `product_id: 3` → mas está operando em produto incorreto (precisa corrigir)
- `product_id: 4` → mas está operando em produto incorreto (precisa corrigir)

## Como Corrigir

Assim que você souber os product_ids corretos, me informe e eu atualizarei todos os arquivos de configuração dos bots.

### Exemplo de configuração correta:

```python
'products': {
    X: {'name': 'BTC/USDT0'},      # Substituir X pelo product_id correto
    Y: {'name': 'FARTCoin/USDT0'}, # Substituir Y pelo product_id correto
    Z: {'name': 'ZEC/USDT0'},      # Substituir Z pelo product_id correto
},
```

## Arquivos que serão atualizados

- `bot1.py`
- `bot2.py`
- `bot3.py`
- `bot4.py`

## Após corrigir

Após atualizar os product_ids, você precisa reiniciar todos os bots:

```bash
./restart_bots.sh
```

## Logs de Inicialização

Agora os bots exibem um log na inicialização mostrando quais produtos estão configurados. Isso ajudará a verificar se a configuração está correta.


