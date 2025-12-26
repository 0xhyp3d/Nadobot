# Como Reiniciar o Bot4

## 🔧 Reiniciar Apenas o Bot4

Se o `restart_bots.sh` não estiver funcionando para o Bot4, use o script específico:

```bash
./restart_bot4.sh
```

## Ou Manualmente

### Opção 1: Comandos Separados

```bash
# 1. Parar Bot4
pkill -f "python3 bot4.py"

# 2. Aguardar alguns segundos
sleep 3

# 3. Iniciar Bot4
nohup python3 bot4.py > logs/bot4.log 2>&1 &

# 4. Verificar logs
tail -f logs/bot4.log
```

### Opção 2: Um Comando

```bash
pkill -f "python3 bot4.py" && sleep 3 && nohup python3 bot4.py > logs/bot4.log 2>&1 & echo "Bot4 reiniciado (PID: $!)"
```

## 🔍 Verificar se o Bot4 está Rodando

```bash
# Verificar processo
ps aux | grep "python3 bot4.py" | grep -v grep

# Ver logs recentes
tail -20 logs/bot4.log

# Ver logs em tempo real
tail -f logs/bot4.log
```

## ⚠️ Problemas Comuns

### Erro de Permissão no .env

Se você ver erro `PermissionError: [Errno 1] Operation not permitted: '/Users/igorbirni/Bot/.env'`:
- Isso é um problema do ambiente sandbox do Cursor, não do código
- Execute os comandos diretamente no terminal (fora do Cursor) para evitar esse erro

### Bot4 não inicia

1. Verifique se o arquivo `bot4.py` existe e tem permissão de execução
2. Verifique os logs: `cat logs/bot4.log`
3. Tente executar diretamente: `python3 bot4.py` (sem nohup) para ver erros

## 📝 Observação sobre ZEC/USDT0

Após reiniciar, o Bot4 começará a coletar candles para os 3 produtos:
- BTC/USDT0
- FARTCoin/USDT0  
- ZEC/USDT0 (novo!)

Cada produto precisa de ~45 minutos (9 candles de 5 minutos) antes de começar a gerar sinais.


