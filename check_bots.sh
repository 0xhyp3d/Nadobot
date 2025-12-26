#!/bin/bash
# Script para verificar se os bots estão rodando

echo "Verificando processos dos bots..."
echo ""

# Verificar Bot 1
if pgrep -f "python3 bot1.py" > /dev/null; then
    PID=$(pgrep -f "python3 bot1.py")
    echo "✅ Bot1 está rodando (PID: $PID)"
else
    echo "❌ Bot1 não está rodando"
fi

# Verificar Bot 2
if pgrep -f "python3 bot2.py" > /dev/null; then
    PID=$(pgrep -f "python3 bot2.py")
    echo "✅ Bot2 está rodando (PID: $PID)"
else
    echo "❌ Bot2 não está rodando"
fi

# Verificar Bot 3
if pgrep -f "python3 bot3.py" > /dev/null; then
    PID=$(pgrep -f "python3 bot3.py")
    echo "✅ Bot3 está rodando (PID: $PID)"
else
    echo "❌ Bot3 não está rodando"
fi
if pgrep -f "python3 bot4.py" > /dev/null; then
    PID=$(pgrep -f "python3 bot4.py")
    echo "✅ Bot4 está rodando (PID: $PID)"
else
    echo "❌ Bot4 não está rodando"
fi

echo ""
echo "Para ver os logs: tail -f logs/bot*.log"



