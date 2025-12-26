#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de diagnóstico para verificar product_ids e preços
"""

import os
from dotenv import load_dotenv
from nado_protocol.client import create_nado_client
from nado_protocol.utils.math import from_x18

load_dotenv()

def main():
    """Diagnosticar product_ids e seus preços"""
    network = os.getenv('NADO_NETWORK', 'mainnet')
    private_key = os.getenv('PRIVATE_KEY')
    
    if not private_key:
        print("ERRO: PRIVATE_KEY não encontrada no .env")
        return
    
    try:
        client = create_nado_client(network, private_key)
        
        # Product IDs para testar
        product_ids_to_test = [2, 3, 4, 18, 22]
        
        print("=" * 60)
        print("DIAGNÓSTICO DE PRODUCT IDs E PREÇOS")
        print("=" * 60)
        print()
        
        for product_id in product_ids_to_test:
            try:
                price_response = client.market.get_latest_market_price(product_id)
                
                if hasattr(price_response, 'bid_x18') and hasattr(price_response, 'ask_x18'):
                    bid = float(from_x18(price_response.bid_x18))
                    ask = float(from_x18(price_response.ask_x18))
                    mid = (bid + ask) / 2.0
                    
                    print(f"Product ID {product_id:2d}:")
                    print(f"  Bid:  {bid:.6f}")
                    print(f"  Ask:  {ask:.6f}")
                    print(f"  Mid:  {mid:.6f}")
                    
                    # Tentar identificar qual ativo é baseado no preço
                    if 80000 < mid < 90000:
                        print(f"  ⚠️  Pode ser BTC (esperado: ~87000)")
                    elif 400 < mid < 500:
                        print(f"  ⚠️  Pode ser ZEC (esperado: ~438)")
                    elif 0.2 < mid < 0.3:
                        print(f"  ⚠️  Pode ser FARTCoin (esperado: ~0.29)")
                    elif 2900 < mid < 3000:
                        print(f"  ⚠️  Preço ~{mid:.2f} - NÃO IDENTIFICADO (pode ser produto incorreto)")
                    print()
            except Exception as e:
                print(f"Product ID {product_id:2d}: ERRO - {e}")
                print()
        
        print("=" * 60)
        print("CONCLUSÃO:")
        print("  - BTC/USDT0 deveria ter product_id com preço ~87000")
        print("  - ZEC/USDT0 deveria ter product_id com preço ~438")
        print("  - FARTCoin/USDT0 deveria ter product_id com preço ~0.29")
        print("=" * 60)
        
    except Exception as e:
        print(f"ERRO ao criar cliente: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()




