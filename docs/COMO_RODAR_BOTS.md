# Como Rodar os Bots

## 🚨 IMPORTANTE: Fechar o Terminal Para os Bots!

Sim, quando você **fecha o terminal** ou usa **Ctrl+C**, os bots **param de rodar** porque o processo Python é terminado.

## Opções para Rodar os Bots

### Opção 1: Rodar em Background (Recomendado)

Use os scripts fornecidos para rodar os bots em background:

```bash
# Iniciar todos os bots em background
./run_bots_background.sh

# Verificar se estão rodando
./check_bots.sh

# Parar todos os bots
./stop_bots.sh
```

Os logs ficarão em `logs/bot1.log`, `logs/bot2.log`, `logs/bot3.log`

Para ver os logs em tempo real:
```bash
tail -f logs/bot*.log
```

### Opção 2: Usar Screen (Permite reconectar depois)

```bash
# Criar sessão screen
screen -S trading_bots

# Dentro do screen, rodar os bots normalmente
python3 bot1.py
# (em outro terminal ou sessão screen)
python3 bot2.py
# etc...

# Para desconectar (deixar rodando): Ctrl+A depois D
# Para reconectar: screen -r trading_bots
```

### Opção 3: Usar TMUX (Alternativa ao screen)

```bash
# Criar sessão tmux
tmux new -s trading_bots

# Rodar os bots
python3 bot1.py
# (Ctrl+B depois D para desconectar)

# Reconectar: tmux attach -t trading_bots
```

### Opção 4: Rodar Manualmente em Background

```bash
# Rodar um bot específico em background
nohup python3 bot1.py > logs/bot1.log 2>&1 &

# Ver processos rodando
ps aux | grep bot

# Parar um bot específico
pkill -f "python3 bot1.py"
```

## Verificar se Bots Estão Rodando

```bash
# Ver processos Python dos bots
ps aux | grep "bot.*.py"

# Ou usar o script
./check_bots.sh
```

## Parar os Bots

```bash
# Parar todos usando o script
./stop_bots.sh

# Ou parar individualmente
pkill -f "python3 bot1.py"
pkill -f "python3 bot2.py"
pkill -f "python3 bot3.py"
```

## Recomendação

Use a **Opção 1** (`run_bots_background.sh`) porque:
- ✅ Simples e fácil de usar
- ✅ Logs organizados
- ✅ Scripts para verificar e parar
- ✅ Continua rodando mesmo fechando o terminal




