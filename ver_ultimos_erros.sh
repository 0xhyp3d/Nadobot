#!/bin/bash
# Script para ver as últimas linhas com erros de todos os bots

echo "=========================================="
echo "🔍 ÚLTIMOS ERROS NOS LOGS"
echo "=========================================="
echo ""

# Cores
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

for bot in 1 2 3 4; do
    log_file="logs/bot${bot}.log"
    
    if [ ! -f "$log_file" ]; then
        continue
    fi
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📋 Bot${bot} - Últimas linhas com ERRO/EXCEPTION/FAILED:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # Buscar últimas linhas com erro (últimas 10)
    errors=$(grep -i "error\|erro\|exception\|failed\|fail" "$log_file" 2>/dev/null | tail -10)
    
    if [ -z "$errors" ]; then
        echo -e "${YELLOW}✅ Nenhum erro encontrado nas últimas entradas${NC}"
    else
        echo -e "${RED}$errors${NC}"
    fi
    
    echo ""
done

echo "=========================================="




