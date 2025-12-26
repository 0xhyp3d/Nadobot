#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para calcular o resultado total (lucro/prejuízo) de cada bot
desde que foram criados, analisando todos os logs históricos.
"""

import re
import os
import json
from decimal import Decimal
from datetime import datetime
from collections import defaultdict

def extrair_pl_detalhado(log_file):
    """
    Extrai informações de P/L detalhado de um arquivo de log.
    Retorna uma lista de dicionários com informações de cada trade.
    """
    trades = []
    
    if not os.path.exists(log_file):
        return trades
    
    with open(log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Padrão 1: P/L DETALHADO: [P/L DETALHADO] Lucro bruto: X.XXXX USDT | Taxas: Y.YYYY USDT | Lucro líquido: Z.ZZZZ USDT
    pattern1 = r'\[P/L DETALHADO\].*?Lucro líquido:\s+([-\d.]+)\s+USDT'
    matches1 = re.finditer(pattern1, content)
    
    for match in matches1:
        lucro_liquido = float(match.group(1))
        
        # Tentar encontrar a data/hora próxima (até 200 caracteres antes)
        context_start = max(0, match.start() - 200)
        context = content[context_start:match.start()]
        
        # Buscar data/hora no formato [YYYY-MM-DD HH:MM:SS]
        date_pattern = r'\[(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\]'
        date_match = re.search(date_pattern, context)
        timestamp = date_match.group(1) if date_match else "Data não encontrada"
        
        trades.append({
            'timestamp': timestamp,
            'lucro_liquido': lucro_liquido,
            'fonte': 'P/L DETALHADO'
        })
    
    # Padrão 2: log_trade com P/L líquido: ... | P/L líquido: X.XXXX USDT | Total acumulado: Y.YYYY USDT
    # Este padrão aparece quando uma ordem é fechada com lucro
    pattern2 = r'P/L líquido:\s+([-\d.]+)\s+USDT\s+\|\s+Total acumulado:\s+([-\d.]+)\s+USDT'
    matches2 = re.finditer(pattern2, content)
    
    for match in matches2:
        lucro_liquido = float(match.group(1))
        
        # Evitar duplicatas (se já foi capturado pelo padrão 1)
        # Verificar se já existe um trade próximo com o mesmo valor
        context_start = max(0, match.start() - 200)
        context_end = min(len(content), match.end() + 50)
        context = content[context_start:context_end]
        
        # Verificar se já foi capturado
        ja_existe = False
        for trade_existente in trades:
            if abs(trade_existente['lucro_liquido'] - lucro_liquido) < 0.0001:
                # Verificar se o timestamp está próximo (mesmo trade)
                if trade_existente['timestamp'] in context or "Data não encontrada" in context:
                    ja_existe = True
                    break
        
        if not ja_existe:
            # Buscar data/hora
            date_pattern = r'\[(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\]'
            date_match = re.search(date_pattern, context)
            timestamp = date_match.group(1) if date_match else "Data não encontrada"
            
            trades.append({
                'timestamp': timestamp,
                'lucro_liquido': lucro_liquido,
                'fonte': 'log_trade'
            })
    
    return trades

def extrair_total_acumulado(log_file):
    """
    Extrai o último total acumulado registrado no log.
    Útil para verificar o estado mais recente.
    """
    if not os.path.exists(log_file):
        return None, 0
    
    with open(log_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Procurar o último registro de "Lucro/Prejuízo acumulado"
    pattern = r'Lucro/Prejuízo acumulado \(líquido, após taxas\):\s+([-\d.]+)\s+USDT.*?Total de trades:\s+(\d+)'
    
    last_match = None
    for line in reversed(lines):
        match = re.search(pattern, line)
        if match:
            last_match = match
            break
    
    if last_match:
        total_usdt = float(last_match.group(1))
        total_trades = int(last_match.group(2))
        
        # Tentar encontrar a data/hora dessa linha
        date_pattern = r'\[(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\]'
        date_match = re.search(date_pattern, line)
        timestamp = date_match.group(1) if date_match else "Data não encontrada"
        
        return timestamp, total_usdt, total_trades
    
    return "Data não encontrada", 0, 0

def calcular_resultado_bot(bot_name):
    """Calcula o resultado total de um bot específico a partir dos logs (fallback)"""
    log_file = f"logs/{bot_name}.log"
    
    print(f"\n{'='*60}")
    print(f"Analisando logs de: {bot_name}")
    print(f"{'='*60}")
    print("⚠️  Nota: Esta análise usa apenas os logs. Para resultados mais precisos,")
    print("    use os arquivos de histórico JSON (logs/{bot_name}_history.json)")
    
    # Extrair todos os trades com P/L detalhado
    trades = extrair_pl_detalhado(log_file)
    
    # Calcular soma total
    total_historico = sum(t['lucro_liquido'] for t in trades)
    
    # Extrair último estado acumulado
    try:
        ultima_data, ultimo_acumulado, total_trades = extrair_total_acumulado(log_file)
    except (ValueError, TypeError):
        ultima_data = "Data não encontrada"
        ultimo_acumulado = 0
        total_trades = 0
    
    print(f"📊 Total de trades realizados (desde ontem): {len(trades)}")
    
    if len(trades) > 0:
        print(f"💰 Lucro/Prejuízo total HISTÓRICO (soma de todos os trades): {total_historico:.4f} USDT")
        print(f"📅 Primeiro trade: {trades[0]['timestamp']}")
        print(f"📅 Último trade: {trades[-1]['timestamp']}")
        
        # Mostrar os últimos 5 trades
        if len(trades) > 5:
            print(f"\n📈 Últimos 5 trades:")
            for trade in trades[-5:]:
                sinal = "+" if trade['lucro_liquido'] >= 0 else ""
                print(f"   {trade['timestamp']}: {sinal}{trade['lucro_liquido']:.4f} USDT")
    else:
        print(f"⚠️  Nenhum trade realizado ainda")
    
    if ultimo_acumulado != 0 or total_trades > 0:
        print(f"\n🔄 Último estado registrado no log:")
        print(f"   Data: {ultima_data}")
        print(f"   Total acumulado: {ultimo_acumulado:.4f} USDT")
        print(f"   Total de trades: {total_trades}")
    
    # Comparar com o histórico
    if len(trades) > 0 and abs(total_historico - ultimo_acumulado) > 0.0001:
        print(f"\n⚠️  AVISO: Diferença entre histórico ({total_historico:.4f}) e último acumulado ({ultimo_acumulado:.4f})")
        print(f"   Isso pode indicar que o bot foi reiniciado e o acumulado foi resetado.")
        print(f"   O valor HISTÓRICO ({total_historico:.4f} USDT) é o correto desde o início.")
    
    return {
        'bot_name': bot_name,
        'total_trades': len(trades),
        'total_historico': total_historico,
        'ultimo_acumulado': ultimo_acumulado,
        'ultima_data': ultima_data,
        'trades': trades
    }

def calcular_resultado_bot_json(bot_name):
    """Calcula o resultado total de um bot usando o arquivo JSON de histórico"""
    history_file = f"logs/{bot_name}_history.json"
    
    if not os.path.exists(history_file):
        return None
    
    try:
        with open(history_file, 'r', encoding='utf-8') as f:
            history = json.load(f)
        
        trades = history.get('trades', [])
        total_profit = history.get('total_profit', sum(t.get('net_profit', 0) for t in trades))
        
        return {
            'bot_name': bot_name,
            'total_trades': len(trades),
            'total_historico': total_profit,
            'trades': trades,
            'created_at': history.get('created_at'),
            'last_updated': history.get('last_updated')
        }
    except Exception as e:
        print(f"Erro ao ler histórico JSON de {bot_name}: {e}")
        return None

def main():
    """Função principal"""
    print("="*60)
    print("ANÁLISE DE RESULTADOS - TODOS OS BOTS")
    print("Calculando lucro/prejuízo total desde o início")
    print("="*60)
    
    bots = ['bot1', 'bot2', 'bot3', 'bot4']
    resultados = {}
    
    # Primeiro tentar usar arquivos JSON de histórico (mais confiável)
    print("\n📁 Verificando arquivos de histórico JSON...")
    for bot in bots:
        resultado_json = calcular_resultado_bot_json(bot)
        if resultado_json:
            resultados[bot] = resultado_json
            print(f"✅ {bot}: {resultado_json['total_trades']} trades, {resultado_json['total_historico']:.4f} USDT")
        else:
            print(f"⚠️  {bot}: Sem arquivo de histórico JSON, usando análise de logs...")
            resultados[bot] = calcular_resultado_bot(bot)
    
    # Resumo comparativo
    print(f"\n{'='*60}")
    print("RESUMO COMPARATIVO")
    print(f"{'='*60}")
    print(f"{'Bot':<10} {'Trades':<10} {'Total Histórico (USDT)':<30} {'Criado em':<20}")
    print("-"*80)
    
    for bot in bots:
        res = resultados[bot]
        total_hist = res.get('total_historico', res.get('ultimo_acumulado', 0))
        created_at = res.get('created_at', res.get('ultima_data', 'N/A'))
        
        # Formatar data
        if created_at and created_at != 'N/A' and 'T' in str(created_at):
            try:
                dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                created_at = dt.strftime('%Y-%m-%d %H:%M')
            except:
                pass
        
        sinal = "+" if total_hist >= 0 else ""
        print(f"{bot:<10} {res['total_trades']:<10} {sinal}{total_hist:>28.4f} {str(created_at):<20}")
    
    # Bot mais rentável
    print(f"\n{'='*60}")
    print("🏆 RANKING DE RENTABILIDADE")
    print(f"{'='*60}")
    
    bots_ordenados = sorted(resultados.items(), 
                          key=lambda x: x[1].get('total_historico', x[1].get('ultimo_acumulado', 0)),
                          reverse=True)
    
    for i, (bot, res) in enumerate(bots_ordenados, 1):
        valor = res.get('total_historico', res.get('ultimo_acumulado', 0))
        sinal = "+" if valor >= 0 else ""
        emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
        print(f"{emoji} {i}º lugar: {bot} = {sinal}{valor:.4f} USDT ({res['total_trades']} trades)")

if __name__ == "__main__":
    main()

