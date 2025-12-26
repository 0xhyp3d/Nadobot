#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bot 2 - Estratégia Customizável
Configure os parâmetros abaixo para testar diferentes estratégias
"""

import os
from dotenv import load_dotenv
from bot import NadoFuturesBot
from nado_protocol.utils.math import to_pow_10

# Carregar variáveis de ambiente do arquivo .env.bot2 (ou .env se não existir)
load_dotenv('.env.bot2')  # Tenta carregar .env.bot2 primeiro
load_dotenv('.env')  # Fallback para .env padrão

def main():
    """Bot 2 - Estratégia Customizável"""
    try:
        network = os.getenv('NADO_NETWORK', 'mainnet')
        
        # ============================================
        # CONFIGURE AQUI OS PARÂMETROS DA ESTRATÉGIA 2
        # ============================================
        config = {
            'subaccount_name': "bot2",  # Subconta específica para Bot2 (altere conforme necessário)
            'leverage': 40,  # Alavancagem (ajuste conforme necessário)
            'products': {
                2: {'name': 'BTC/USDT0'},   # BTC-PERP (product_id 2) - Perpétuo
                4: {'name': 'ETH/USDT0'},   # ETH-PERP (product_id 4) - Perpétuo
                3: {'name': 'WETH/USDT0'},  # WETH/USDT0 (product_id 3) - Spot
            },
            'quantity_per_order_usdc': 200,  # 200 USDC por ordem
            'grid_spacing': 0.10,  # 0.10% entre grids (MAIOR spread = menos trades, maior lucro por trade)
            'max_open_orders_per_product': 10,  # Mais ordens abertas simultaneamente
            'stop_loss_pct': 0.01,  # Stop Loss de 1% (MAIS RESTRITIVO)
            'take_profit_pct': 0.03,  # Take Profit de 3% (R:R 3:1)
            'min_balance': 100,
            'grid_levels': 5,  # Mais níveis de grid
            'order_expiration': 3600,
        }
        
        # Criar bot com estratégia customizada
        bot = NadoFuturesBot(
            network=network,
            private_key=os.getenv('PRIVATE_KEY_BOT2') or os.getenv('PRIVATE_KEY'),
            bot_name="Bot2",
            config=config
        )
        
        bot.run()
        
    except Exception as e:
        print(f"Erro fatal no Bot2: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    main()



