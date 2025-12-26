#!/bin/bash
# Script para iniciar todos os bots

echo "Iniciando todos os bots..."

# Criar diretório para logs se não existir
mkdir -p logs

# Parar bots existentes (se houver)
pkill -f "python3 bot1.py" 2>/dev/null
pkill -f "python3 bot2.py" 2>/dev/null
pkill -f "python3 bot3.py" 2>/dev/null
sleep 1

# Iniciar todos os bots em background
nohup python3 bot1.py > logs/bot1.log 2>&1 &
BOT1_PID=$!
echo "✅ Bot1 iniciado (PID: $BOT1_PID)"

nohup python3 bot2.py > logs/bot2.log 2>&1 &
BOT2_PID=$!
echo "✅ Bot2 iniciado (PID: $BOT2_PID)"

nohup python3 bot3.py > logs/bot3.log 2>&1 &
BOT3_PID=$!
echo "✅ Bot3 iniciado (PID: $BOT3_PID)"

nohup python3 bot4.py > logs/bot4.log 2>&1 &
BOT4_PID=$!
echo "✅ Bot4 iniciado (PID: $BOT4_PID)"

echo ""
echo "Todos os bots foram iniciados!"
echo ""
echo "Para visualizar os logs em terminais separados:"
echo "  Terminal 1: ./watch_bot1.sh"
echo "  Terminal 2: ./watch_bot2.sh"
echo "  Terminal 3: ./watch_bot3.sh"
echo ""
echo "Ou para parar todos os bots: ./stop_bots.sh"

