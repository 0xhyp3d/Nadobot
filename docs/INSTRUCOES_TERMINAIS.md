# Instruções para Visualizar Logs em 3 Terminais Separados

## Passo 1: Iniciar Todos os Bots
Execute em qualquer terminal:
```bash
./start_all_bots.sh
```

## Passo 2: Abrir 3 Terminais e Visualizar Logs

### Terminal 1 - Bot1:
```bash
cd /Users/igorbirni/Bot
./watch_bot1.sh
```

### Terminal 2 - Bot2:
```bash
cd /Users/igorbirni/Bot
./watch_bot2.sh
```

### Terminal 3 - Bot3:
```bash
cd /Users/igorbirni/Bot
./watch_bot3.sh
```

---

## Alternativa: Abrir Terminais Automaticamente (macOS)

Se você quiser abrir 3 terminais automaticamente, execute:

```bash
osascript -e 'tell app "Terminal" to do script "cd /Users/igorbirni/Bot && ./watch_bot1.sh"'
osascript -e 'tell app "Terminal" to do script "cd /Users/igorbirni/Bot && ./watch_bot2.sh"'
osascript -e 'tell app "Terminal" to do script "cd /Users/igorbirni/Bot && ./watch_bot3.sh"'
```

---

## Comandos Úteis

### Parar todos os bots:
```bash
./stop_bots.sh
```

### Verificar status dos bots:
```bash
./check_bots.sh
```

### Ver últimas linhas de um log específico:
```bash
tail -20 logs/bot1.log
tail -20 logs/bot2.log
tail -20 logs/bot3.log
```


