#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bot 3 - Grid Trading com Range -3% / +3%
Estratégia: Geometric Grid com range automático
"""

import os
from dotenv import load_dotenv
from bot import NadoFuturesBot
from nado_protocol.utils.math import to_pow_10

# Carregar variáveis de ambiente do arquivo .env.bot3 (ou .env se não existir)
load_dotenv('.env.bot3')  # Tenta carregar .env.bot3 primeiro
load_dotenv('.env')  # Fallback para .env padrão

def main():
    """Bot 3 - Grid Trading com Range -3% / +3%"""
    try:
        network = os.getenv('NADO_NETWORK', 'mainnet')
        
        # Configuração baseada na imagem fornecida
        config = {
            'subaccount_name': "default",
            'leverage': 40,  # Alavancagem de 40x
            'products': {
                2: {'name': 'BTC/USDT0'},      # BTC-PERP (product_id 2) - ✅ Perpétuo
                3: {'name': 'WETH/USDT0'},     # WETH/USDT0 (product_id 3) - ✅ Spot
                4: {'name': 'ETH/USDT0'},      # ETH-PERP (product_id 4) - ✅ Perpétuo
            },
            'grid_range_lower': -3.0,  # -3% do preço de mercado
            'grid_range_upper': 3.0,   # +3% do preço de mercado
            'grid_levels': 3,  # Número de níveis de grid (ajustado para max 3 ordens ativas)
            'grid_kind': 'geometric',  # Geometric grid
            'quantity_per_order_usdc': 200,  # 200 USDC por ordem
            # Modo agressivo - DESATIVADO (modo padrão)
            'aggressive_mode': False,  # Modo padrão ativo
            'aggressive_grid_spacing': 0.03,  # Grid mais apertado no modo agressivo
            'aggressive_max_orders': 8,  # Mais ordens no modo agressivo
            'aggressive_grid_levels': 5,  # Mais níveis no modo agressivo
            'aggressive_quantity_usdc': 150,  # Quantidade menor no modo agressivo para evitar account health
            'max_open_orders_per_product': 3,  # Max active orders: 3
            'stop_loss_pct': 0.01,  # 1% (Close Position on Loss: 1)
            'take_profit_pct': 0.01,  # 1% (Close Position on Profit: 1)
            'min_balance': 100,
            'order_expiration': 3600,
            'grid_spacing': 0.05,  # Não usado quando tem range, mas necessário para compatibilidade
        }
        
        # Criar bot com estratégia de Grid Trading
        bot = NadoFuturesBot(
            network=network,
            private_key=os.getenv('PRIVATE_KEY_BOT3') or os.getenv('PRIVATE_KEY'),
            bot_name="Bot3",
            config=config
        )
        
        bot.run()
        
    except Exception as e:
        print(f"Erro fatal no Bot3: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    main()

