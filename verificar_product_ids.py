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
            
            # Buscar especificamente por BTC, ETH e WETH
            target_symbols = ['BTC', 'ETH', 'WETH']
            
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
            eth_perp = None
            weth = None
            
            for sym in symbols:
                symbol = sym.get('symbol', '')
                if 'BTC-PERP' in symbol or (symbol == 'BTC' and 'PERP' not in symbol):
                    btc_perp = sym.get('product_id')
                if 'ETH-PERP' in symbol:
                    eth_perp = sym.get('product_id')
                if 'WETH' in symbol and 'PERP' not in symbol:
                    weth = sym.get('product_id')
            
            print("\nProduct IDs recomendados:")
            if btc_perp is not None:
                print(f"  BTC/USDT0 Perp: {btc_perp}")
            if eth_perp is not None:
                print(f"  ETH/USDT0 Perp: {eth_perp}")
            if weth is not None:
                print(f"  WETH/USDT0: {weth}")
            
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





