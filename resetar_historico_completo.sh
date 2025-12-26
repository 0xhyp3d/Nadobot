#!/bin/bash

echo "═══════════════════════════════════════════════════════════"
echo "  🔄 RESET COMPLETO DE HISTÓRICO"
echo "═══════════════════════════════════════════════════════════"
echo ""

cd "$(dirname "$0")"

echo "1️⃣  Parando TODOS os processos dos bots..."
pkill -9 -f "python.*bot[1-4]\.py" 2>/dev/null
sleep 5

echo ""
echo "2️⃣  Removendo TODOS os arquivos de histórico..."
rm -f logs/Bot1_history.json
rm -f logs/Bot2_history.json
rm -f logs/Bot3_history.json
rm -f logs/Bot4_history.json
rm -f logs/bot1_history.json
rm -f logs/bot2_history.json
rm -f logs/bot3_history.json
rm -f logs/bot4_history.json
rm -f logs/*_history.json
# Remover também de subpastas (como backup_antes_correcao_pl)
find logs/ -name "*history*.json" -type f -delete 2>/dev/null

echo ""
echo "3️⃣  Verificando se os arquivos foram removidos..."
REMAINING=$(find logs -name "*history*.json" -type f 2>/dev/null | grep -v backup | wc -l | tr -d ' ')
if [ "$REMAINING" -eq 0 ]; then
    echo "✅ Todos os arquivos de histórico foram removidos"
else
    echo "⚠️  Ainda há $REMAINING arquivo(s) de histórico:"
    find logs -name "*history*.json" -type f 2>/dev/null | grep -v backup
fi

echo ""
echo "4️⃣  Verificando se ainda há processos rodando..."
REMAINING_PROCS=$(pgrep -f "bot[1-4]\.py" 2>/dev/null | wc -l | tr -d ' ' 2>/dev/null || echo "0")
if [ "$REMAINING_PROCS" = "0" ] || [ -z "$REMAINING_PROCS" ]; then
    echo "✅ Todos os processos foram encerrados"
else
    echo "⚠️  Ainda há $REMAINING_PROCS processo(s) rodando. Tentando matar novamente..."
    pkill -9 -f "bot[1-4]\.py" 2>/dev/null
    sleep 3
    # Verificar novamente
    REMAINING_PROCS2=$(pgrep -f "bot[1-4]\.py" 2>/dev/null | wc -l | tr -d ' ' 2>/dev/null || echo "0")
    if [ "$REMAINING_PROCS2" = "0" ] || [ -z "$REMAINING_PROCS2" ]; then
        echo "✅ Processos encerrados após segunda tentativa"
    else
        echo "⚠️  Ainda há processos. Tente matar manualmente: pkill -9 -f 'python.*bot[1-4]\.py'"
    fi
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  ✅ RESET COMPLETO FINALIZADO"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Agora você pode reiniciar os bots:"
echo "  ./reiniciar_bots.sh"
echo ""
echo "Os bots vão começar do zero:"
echo "  • Total de trades: 0"
echo "  • P/L acumulado: 0.0000 USDT"
echo ""
echo "═══════════════════════════════════════════════════════════"

