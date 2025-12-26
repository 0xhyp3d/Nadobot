#!/bin/bash
# Script para reiniciar todos os bots

echo "🔄 Reiniciando todos os bots..."
echo ""

# Parar todos os bots
echo "1️⃣  Parando bots ativos..."
./stop_bots.sh

# Aguardar alguns segundos para garantir que os processos foram finalizados
echo ""
echo "⏳ Aguardando 3 segundos..."
sleep 3

# Iniciar todos os bots novamente
echo ""
echo "2️⃣  Iniciando bots novamente..."
./start_all_bots.sh

echo ""
echo "✅ Reinicialização concluída!"
echo ""
echo "📊 Verificar status dos bots: ./check_bots.sh"
echo "📝 Ver logs: tail -f logs/bot*.log"
