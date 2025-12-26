#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar os product_ids corretos na API da Nado
"""

import requests
import json

def main():
    """Consultar API da Nado para obter símbolos e product_ids"""
    try:
        print("Consultando API da Nado para obter símbolos...")
        print("URL: https://gateway.prod.nado.xyz/v1/symbols\n")
        
        response = requests.get('https://gateway.prod.nado.xyz/v1/symbols', timeout=10)
        
        if response.status_code == 200:
            symbols = response.json()
            
            print("=" * 60)
            print("SÍMBOLOS DISPONÍVEIS NA NADO PROTOCOL")
            print("=" * 60)
            
            # Buscar especificamente por BTC, FARTCoin e ZEC
            target_symbols = ['BTC', 'FART', 'ZEC', 'ETH', 'WETH']
            
            print("\n📊 Produtos relevantes encontrados:")
            print("-" * 60)
            
            for sym in sorted(symbols, key=lambda x: x.get('product_id', 0)):
                symbol_name = sym.get('symbol', '')
                product_id = sym.get('product_id')
                delisted = sym.get('delisted', False)
                
                # Mostrar todos, mas destacar os relevantes
                if any(target in symbol_name for target in target_symbols):
                    status = "❌ DELISTED" if delisted else "✅ ATIVO"
                    print(f"Product ID: {product_id:2d} | Symbol: {symbol_name:20s} | {status}")
            
            print("\n" + "=" * 60)
            print("TODOS OS SÍMBOLOS:")
            print("=" * 60)
            
            for sym in sorted(symbols, key=lambda x: x.get('product_id', 0)):
                symbol_name = sym.get('symbol', '')
                product_id = sym.get('product_id')
                delisted = sym.get('delisted', False)
                status = "(DELISTED)" if delisted else ""
                print(f"Product ID: {product_id:2d} | Symbol: {symbol_name:20s} {status}")
            
            print("\n" + "=" * 60)
            print("RECOMENDAÇÃO:")
            print("=" * 60)
            
            # Identificar product_ids recomendados
            btc_perp = None
            fart_perp = None
            zec_perp = None
            
            for sym in symbols:
                symbol = sym.get('symbol', '')
                if 'BTC-PERP' in symbol or (symbol == 'BTC' and 'PERP' not in symbol):
                    btc_perp = sym.get('product_id')
                if 'FARTCOIN-PERP' in symbol or 'FART-PERP' in symbol:
                    fart_perp = sym.get('product_id')
                if 'ZEC-PERP' in symbol:
                    zec_perp = sym.get('product_id')
            
            print("\nProduct IDs recomendados:")
            if btc_perp is not None:
                print(f"  BTC/USDT0 Perp: {btc_perp}")
            if fart_perp is not None:
                print(f"  FARTCoin/USDT0 Perp: {fart_perp}")
            if zec_perp is not None:
                print(f"  ZEC/USDT0 Perp: {zec_perp}")
            
        else:
            print(f"❌ Erro ao consultar API: Status {response.status_code}")
            print(f"Resposta: {response.text[:500]}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro de conexão: {e}")
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()





