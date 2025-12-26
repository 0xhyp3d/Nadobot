#!/bin/bash
# Script para rodar bots em background (nohup)

# Criar diretório para logs se não existir
mkdir -p logs

# Rodar Bot 1 em background
nohup python3 bot1.py > logs/bot1.log 2>&1 &
echo "Bot1 iniciado em background (PID: $!)"
echo "Logs em: logs/bot1.log"

# Rodar Bot 2 em background
nohup python3 bot2.py > logs/bot2.log 2>&1 &
echo "Bot2 iniciado em background (PID: $!)"
echo "Logs em: logs/bot2.log"

# Rodar Bot 3 em background
nohup python3 bot3.py > logs/bot3.log 2>&1 &
echo "Bot3 iniciado em background (PID: $!)"
echo "Logs em: logs/bot3.log"

echo ""
echo "Todos os bots foram iniciados em background!"
echo "Para ver os logs em tempo real: tail -f logs/bot*.log"
echo "Para parar os bots: ./stop_bots.sh"







