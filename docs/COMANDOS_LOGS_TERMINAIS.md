# 📺 Comandos para Acompanhar Logs dos Bots em Tempo Real

## Opção 1: Usando os Scripts (Recomendado)

### Terminal 1 - Bot1
```bash
cd /Users/igorbirni/Bot
./watch_bot1.sh
```

### Terminal 2 - Bot2
```bash
cd /Users/igorbirni/Bot
./watch_bot2.sh
```

### Terminal 3 - Bot3
```bash
cd /Users/igorbirni/Bot
./watch_bot3.sh
```

### Terminal 4 - Bot4
```bash
cd /Users/igorbirni/Bot
./watch_bot4.sh
```

---

## Opção 2: Comandos Diretos (Alternativa)

### Terminal 1 - Bot1
```bash
cd /Users/igorbirni/Bot && tail -f logs/bot1.log
```

### Terminal 2 - Bot2
```bash
cd /Users/igorbirni/Bot && tail -f logs/bot2.log
```

### Terminal 3 - Bot3
```bash
cd /Users/igorbirni/Bot && tail -f logs/bot3.log
```

### Terminal 4 - Bot4
```bash
cd /Users/igorbirni/Bot && tail -f logs/bot4.log
```

---

## Como Usar

1. **Abra 4 terminais diferentes** (ou use abas/painéis do seu terminal)

2. **Execute um comando diferente em cada terminal:**
   - Terminal 1: `./watch_bot1.sh` ou `tail -f logs/bot1.log`
   - Terminal 2: `./watch_bot2.sh` ou `tail -f logs/bot2.log`
   - Terminal 3: `./watch_bot3.sh` ou `tail -f logs/bot3.log`
   - Terminal 4: `./watch_bot4.sh` ou `tail -f logs/bot4.log`

3. **Os logs aparecerão em tempo real** conforme os bots executam operações

4. **Para parar**, pressione `Ctrl+C` no terminal correspondente

---

## Informações dos Bots

| Bot | Estratégia | Produtos | Leverage |
|-----|------------|----------|----------|
| Bot1 | Market Making / Scalping | BTC, FARTCoin, ZEC | 40x |
| Bot2 | Market Making / Scalping | BTC, FARTCoin, ZEC | 40x |
| Bot3 | Grid Trading (Geométrico) | BTC, FARTCoin, ZEC | 40x |
| Bot4 | Larry Williams %R (9,2) | BTC, FARTCoin, ZEC | 40x |

---

## Comandos Úteis Adicionais

### Ver apenas as últimas 50 linhas de um bot
```bash
tail -50 logs/bot1.log
```

### Filtrar logs por produto específico
```bash
tail -f logs/bot1.log | grep "BTC/USDT0"
```

### Ver apenas erros
```bash
tail -f logs/bot1.log | grep -i "error\|warning"
```

### Ver apenas ordens executadas
```bash
tail -f logs/bot1.log | grep -i "ORDEM\|Preço de mercado"
```


