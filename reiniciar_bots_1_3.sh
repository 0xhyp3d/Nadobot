#!/bin/bash

echo "═══════════════════════════════════════════════════════════"
echo "  🔄 REINICIANDO BOTS 1, 2 e 3"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Mudar para o diretório do projeto
cd "$(dirname "$0")"

echo "1️⃣  Parando bots 1, 2 e 3..."
pkill -f "python.*bot1\.py" 2>/dev/null
pkill -f "python.*bot2\.py" 2>/dev/null
pkill -f "python.*bot3\.py" 2>/dev/null
sleep 3

echo ""
echo "2️⃣  Verificando se todos os processos foram encerrados..."
REMAINING=$(pgrep -f "python.*bot[1-3]\.py" 2>/dev/null | wc -l | tr -d ' ' 2>/dev/null || echo "0")
if [ "$REMAINING" -gt 0 ]; then
    echo "⚠️  Ainda há $REMAINING processo(s) rodando. Forçando encerramento..."
    pkill -9 -f "bot1\.py"
    pkill -9 -f "bot2\.py"
    pkill -9 -f "bot3\.py"
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
sleep 2

echo ""
echo "5️⃣  Verificando se todos os bots iniciaram..."
sleep 2

BOT1_STATUS=$(pgrep -f "bot1.py" 2>/dev/null | wc -l | tr -d ' ' 2>/dev/null || echo "0")
BOT2_STATUS=$(pgrep -f "bot2.py" 2>/dev/null | wc -l | tr -d ' ' 2>/dev/null || echo "0")
BOT3_STATUS=$(pgrep -f "bot3.py" 2>/dev/null | wc -l | tr -d ' ' 2>/dev/null || echo "0")

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

TOTAL=$((BOT1_STATUS + BOT2_STATUS + BOT3_STATUS))
echo ""
if [ "$TOTAL" -eq 3 ]; then
    echo "✅ TODOS os 3 bots estão rodando!"
else
    echo "⚠️  Apenas $TOTAL de 3 bots estão rodando"
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
echo ""
echo "Para verificar se estão operando:"
echo "  ps aux | grep bot[1-3].py"
echo ""
echo "═══════════════════════════════════════════════════════════"


