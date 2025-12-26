#!/bin/bash
# Script para verificar se há histórico completo nos logs

echo "=== Verificando histórico completo dos bots ==="
echo ""

for bot in bot1 bot2 bot3; do
    echo "📊 Analisando $bot:"
    
    # Verificar tamanho do arquivo
    if [ -f "logs/${bot}.log" ]; then
        size=$(stat -f%z "logs/${bot}.log" 2>/dev/null || stat -c%s "logs/${bot}.log" 2>/dev/null)
        echo "   Tamanho: $size bytes"
        
        # Verificar primeira linha
        first_line=$(head -1 "logs/${bot}.log" 2>/dev/null)
        echo "   Primeira linha: $first_line"
        
        # Verificar última linha
        last_line=$(tail -1 "logs/${bot}.log" 2>/dev/null)
        echo "   Última linha: ${last_line:0:100}..."
        
        # Contar linhas
        lines=$(wc -l < "logs/${bot}.log" 2>/dev/null)
        echo "   Total de linhas: $lines"
        
        # Verificar se há trades
        trades_count=$(grep -c "P/L líquido\|P/L DETALHADO" "logs/${bot}.log" 2>/dev/null || echo "0")
        echo "   Trades encontrados: $trades_count"
    else
        echo "   ❌ Arquivo não encontrado"
    fi
    echo ""
done

echo "=== Executando análise Python ==="
python3 calcular_resultado_total.py





