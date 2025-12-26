#!/bin/bash
# Script para verificar erros nos logs de todos os bots

echo "=========================================="
echo "🔍 VERIFICANDO ERROS NOS LOGS DOS BOTS"
echo "=========================================="
echo ""

# Cores para output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Função para verificar erros em um log
check_errors() {
    local bot_name=$1
    local log_file=$2
    
    if [ ! -f "$log_file" ]; then
        echo -e "${YELLOW}⚠️  $bot_name: Arquivo de log não encontrado${NC}"
        return
    fi
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📋 $bot_name"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # Contar diferentes tipos de erros
    error_count=$(grep -i "error\|erro\|exception\|failed\|fail" "$log_file" 2>/dev/null | wc -l | tr -d ' ')
    cloudflare_count=$(grep -i "cloudflare\|just a moment" "$log_file" 2>/dev/null | wc -l | tr -d ' ')
    warning_count=$(grep -i "warning\|aviso" "$log_file" 2>/dev/null | wc -l | tr -d ' ')
    
    if [ "$error_count" -gt 0 ] || [ "$cloudflare_count" -gt 0 ]; then
        echo -e "${RED}❌ Encontrados $error_count erros e $cloudflare_count bloqueios Cloudflare${NC}"
        
        # Mostrar últimos erros
        echo ""
        echo "📌 Últimos erros encontrados:"
        grep -i "error\|erro\|exception\|failed\|fail" "$log_file" 2>/dev/null | tail -5 | sed 's/^/   /'
        
        if [ "$cloudflare_count" -gt 0 ]; then
            echo ""
            echo "🌐 Últimos bloqueios Cloudflare:"
            grep -i "cloudflare\|just a moment" "$log_file" 2>/dev/null | tail -3 | sed 's/^/   /'
        fi
    else
        echo -e "${GREEN}✅ Nenhum erro encontrado${NC}"
    fi
    
    if [ "$warning_count" -gt 0 ]; then
        echo -e "${YELLOW}⚠️  Encontrados $warning_count avisos${NC}"
    fi
    
    echo ""
}

# Verificar cada bot
check_errors "Bot1" "logs/bot1.log"
check_errors "Bot2" "logs/bot2.log"
check_errors "Bot3" "logs/bot3.log"
check_errors "Bot4" "logs/bot4.log"

echo "=========================================="
echo "✅ Verificação concluída!"
echo ""
echo "💡 Dicas:"
echo "   - Para ver logs em tempo real: ./watch_bot1.sh (ou bot2, bot3, bot4)"
echo "   - Para ver últimas 50 linhas: tail -50 logs/bot1.log"
echo "   - Para buscar um erro específico: grep 'erro' logs/bot1.log"
echo "=========================================="




