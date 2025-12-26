#!/bin/bash

echo "═══════════════════════════════════════════════════════════"
echo "  🚀 INICIANDO TODOS OS BOTS"
echo "═══════════════════════════════════════════════════════════"
echo ""

cd "$(dirname "$0")"

echo "Iniciando Bot1..."
nohup python3 bot1.py > /dev/null 2>&1 &
BOT1_PID=$!
sleep 1

echo "Iniciando Bot2..."
nohup python3 bot2.py > /dev/null 2>&1 &
BOT2_PID=$!
sleep 1

echo "Iniciando Bot3..."
nohup python3 bot3.py > /dev/null 2>&1 &
BOT3_PID=$!
sleep 1

echo "Iniciando Bot4..."
nohup python3 bot4.py > /dev/null 2>&1 &
BOT4_PID=$!
sleep 2

echo ""
echo "✅ Todos os bots foram iniciados!"
echo ""
echo "Para verificar se estão rodando:"
echo "  ps aux | grep bot[1-4].py | grep -v grep"
echo ""
echo "Para ver os logs:"
echo "  tail -f logs/Bot1.log"
echo "  tail -f logs/Bot2.log"
echo "  tail -f logs/Bot3.log"
echo "  tail -f logs/Bot4.log"
echo ""
echo "═══════════════════════════════════════════════════════════"


