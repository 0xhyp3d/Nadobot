#!/bin/bash

echo "═══════════════════════════════════════════════════════════"
echo "  🔥 FORÇAR RESET COMPLETO - MATANDO TUDO"
echo "═══════════════════════════════════════════════════════════"
echo ""

cd "$(dirname "$0")"

echo "1️⃣  Matando TODOS os processos Python relacionados aos bots..."
# Tentar múltiplas formas de matar
pkill -9 -f "python.*bot[1-4]\.py" 2>/dev/null
pkill -9 -f "bot1.py" 2>/dev/null
pkill -9 -f "bot2.py" 2>/dev/null
pkill -9 -f "bot3.py" 2>/dev/null
pkill -9 -f "bot4.py" 2>/dev/null
killall -9 python3 2>/dev/null || true
sleep 3

echo ""
echo "2️⃣  Verificando processos restantes..."
PROCS=$(ps aux | grep -E "python.*bot[1-4]\.py" | grep -v grep | wc -l | tr -d ' ' || echo "0")
if [ "$PROCS" != "0" ]; then
    echo "⚠️  Ainda há processos. Listando:"
    ps aux | grep -E "python.*bot[1-4]\.py" | grep -v grep
    echo ""
    echo "Tente matar manualmente os PIDs acima"
else
    echo "✅ Nenhum processo encontrado"
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
echo "4️⃣  Verificando se os arquivos foram removidos..."
REMAINING=$(find logs -name "*history*.json" -type f 2>/dev/null | wc -l | tr -d ' ' || echo "0")
if [ "$REMAINING" = "0" ]; then
    echo "✅ Todos os arquivos de histórico foram removidos"
else
    echo "⚠️  Ainda há $REMAINING arquivo(s) de histórico:"
    find logs -name "*history*.json" -type f 2>/dev/null
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  ✅ RESET COMPLETO FINALIZADO"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "IMPORTANTE: Os bots foram PARADOS."
echo ""
echo "Agora execute para REINICIAR:"
echo "  ./reiniciar_bots.sh"
echo ""
echo "Os bots vão iniciar com:"
echo "  • Código atualizado (com logs melhorados)"
echo "  • Histórico zerado (0 trades, 0.0000 USDT)"
echo "  • Modo padrão (agressivo desativado)"
echo ""
echo "Nos logs você verá:"
echo "  ✅ Nenhum histórico encontrado. Iniciando do zero: 0 trades, 0.0000 USDT"
echo ""
echo "═══════════════════════════════════════════════════════════"


