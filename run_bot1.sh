#!/bin/bash
# Script para rodar apenas o Bot1 em background

# Criar diretório para logs se não existir
mkdir -p logs

# Rodar Bot 1 em background
nohup python3 bot1.py > logs/bot1.log 2>&1 &
echo "Bot1 iniciado em background (PID: $!)"
echo "Logs em: logs/bot1.log"
echo ""
echo "Para ver os logs em tempo real: tail -f logs/bot1.log"
echo "Para parar o Bot1: pkill -f 'python3 bot1.py'"






