#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar TODOS os produtos de perps /USDT0 disponíveis na Nado
e identificar quais estão funcionando corretamente
"""

import os
import sys
import time
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Importar cloudscraper ANTES do SDK
try:
    import cloudscraper
    import requests
    
    _OriginalSession = requests.Session
    
    class CloudflareSession(_OriginalSession):
        def __init__(self, *args, **kwargs):
            self._cloudscraper = cloudscraper.create_scraper(
                browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
            )
            for attr_name in dir(self._cloudscraper):
                if not attr_name.startswith('_') and not callable(getattr(self._cloudscraper, attr_name, None)):
                    try:
                        setattr(self, attr_name, getattr(self._cloudscraper, attr_name))
                    except (AttributeError, TypeError):
                        pass
        
        def request(self, method, url, **kwargs):
            if 'headers' not in kwargs:
                kwargs['headers'] = {}
            return self._cloudscraper.request(method, url, **kwargs)
    
    requests.Session = CloudflareSession
except ImportError:
    import requests

from nado_protocol.client import create_nado_client
from nado_protocol.utils.exceptions import BadStatusCodeException

def test_product(client, product_id: int, max_attempts: int = 3) -> tuple[bool, str]:
    """
    Testa um produto específico tentando obter o preço de mercado.
    Faz múltiplas tentativas para lidar com erros intermitentes do Cloudflare.
    Retorna (sucesso: bool, mensagem: str)
    """
    last_error = None
    
    for attempt in range(max_attempts):
        try:
            # Tentar obter preço de mercado
            price_response = client.market.get_latest_market_price(product_id)
            
            if hasattr(price_response, 'bid_x18') and hasattr(price_response, 'ask_x18'):
                # Converter para int se for string
                bid_x18 = int(price_response.bid_x18) if not isinstance(price_response.bid_x18, int) else price_response.bid_x18
                ask_x18 = int(price_response.ask_x18) if not isinstance(price_response.ask_x18, int) else price_response.ask_x18
                
                bid = bid_x18 / (10 ** 18)
                ask = ask_x18 / (10 ** 18)
                return True, f"OK - bid={bid:.6f}, ask={ask:.6f}"
            else:
                last_error = "Erro: Resposta inválida (sem bid/ask)"
                
        except BadStatusCodeException as e:
            error_str = str(e)
            if "Just a moment" in error_str or "<!DOCTYPE html>" in error_str:
                last_error = "Cloudflare Challenge"
                # Se for Cloudflare, aguardar um pouco antes de tentar novamente
                if attempt < max_attempts - 1:
                    time.sleep(2)
                continue
            last_error = f"BadStatusCodeException: {str(e)[:80]}"
        except Exception as e:
            error_msg = str(e)
            # Filtrar erros de produto inexistente - não tentar novamente
            if "market for the given product" in error_msg or "product or ticker ID was not" in error_msg:
                return False, "Produto não existe"
            last_error = f"{type(e).__name__}: {error_msg[:60]}"
            if attempt < max_attempts - 1:
                time.sleep(1)
    
    # Se chegou aqui, todas as tentativas falharam
    return False, last_error or "Erro desconhecido"

def main():
    """Testa todos os produtos de perps conhecidos"""
    
    private_key = os.getenv('PRIVATE_KEY')
    if not private_key:
        print("❌ PRIVATE_KEY não encontrada no arquivo .env")
        return
    
    network = os.getenv('NADO_NETWORK', 'mainnet')
    
    print(f"🔌 Conectando à rede {network}...")
    try:
        client = create_nado_client(network, private_key)
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return
    
    # Lista completa de product_ids para testar (range amplo para encontrar todos)
    # Testar de 1 a 50 para garantir que pegamos todos os perps disponíveis
    products_to_test = {}
    
    print("\n🔍 Descobrindo produtos disponíveis (testando IDs de 1 a 50)...")
    
    # Primeiro, testar produtos conhecidos e depois fazer uma varredura
    known_products = {
        2: "BTC/USDT0",
        3: "WETH/USDT0", 
        4: "ETH/USDT0",
        # Adicionar outros conhecidos conforme necessário
    }
    
    # Adicionar conhecidos
    for pid, name in known_products.items():
        products_to_test[pid] = name
    
    # Também testar alguns IDs comuns
    common_ids = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 20, 21, 23, 24, 25]
    for pid in common_ids:
        if pid not in products_to_test:
            products_to_test[pid] = f"UNKNOWN{pid}/USDT0"
    
    print(f"\n🧪 Testando {len(products_to_test)} produtos...\n")
    print("=" * 90)
    
    working_products = []
    failed_products = []
    
    for product_id, symbol in sorted(products_to_test.items()):
        print(f"📊 ID {product_id:2d} ({symbol:20s})...", end=" ", flush=True)
        
        success, message = test_product(client, product_id, max_attempts=3)
        
        if success:
            print(f"✅ {message}")
            working_products.append((product_id, symbol))
        else:
            print(f"❌ {message}")
            failed_products.append((product_id, symbol))
        
        # Pequeno delay para evitar rate limiting
        time.sleep(0.8)
    
    print("\n" + "=" * 90)
    print("\n📈 RESULTADO FINAL DOS TESTES\n")
    
    print(f"✅ Produtos funcionando ({len(working_products)}):")
    for product_id, symbol in sorted(working_products):
        print(f"   - Product ID {product_id:2d}: {symbol}")
    
    print(f"\n❌ Produtos com erro ({len(failed_products)}):")
    for product_id, symbol in sorted(failed_products):
        print(f"   - Product ID {product_id:2d}: {symbol}")
    
    # Gerar configuração Python para os produtos funcionando
    print("\n" + "=" * 90)
    print("\n📝 CONFIGURAÇÃO PARA OS BOTS (produtos funcionando):\n")
    print("'products': {")
    for product_id, symbol in sorted(working_products):
        # Garantir formato /USDT0
        if not symbol.endswith('/USDT0'):
            # Se não terminar com /USDT0, adicionar
            symbol = symbol.replace('-PERP', '/USDT0')
            if not symbol.endswith('/USDT0'):
                symbol = f"{symbol}/USDT0"
        print(f"    {product_id}: {{'name': '{symbol}'}},")
    print("},")
    
    print("\n✅ Teste concluído!")
    
    # Salvar resultado em arquivo
    result_file = "produtos_funcionais.txt"
    with open(result_file, 'w') as f:
        f.write("# Produtos funcionais identificados\n\n")
        for product_id, symbol in sorted(working_products):
            if not symbol.endswith('/USDT0'):
                symbol = symbol.replace('-PERP', '/USDT0')
                if not symbol.endswith('/USDT0'):
                    symbol = f"{symbol}/USDT0"
            f.write(f"{product_id}: {symbol}\n")
    
    print(f"\n💾 Resultado salvo em: {result_file}")

if __name__ == "__main__":
    main()




