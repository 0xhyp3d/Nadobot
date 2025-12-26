#!/bin/bash

echo "═══════════════════════════════════════════════════════════"
echo "  🔄 MATANDO E REINICIANDO TODOS OS BOTS"
echo "═══════════════════════════════════════════════════════════"
echo ""

cd "$(dirname "$0")"

echo "1️⃣  Parando todos os bots..."
pkill -9 -f "python.*bot[1-4]\.py" 2>/dev/null
sleep 3

echo ""
echo "2️⃣  Verificando se todos os processos foram encerrados..."
REMAINING=$(ps aux | grep -E "python.*bot[1-4]\.py" | grep -v grep | wc -l | tr -d ' ' 2>/dev/null || echo "0")
if [ "$REMAINING" -gt 0 ]; then
    echo "⚠️  Ainda há $REMAINING processo(s) rodando. Listando:"
    ps aux | grep -E "python.*bot[1-4]\.py" | grep -v grep
    echo ""
    echo "Tentando matar novamente..."
    pkill -9 -f "bot[1-4]\.py"
    sleep 2
else
    echo "✅ Todos os bots foram parados com sucesso"
fi

echo ""
echo "3️⃣  Removendo TODOS os arquivos de histórico..."
rm -f logs/Bot1_history.json
rm -f logs/Bot2_history.json
rm -f logs/Bot3_history.json
rm -f logs/Bot4_history.json
rm -f logs/bot1_history.json
rm -f logs/bot2_history.json
rm -f logs/bot3_history.json
rm -f logs/bot4_history.json
rm -f logs/*_history.json
find logs/ -name "*history*.json" -type f -delete 2>/dev/null
echo "✅ Arquivos de histórico removidos"

echo ""
echo "4️⃣  Aguardando 2 segundos antes de reiniciar..."
sleep 2

echo ""
echo "5️⃣  Iniciando os bots..."
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
echo "6️⃣  Verificando se todos os bots iniciaram..."
sleep 2

BOT1_STATUS=$(ps aux | grep -E "python.*bot1\.py" | grep -v grep | wc -l | tr -d ' ' 2>/dev/null || echo "0")
BOT2_STATUS=$(ps aux | grep -E "python.*bot2\.py" | grep -v grep | wc -l | tr -d ' ' 2>/dev/null || echo "0")
BOT3_STATUS=$(ps aux | grep -E "python.*bot3\.py" | grep -v grep | wc -l | tr -d ' ' 2>/dev/null || echo "0")
BOT4_STATUS=$(ps aux | grep -E "python.*bot4\.py" | grep -v grep | wc -l | tr -d ' ' 2>/dev/null || echo "0")

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
echo "Aguarde alguns segundos e verifique os logs:"
echo "  tail -f logs/Bot1.log"
echo ""
echo "Você deve ver:"
echo "  • Data de HOJE (não de ontem)"
echo "  • ✅ Nenhum histórico encontrado. Iniciando do zero: 0 trades, 0.0000 USDT"
echo "  • Valores zerados: 0 trades, 0.0000 USDT"
echo ""
echo "Se ainda ver dados antigos, os processos não foram parados."
echo "Execute manualmente:"
echo "  pkill -9 -f 'python.*bot[1-4]\.py'"
echo "  ./reiniciar_bots.sh"
echo ""
echo "═══════════════════════════════════════════════════════════"


