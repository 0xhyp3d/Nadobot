# Como Reiniciar os Bots para Operar com FARTCoin

## ⚠️ IMPORTANTE

**SIM**, você precisa reiniciar os bots para que eles comecem a operar com FARTCoin/USDT0. As configurações de produtos são lidas apenas quando o bot é iniciado.

## Passos para Reiniciar:

### Opção 1: Parar e Iniciar Todos os Bots (Recomendado)

```bash
# 1. Parar todos os bots
./stop_bots.sh

# 2. Aguardar alguns segundos
sleep 3

# 3. Iniciar todos os bots novamente
./start_all_bots.sh
```

### Opção 2: Reiniciar Bots Individuais

```bash
# Parar um bot específico
pkill -f "python3 bot1.py"

# Aguardar
sleep 2

# Iniciar novamente
nohup python3 bot1.py > logs/bot1.log 2>&1 &
```

### Opção 3: Script de Reinício Automático

```bash
# Usar o script restart_bots.sh (se existir)
./restart_bots.sh
```

## Verificar se os Bots Estão Operando com FARTCoin:

Após reiniciar, verifique os logs para confirmar que os bots estão operando nos dois produtos:

```bash
# Ver logs em tempo real
tail -f logs/bot1.log

# Ou procurar por mensagens de FARTCoin
grep -i "fartcoin" logs/bot*.log
```

Você deve ver mensagens como:
```
[BTC/USDT0] Preço de mercado: 87329.50
[FARTCoin/USDT0] Preço de mercado: X.XX
```

## Observações:

- ⏱️ **Aguarde alguns segundos** entre parar e iniciar os bots
- 📊 Os bots começam a operar nos **dois produtos simultaneamente** após reiniciar
- 🔍 Se aparecerem erros de product_id inválido, você precisará ajustar o product_id do FARTCoin nos arquivos de configuração
- 💾 As ordens abertas antigas serão canceladas quando você parar os bots (devido ao `close_all_orders` no encerramento)

## Status Atual:

Após reiniciar, todos os 4 bots estarão configurados para:
- ✅ BTC/USDT0 (product_id: 2)
- ✅ FARTCoin/USDT0 (product_id: 3 - verificar se está correto)


