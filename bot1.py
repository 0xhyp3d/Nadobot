#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bot 1 - Estratégia Original
Grid Trading / Market Making com parâmetros padrão
"""

import os
from dotenv import load_dotenv
from bot import NadoFuturesBot
from nado_protocol.utils.math import to_pow_10

# Carregar variáveis de ambiente do arquivo .env.bot1 (ou .env se não existir)
load_dotenv('.env.bot1')  # Tenta carregar .env.bot1 primeiro
load_dotenv('.env')  # Fallback para .env padrão

def main():
    """Bot 1 - Estratégia Original"""
    try:
        network = os.getenv('NADO_NETWORK', 'mainnet')
        
        # Configuração da estratégia original
        config = {
            'subaccount_name': "bot1",  # Subconta específica para Bot1 (altere conforme necessário)
            'leverage': 40,  # Alavancagem de 40x
            'products': {
                2: {'name': 'BTC/USDT0'},   # BTC-PERP (product_id 2) - Perpétuo
                4: {'name': 'ETH/USDT0'},   # ETH-PERP (product_id 4) - Perpétuo
                3: {'name': 'WETH/USDT0'},  # WETH/USDT0 (product_id 3) - Spot
            },
            'quantity_per_order_usdc': 200,  # 200 USDC por ordem
            'grid_spacing': 0.05,  # 0.05% entre grids
            'max_open_orders_per_product': 5,
            'stop_loss_pct': 0.02,  # Stop Loss de 2%
            'take_profit_pct': 0.04,  # Take Profit de 4% (R:R 2:1)
            'min_balance': 100,
            'grid_levels': 3,
            'order_expiration': 3600,
        }
        
        # Criar bot com estratégia original
        bot = NadoFuturesBot(
            network=network,
            private_key=os.getenv('PRIVATE_KEY_BOT1') or os.getenv('PRIVATE_KEY'),
            bot_name="Bot1",
            config=config
        )
        
        bot.run()
        
    except Exception as e:
        print(f"Erro fatal no Bot1: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    main()



