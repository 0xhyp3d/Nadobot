#!/bin/bash
# Script para reiniciar apenas o Bot4

echo "🔄 Reiniciando Bot4..."
echo ""

# Parar Bot4
echo "1️⃣  Parando Bot4..."
pkill -f "python3 bot4.py" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ Bot4 parado"
else
    echo "⚠️  Bot4 não estava rodando ou já estava parado"
fi

# Aguardar alguns segundos
echo ""
echo "⏳ Aguardando 3 segundos..."
sleep 3

# Criar diretório de logs se não existir
mkdir -p logs

# Iniciar Bot4 novamente
echo ""
echo "2️⃣  Iniciando Bot4 novamente..."
nohup python3 bot4.py > logs/bot4.log 2>&1 &
BOT4_PID=$!

if [ $? -eq 0 ]; then
    echo "✅ Bot4 iniciado (PID: $BOT4_PID)"
    echo ""
    echo "📝 Logs: tail -f logs/bot4.log"
    echo ""
    echo "Aguardando 3 segundos para verificar inicialização..."
    sleep 3
    echo ""
    echo "📊 Últimas linhas do log:"
    tail -10 logs/bot4.log
else
    echo "❌ Erro ao iniciar Bot4"
    echo "Verifique os logs: cat logs/bot4.log"
fi





