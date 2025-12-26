#!/bin/bash

echo "═══════════════════════════════════════════════════════════"
echo "  🔄 REINICIANDO TODOS OS BOTS"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Mudar para o diretório do projeto
cd "$(dirname "$0")"

echo "1️⃣  Parando todos os bots..."
pkill -f "python.*bot[1-4]\.py"
sleep 3

echo ""
echo "2️⃣  Verificando se todos os processos foram encerrados..."
REMAINING=$(pgrep -f "bot[1-4]\.py" 2>/dev/null | wc -l | tr -d ' ')
if [ "$REMAINING" -gt 0 ]; then
    echo "⚠️  Ainda há $REMAINING processo(s) rodando. Forçando encerramento..."
    pkill -9 -f "bot[1-4]\.py"
    sleep 2
else
    echo "✅ Todos os bots foram parados com sucesso"
fi

echo ""
echo "3️⃣  Aguardando 2 segundos antes de reiniciar..."
sleep 2

echo ""
echo "4️⃣  Iniciando os bots..."
echo ""

# Iniciar cada bot em background
echo "  → Iniciando Bot1..."
nohup python3 bot1.py > /dev/null 2>&1 &
BOT1_PID=$!
sleep 1

echo "  → Iniciando Bot2..."
nohup python3 bot2.py > /dev/null 2>&1 &
BOT2_PID=$!
sleep 1

echo "  → Iniciando Bot3..."
nohup python3 bot3.py > /dev/null 2>&1 &
BOT3_PID=$!
sleep 1

echo "  → Iniciando Bot4..."
nohup python3 bot4.py > /dev/null 2>&1 &
BOT4_PID=$!
sleep 2

echo ""
echo "5️⃣  Verificando se todos os bots iniciaram..."
sleep 2

BOT1_STATUS=$(pgrep -f "bot1.py" 2>/dev/null | wc -l | tr -d ' ')
BOT2_STATUS=$(pgrep -f "bot2.py" 2>/dev/null | wc -l | tr -d ' ')
BOT3_STATUS=$(pgrep -f "bot3.py" 2>/dev/null | wc -l | tr -d ' ')
BOT4_STATUS=$(pgrep -f "bot4.py" 2>/dev/null | wc -l | tr -d ' ')

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  ✅ STATUS FINAL"
echo "═══════════════════════════════════════════════════════════"
echo ""

if [ "$BOT1_STATUS" -gt 0 ]; then
    echo "✅ Bot1: RODANDO"
else
    echo "❌ Bot1: FALHOU ao iniciar"
fi

if [ "$BOT2_STATUS" -gt 0 ]; then
    echo "✅ Bot2: RODANDO"
else
    echo "❌ Bot2: FALHOU ao iniciar"
fi

if [ "$BOT3_STATUS" -gt 0 ]; then
    echo "✅ Bot3: RODANDO"
else
    echo "❌ Bot3: FALHOU ao iniciar"
fi

if [ "$BOT4_STATUS" -gt 0 ]; then
    echo "✅ Bot4: RODANDO"
else
    echo "❌ Bot4: FALHOU ao iniciar"
fi

TOTAL=$((BOT1_STATUS + BOT2_STATUS + BOT3_STATUS + BOT4_STATUS))
echo ""
if [ "$TOTAL" -eq 4 ]; then
    echo "✅ TODOS os 4 bots estão rodando!"
else
    echo "⚠️  Apenas $TOTAL de 4 bots estão rodando"
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  📋 PRÓXIMOS PASSOS"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Para verificar os logs em tempo real:"
echo "  tail -f logs/Bot1.log"
echo "  tail -f logs/Bot2.log"
echo "  tail -f logs/Bot3.log"
echo "  tail -f logs/Bot4.log"
echo ""
echo "Para verificar se estão operando:"
echo "  ps aux | grep bot[1-4].py"
echo ""
echo "═══════════════════════════════════════════════════════════"

