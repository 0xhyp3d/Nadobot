#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bot de Trading de Futuros para Nado
Estratégia: Grid Trading / Scalping com Market Making
Usando SDK oficial da Nado Protocol
"""

# CRÍTICO: Configurar cloudscraper ANTES de qualquer outro import
# Isso garante que o monkey patch seja aplicado antes do SDK da Nado criar suas sessões HTTP
try:
    import cloudscraper
    import requests
    CLOUDSCRAPER_AVAILABLE = True
    
    # User-Agent do Chrome (mais comum)
    CHROME_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    
    # Salvar referência à classe original do Session ANTES de substituir
    _OriginalSession = requests.Session
    
    # Criar uma classe que substitui requests.Session e usa cloudscraper internamente
    class CloudflareSession(_OriginalSession):
        """
        Session que usa cloudscraper para contornar desafios do Cloudflare.
        É compatível com requests.Session mas resolve automaticamente os desafios JavaScript.
        """
        def __init__(self, *args, **kwargs):
            # Criar sessão cloudscraper que é compatível com requests.Session
            # Configurações otimizadas para melhor compatibilidade com Cloudflare
            self._cloudscraper = cloudscraper.create_scraper(
                browser={
                    'browser': 'chrome',
                    'platform': 'windows',
                    'desktop': True
                },
                delay=10,  # Delay entre requisições (milissegundos)
                debug=False
            )
            # Copiar todos os atributos do cloudscraper para este objeto
            # para manter compatibilidade total com requests.Session
            for attr_name in dir(self._cloudscraper):
                if not attr_name.startswith('_') and not callable(getattr(self._cloudscraper, attr_name, None)):
                    try:
                        setattr(self, attr_name, getattr(self._cloudscraper, attr_name))
                    except (AttributeError, TypeError):
                        pass
        
        def request(self, method, url, **kwargs):
            """Fazer requisição usando cloudscraper com retry e headers melhorados"""
            # Garantir User-Agent se não fornecido
            if 'headers' not in kwargs:
                kwargs['headers'] = {}
            if 'User-Agent' not in kwargs['headers']:
                if hasattr(self, 'headers') and 'User-Agent' in self.headers:
                    kwargs['headers']['User-Agent'] = self.headers['User-Agent']
                else:
                    kwargs['headers']['User-Agent'] = CHROME_USER_AGENT
            
            # Adicionar headers adicionais para melhor compatibilidade com Cloudflare
            kwargs['headers'].update({
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            })
            
            # Tentar fazer requisição com retry (até 2 tentativas adicionais = 3 total)
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    # Usar cloudscraper para fazer a requisição (resolve desafios do Cloudflare automaticamente)
                    response = self._cloudscraper.request(method, url, **kwargs)
                    return response
                except Exception as e:
                    error_str = str(e).lower()
                    # Se for possível erro de Cloudflare e ainda temos tentativas, aguardar e tentar novamente
                    if attempt < max_retries - 1:
                        import time
                        wait_time = (attempt + 1) * 3  # 3s, 6s, 9s
                        time.sleep(wait_time)
                        continue
                    # Se esgotaram tentativas, relançar exceção
                    raise
    
    # Substituir requests.Session pela nossa CloudflareSession
    # Isso deve acontecer ANTES de qualquer código importar requests.Session
    requests.Session = CloudflareSession
    
    import sys
    sys.stderr.write("[CLOUDFLARE] cloudscraper ativado - proteção contra desafios do Cloudflare habilitada\n")
    
except ImportError:
    # Se cloudscraper não estiver instalado, usar requests normal com User-Agent
    import requests
    CLOUDSCRAPER_AVAILABLE = False
    
    # User-Agent do Chrome (mais comum)
    CHROME_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    
    # Monkey patch para adicionar User-Agent padrão a todas as requisições requests
    original_request = requests.Session.request
    def request_with_user_agent(self, method, url, **kwargs):
        if 'headers' not in kwargs:
            kwargs['headers'] = {}
        if 'User-Agent' not in kwargs['headers']:
            kwargs['headers']['User-Agent'] = CHROME_USER_AGENT
        return original_request(self, method, url, **kwargs)
    
    requests.Session.request = request_with_user_agent
    import sys
    sys.stderr.write("[CLOUDFLARE] cloudscraper não disponível - usando requests com User-Agent padrão\n")

# Agora importar outras bibliotecas padrão
import os
import time
import logging
import json
from decimal import Decimal
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Importar SDK da Nado DEPOIS do monkey patch do cloudscraper
from nado_protocol.client import create_nado_client
from nado_protocol.engine_client.types.execute import (
    OrderParams,
    PlaceOrderParams,
    CancelOrdersParams
)
from nado_protocol.utils.bytes32 import subaccount_to_bytes32, subaccount_to_hex
from nado_protocol.utils.expiration import OrderType, get_expiration_timestamp
from nado_protocol.utils.math import to_pow_10, to_x18, from_x18
from nado_protocol.utils.nonce import gen_order_nonce
from nado_protocol.utils.subaccount import SubaccountParams
from nado_protocol.utils.order import build_appendix
from nado_protocol.utils.exceptions import BadStatusCodeException

# Carregar variáveis de ambiente
load_dotenv()

# Configuração de logging será feita por cada bot individualmente
def setup_logger(bot_name: str) -> logging.Logger:
    """Configurar logger para um bot específico"""
    logger = logging.getLogger(bot_name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            f'[%(asctime)s] [{bot_name}] %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

# Logger padrão será substituído por self.logger em cada instância do bot


class NadoFuturesBot:
    """Bot de trading de futuros para Nado com estratégia de Grid Trading"""
    
    def __init__(self, network: str = "mainnet", private_key: Optional[str] = None, 
                 bot_name: str = "Bot", config: Optional[Dict] = None):
        """
        Inicializa o bot de trading
        
        Args:
            network: Rede a usar (mainnet ou devnet)
            private_key: Chave privada (opcional, usa PRIVATE_KEY do .env se não fornecido)
            bot_name: Nome do bot para logs
            config: Dicionário com configurações customizadas (opcional)
        """
        self.bot_name = bot_name
        
        # Credenciais da API
        private_key_raw = private_key or os.getenv('PRIVATE_KEY')
        
        if not private_key_raw:
            raise ValueError(f"PRIVATE_KEY deve estar configurado no arquivo .env ou passado como parâmetro para {self.bot_name}")
        
        # Limpar a chave privada (remover espaços, quebras de linha, etc)
        self.private_key = private_key_raw.strip().replace(' ', '').replace('\n', '').replace('\r', '').replace('\t', '')
        
        # Validar formato básico (deve começar com 0x e ter 66 caracteres)
        if not self.private_key.startswith('0x'):
            raise ValueError("PRIVATE_KEY deve começar com '0x'")
        if len(self.private_key) != 66:
            raise ValueError(
                f"PRIVATE_KEY deve ter 66 caracteres (encontrado: {len(self.private_key)}). "
                f"Certifique-se de que a chave está completa e sem espaços no arquivo .env"
            )
        
        # Validar que todos os caracteres após 0x são hexadecimais
        hex_part = self.private_key[2:]
        if not all(c in '0123456789abcdefABCDEF' for c in hex_part):
            raise ValueError(
                "PRIVATE_KEY contém caracteres inválidos. "
                "A chave deve conter apenas caracteres hexadecimais (0-9, a-f, A-F) após '0x'"
            )
        
        # Inicializar cliente Nado
        # Nota: devnet requer configurações adicionais que podem não estar disponíveis
        # Use mainnet para produção ou configure devnet adequadamente
        try:
            self.client = create_nado_client(network, self.private_key)
            
            # Adicionar User-Agent ao cliente HTTP subjacente se possível
            # Isso ajuda a evitar bloqueios do Cloudflare
            # Nota: self.logger ainda não foi criado, então não logamos aqui
            try:
                # Tentar encontrar e configurar o session HTTP do cliente
                if hasattr(self.client, 'context'):
                    # Verificar se há um cliente HTTP configurável
                    if hasattr(self.client.context, 'engine_client'):
                        engine_client = self.client.context.engine_client
                        # Tentar encontrar session/requests client
                        for attr_name in dir(engine_client):
                            attr = getattr(engine_client, attr_name, None)
                            if hasattr(attr, 'session'):
                                session = getattr(attr, 'session', None)
                                if session and hasattr(session, 'headers'):
                                    session.headers.update({'User-Agent': CHROME_USER_AGENT})
                            elif hasattr(attr, 'headers'):
                                attr.headers.update({'User-Agent': CHROME_USER_AGENT})
            except Exception:
                # Se não conseguir configurar diretamente, o monkey patch do requests já deve funcionar
                pass
        except AssertionError as e:
            if network == "devnet":
                # Usar print() pois logger ainda não foi inicializado
                print("⚠️ devnet não está configurado. Tente usar mainnet ou configure devnet adequadamente.")
                raise ValueError(
                    "devnet requer configurações adicionais (RPC node URL). "
                    "Altere NADO_NETWORK=mainnet no arquivo .env ou configure devnet corretamente."
                )
            raise
        except ValueError as e:
            if "hexadecimal" in str(e).lower() or "hex" in str(e).lower():
                # Usar print() pois logger ainda não foi inicializado
                print("❌ Erro: Chave privada inválida. Verifique o formato no arquivo .env")
                print("A chave deve estar no formato: 0x seguido de 64 caracteres hexadecimais")
                raise ValueError(
                    f"Chave privada inválida: {e}. "
                    "Verifique se o arquivo .env contém apenas a chave sem espaços extras ou caracteres especiais."
                )
            raise
        except Exception as e:
            # Usar print() pois logger ainda não foi inicializado
            print(f"❌ Erro ao criar cliente Nado: {e}")
            raise
        
        self.owner = self.client.context.engine_client.signer.address
        
        # Parâmetros de trading (valores padrão)
        default_config = {
            'subaccount_name': "default",
            'leverage': 40,  # Alavancagem de 40x
            'products': {
                2: {'name': 'BTC/USDT0', 'amount_x18': to_pow_10(0.001, 18)},  # BTC/USDT0 Perp (product_id pode variar)
            },
            'grid_spacing': 0.05,  # 0.05% entre grids
            'max_open_orders_per_product': 5,  # Limite de ordens abertas por produto
            'stop_loss_pct': 0.02,  # Stop Loss de 2%
            'take_profit_pct': 0.04,  # Take Profit de 4% (R:R 2:1)
            'min_balance': 100,  # Saldo mínimo em USDT
            'grid_levels': 3,  # Níveis de grid acima e abaixo do preço
            'order_expiration': 3600,  # Expiração das ordens em segundos (1 hora)
            # Parâmetros para Grid Trading com range
            'grid_range_lower': None,  # Range inferior em % (ex: -3.0 para -3%)
            'grid_range_upper': None,  # Range superior em % (ex: 3.0 para +3%)
            'grid_kind': 'linear',  # 'linear' ou 'geometric'
            'quantity_per_order_usdc': None,  # Quantidade por ordem em USDC (se especificado, usa isso ao invés de amount_x18)
        }
        
        # Mesclar configuração customizada com padrão
        if config:
            default_config.update(config)
        
        # Aplicar configurações
        self.subaccount_name = default_config['subaccount_name']
        self.leverage = default_config['leverage']
        self.products = default_config['products']
        self.grid_spacing = default_config['grid_spacing']
        self.max_open_orders_per_product = default_config['max_open_orders_per_product']
        self.stop_loss_pct = default_config['stop_loss_pct']
        self.take_profit_pct = default_config['take_profit_pct']
        self.min_balance = default_config['min_balance']
        self.grid_levels = default_config['grid_levels']
        self.order_expiration = default_config['order_expiration']
        # Grid Trading com range
        self.grid_range_lower = default_config.get('grid_range_lower')
        self.grid_range_upper = default_config.get('grid_range_upper')
        self.grid_kind = default_config.get('grid_kind', 'linear')
        
        # Quantidade por ordem
        self.quantity_per_order_usdc = default_config.get('quantity_per_order_usdc')
        
        # Estado do bot
        self.open_orders: List[Dict] = []
        self.closed_orders: List[Dict] = []
        self.max_closed_orders = 1000  # Limite máximo de ordens fechadas em memória (previne consumo infinito de RAM)
        self.total_profit = Decimal('0')
        self.total_trades = 0
        self.running = False
        
        # Rastreamento de erros do Cloudflare por produto
        # Desabilita temporariamente produtos com muitos erros consecutivos
        self.product_cloudflare_errors: Dict[int, int] = {}  # product_id -> contador de erros
        self.product_disabled_until: Dict[int, float] = {}  # product_id -> timestamp até quando está desabilitado
        self.max_cloudflare_errors = 10  # Máximo de erros consecutivos antes de desabilitar (aumentado para ser mais tolerante)
        self.disabled_cooldown = 120  # 2 minutos de cooldown após desabilitar (aumentado para dar mais tempo ao Cloudflare)
        
        # Rastreamento de erros "Insufficient account health" por produto
        self.product_account_health_errors: Dict[int, int] = {}  # product_id -> contador de erros
        self.product_quantity_multiplier: Dict[int, float] = {}  # product_id -> multiplicador para reduzir quantidade (0.0-1.0)
        self.max_account_health_errors = 3  # Máximo de erros antes de reduzir quantidade
        
        # Rastreamento geral de erros por produto (para desabilitação se muitos erros)
        self.product_general_errors: Dict[int, int] = {}  # product_id -> contador total de erros
        self.max_general_errors = 50  # Máximo de erros totais antes de desabilitar (número alto para não desabilitar facilmente)
        self.product_permanently_disabled: Dict[int, bool] = {}  # product_id -> True se desabilitado
        
        # Arquivo de histórico persistente
        self.history_file = f"logs/{bot_name}_history.json"
        
        # Taxas de trading (em decimal: 0.0035% = 0.000035)
        self.maker_fee = Decimal('0.000035')  # 0.0035% para ordens maker (POST_ONLY)
        self.taker_fee = Decimal('0.00001')   # 0.001% para ordens taker (market orders)
        
        # Configurar logger específico para este bot
        self.logger = setup_logger(bot_name)
        
        # Resetar produtos desabilitados ao iniciar (dar uma nova chance)
        # Isso permite que produtos que foram desabilitados anteriormente sejam reativados ao reiniciar
        if self.product_disabled_until:
            reset_count = len(self.product_disabled_until)
            self.product_disabled_until.clear()
            self.product_cloudflare_errors.clear()
            if reset_count > 0:
                self.logger.info(f"Resetando {reset_count} produto(s) desabilitado(s) - dando nova chance ao reiniciar")
        
        # Log de inicialização mostrando produtos configurados
        self.logger.info("=" * 60)
        self.logger.info(f"INICIALIZANDO {bot_name}")
        self.logger.info("=" * 60)
        self.logger.info(f"Produtos configurados: {len(self.products)} produto(s)")
        for prod_id, prod_info in self.products.items():
            self.logger.info(f"  - Product ID {prod_id}: {prod_info.get('name', 'Nome não especificado')}")
        self.logger.info(f"Alavancagem: {self.leverage}x")
        self.logger.info(f"Quantidade por ordem: {self.quantity_per_order_usdc} USDC" if self.quantity_per_order_usdc else "Quantidade: amount_x18")
        self.logger.info("=" * 60)
        
        # Carregar histórico ao iniciar
        self.load_history()
    
    def load_history(self):
        """Carregar histórico de trades de arquivo JSON"""
        try:
            # Verificar se deve resetar o histórico (variável de ambiente)
            reset_history = os.getenv('RESET_HISTORY', 'false').lower() == 'true'
            if reset_history and os.path.exists(self.history_file):
                backup_file = f"{self.history_file}.backup_{int(time.time())}"
                import shutil
                shutil.copy2(self.history_file, backup_file)
                os.remove(self.history_file)
                self.logger.warning(f"⚠️  Histórico RESETADO! Backup salvo em: {backup_file}")
                self.logger.warning("⚠️  Para resetar novamente, use: RESET_HISTORY=true")
                self.logger.info("✅ Iniciando com histórico zerado: 0 trades, 0.0000 USDT")
                return
            
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
                    # Somar todos os lucros líquidos do histórico
                    for trade in history.get('trades', []):
                        self.total_profit += Decimal(str(trade.get('net_profit', 0)))
                        self.total_trades += 1
                    self.logger.info(
                        f"📂 Histórico carregado: {self.total_trades} trades, "
                        f"P/L acumulado: {float(self.total_profit):.4f} USDT"
                    )
            else:
                # Arquivo de histórico não existe, iniciar do zero
                self.logger.info("✅ Nenhum histórico encontrado. Iniciando do zero: 0 trades, 0.0000 USDT")
        except Exception as e:
            self.logger.warning(f"Erro ao carregar histórico: {e}")
            self.logger.info("✅ Iniciando com histórico zerado devido ao erro")
    
    def save_trade_to_history(self, trade_data: Dict):
        """Salvar um trade no arquivo de histórico JSON"""
        try:
            # Criar diretório se não existir
            os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
            
            # Carregar histórico existente ou criar novo
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            else:
                history = {'trades': [], 'created_at': datetime.now().isoformat()}
            
            # Adicionar novo trade
            history['trades'].append(trade_data)
            history['last_updated'] = datetime.now().isoformat()
            history['total_trades'] = len(history['trades'])
            # Calcular total_profit teórico (somando net_profit de todos os trades)
            history['total_profit_theoretical'] = sum(t.get('net_profit', 0) for t in history['trades'])
            
            # Salvar de volta
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            self.logger.error(f"Erro ao salvar histórico: {e}")
    
    def log_trade(self, order_type: str, order_digest: str, price: float, amount: float,
                  profit: Optional[float] = None):
        """Log detalhado de cada ordem"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if profit is not None:
            self.logger.info(f"[{timestamp}] {order_type} | Digest: {order_digest[:16]}... | "
                       f"Preço: {price:.2f} | Qtd: {amount:.6f} | "
                       f"P/L líquido: {profit:+.4f} USDT | Total acumulado: {float(self.total_profit):+.4f} USDT")
        else:
            self.logger.info(f"[{timestamp}] {order_type} | Digest: {order_digest[:16]}... | "
                       f"Preço: {price:.2f} | Qtd: {amount:.6f}")
    
    def get_size_increment(self, product_id: int) -> int:
        """
        Retorna o size_increment (em x18) para um produto específico.
        Cada produto tem seu próprio size_increment que deve ser respeitado.
        """
        # Mapeamento de product_id para size_increment_x18
        # Baseado na documentação: https://docs.nado.xyz/developer-resources/api/symbols
        # - Product 2 (BTC-PERP): 0.00005 BTC = 50000000000000
        size_increments = {
            2: 50000000000000,      # 0.00005 BTC (BTC-PERP)
            3: 1000000000000000,    # 0.001 WETH (WETH/USDT0) - valor estimado, ajustar se necessário
            4: 1000000000000000,    # 0.001 ETH (ETH-PERP) - valor estimado, ajustar se necessário
        }
        
        if product_id in size_increments:
            return size_increments[product_id]
        
        # Fallback: tentar BTC size_increment se não conhecido
        self.logger.warning(
            f"Product ID {product_id} não tem size_increment conhecido. "
            f"Usando default de BTC (0.00005). Se houver erro, adicione o size_increment correto."
        )
        return 50000000000000  # Default BTC
    
    def is_cloudflare_error(self, error: Exception) -> bool:
        """Verifica se o erro é um bloqueio do Cloudflare Challenge"""
        error_str = str(error)
        error_type = type(error).__name__
        
        # Excluir erros de rede/DNS que não são do Cloudflare
        # Verificar tanto o tipo do erro quanto a string do erro
        network_error_types = [
            "NameResolutionError", "ConnectionError", "Timeout", 
            "MaxRetryError", "ConnectionRefusedError"
        ]
        
        network_error_strings = [
            "NameResolutionError", "Failed to resolve", "nodename nor servname",
            "ConnectionError", "Connection refused", "Timeout", 
            "Max retries exceeded", "HTTPSConnectionPool"
        ]
        
        # Verificar tipo do erro
        if any(net_type in error_type for net_type in network_error_types):
            return False  # Não é erro do Cloudflare, é erro de rede
        
        # Verificar string do erro
        if any(net_str in error_str for net_str in network_error_strings):
            return False  # Não é erro do Cloudflare, é erro de rede
        
        # Verificar se é uma exceção de conexão do requests
        import requests
        if isinstance(error, (requests.exceptions.ConnectionError, 
                             requests.exceptions.Timeout,
                             requests.exceptions.RequestException)):
            # Mas verificar se não é um NameResolutionError dentro do ConnectionError
            if "NameResolutionError" not in error_str and "Failed to resolve" not in error_str:
                # Pode ser um erro de conexão real, mas não DNS, então pode ser Cloudflare
                pass
            else:
                return False  # É erro de DNS, não Cloudflare
        
        # Cloudflare retorna HTML com "Just a moment..." ou "challenge-platform"
        if "Just a moment" in error_str or "challenge-platform" in error_str or "<!DOCTYPE html>" in error_str:
            return True
        if isinstance(error, BadStatusCodeException):
            return True
        return False
    
    def is_product_disabled(self, product_id: int) -> bool:
        """Verifica se um produto está desabilitado (temporariamente ou permanentemente)"""
        # Verificar se está permanentemente desabilitado
        if product_id in self.product_permanently_disabled and self.product_permanently_disabled[product_id]:
            return True
        
        # Verificar se está temporariamente desabilitado devido a erros do Cloudflare
        if product_id in self.product_disabled_until:
            current_time = time.time()
            if current_time < self.product_disabled_until[product_id]:
                # Ainda está no período de cooldown
                remaining = int(self.product_disabled_until[product_id] - current_time)
                product_name = self.products.get(product_id, {}).get('name', f'Product_{product_id}')
                # Usar INFO ao invés de DEBUG para que seja visível nos logs
                self.logger.warning(
                    f"[{product_name}] Temporariamente desabilitado devido a erros do Cloudflare. "
                    f"Reativando em {remaining}s"
                )
                return True
            else:
                # Período de cooldown expirou, reabilitar o produto
                del self.product_disabled_until[product_id]
                if product_id in self.product_cloudflare_errors:
                    del self.product_cloudflare_errors[product_id]
                product_name = self.products.get(product_id, {}).get('name', f'Product_{product_id}')
                self.logger.info(f"[{product_name}] ✅ Reabilitado após período de cooldown")
                return False  # Produto reabilitado
        return False
    
    def record_cloudflare_error(self, product_id: int):
        """Registra um erro do Cloudflare para um produto e desabilita se necessário"""
        if product_id not in self.product_cloudflare_errors:
            self.product_cloudflare_errors[product_id] = 0
        self.product_cloudflare_errors[product_id] += 1
        
        product_name = self.products.get(product_id, {}).get('name', f'Product_{product_id}')
        error_count = self.product_cloudflare_errors[product_id]
        
        if error_count >= self.max_cloudflare_errors:
            # Desabilitar produto por um período de cooldown
            self.product_disabled_until[product_id] = time.time() + self.disabled_cooldown
            self.logger.warning(
                f"[{product_name}] Desabilitado temporariamente após {error_count} erros consecutivos "
                f"do Cloudflare. Reativando em {self.disabled_cooldown}s"
            )
        else:
            self.logger.warning(
                f"[{product_name}] Erro do Cloudflare ({error_count}/{self.max_cloudflare_errors}). "
                f"Se atingir {self.max_cloudflare_errors}, produto será desabilitado temporariamente."
            )
    
    def record_cloudflare_success(self, product_id: int):
        """Registra sucesso na API, resetando contador de erros do Cloudflare"""
        if product_id in self.product_cloudflare_errors:
            del self.product_cloudflare_errors[product_id]
    
    def get_market_price(self, product_id: int) -> float:
        """Obter preço de mercado atual para um produto específico"""
        # Verificar se produto está desabilitado
        if self.is_product_disabled(product_id):
            product_name = self.products.get(product_id, {}).get('name', f'Product_{product_id}')
            raise Exception(f"{product_name} está temporariamente desabilitado devido a erros do Cloudflare")
        
        # Adicionar pequeno delay para evitar rate limiting (apenas se não tiver erros recentes)
        if product_id not in self.product_cloudflare_errors or self.product_cloudflare_errors.get(product_id, 0) == 0:
            time.sleep(0.3)  # Delay de 0.3s entre requisições para evitar rate limiting
        
        try:
            # Usar get_latest_market_price que está disponível na API
            price_response = self.client.market.get_latest_market_price(product_id)
            
            # Se chegou aqui, a requisição foi bem-sucedida, resetar contador de erros
            self.record_cloudflare_success(product_id)
            
            # A API retorna MarketPriceData com bid_x18 e ask_x18
            # Calcular preço médio (mid price) entre bid e ask
            if hasattr(price_response, 'bid_x18') and hasattr(price_response, 'ask_x18'):
                bid_x18 = price_response.bid_x18
                ask_x18 = price_response.ask_x18
                
                # Converter de x18 para float
                bid = float(from_x18(bid_x18))
                ask = float(from_x18(ask_x18))
                
                # Retornar preço médio (mid price)
                return (bid + ask) / 2.0
            
            # Se chegou aqui, não conseguiu processar
            self.logger.error(f"Resposta recebida: {price_response} (tipo: {type(price_response)})")
            if hasattr(price_response, '__dict__'):
                self.logger.error(f"Atributos disponíveis: {price_response.__dict__}")
            raise ValueError(f"Formato de resposta de preço não reconhecido para produto {product_id}: {price_response}")
        except Exception as e:
            # Registrar erro do Cloudflare e potencialmente desabilitar produto
            if self.is_cloudflare_error(e):
                self.record_cloudflare_error(product_id)
                raise
            # Não logar como ERROR se for erro do Cloudflare (será tratado no nível superior)
            self.logger.error(f"Erro ao obter preço de mercado para produto {product_id}: {e}")
            raise
    
    def get_balance(self) -> float:
        """Obter saldo disponível na subconta"""
        try:
            sender = subaccount_to_hex(SubaccountParams(
                subaccount_owner=self.owner,
                subaccount_name=self.subaccount_name
            ))
            
            # Tentar diferentes métodos da API para obter saldo (USDT0 = product_id 0)
            # A API da Nado pode variar, então tentamos múltiplas abordagens
            try:
                balance_response = None
                
                # Tentar método query subaccount balance
                if hasattr(self.client.spot, 'query_subaccount_balance'):
                    balance_response = self.client.spot.query_subaccount_balance(
                        subaccount=sender,
                        product_id=0  # USDT0
                    )
                elif hasattr(self.client, 'query') and hasattr(self.client.query, 'subaccount_balance'):
                    balance_response = self.client.query.subaccount_balance(
                        subaccount=sender,
                        product_id=0  # USDT0
                    )
                
                if balance_response:
                    # Converter de x18 para float
                    if hasattr(balance_response, 'amount'):
                        return float(from_x18(balance_response.amount))
                    elif isinstance(balance_response, dict) and 'amount' in balance_response:
                        return float(from_x18(balance_response['amount']))
                
                # Se não conseguiu obter, continuar sem verificação
                self.logger.warning("Não foi possível obter saldo USDT0 da API. Continuando sem verificação de saldo.")
                return float('inf')
                    
            except AttributeError:
                # Método não existe, continuar sem verificação
                self.logger.warning("Método de obtenção de saldo não disponível na API. Continuando sem verificação.")
                return float('inf')
                
        except Exception as e:
            self.logger.warning(f"Erro ao obter saldo: {e}. Continuando sem verificação de saldo.")
            return float('inf')  # Retornar infinito para permitir que o bot continue
    
    def check_balance(self) -> bool:
        """Verificar se o saldo é suficiente"""
        balance = self.get_balance()
        # Se o saldo for infinito (não foi possível obter), permitir continuar
        if balance == float('inf'):
            return True
        if balance < self.min_balance:
            self.logger.warning(f"Saldo insuficiente: {balance:.2f} USDT (mínimo: {self.min_balance} USDT)")
            return False
        return True
    
    def place_order(self, product_id: int, side: str, price: float, amount_x18: int, 
                   stop_loss: Optional[float] = None, take_profit: Optional[float] = None) -> Optional[Dict]:
        """Colocar ordem no exchange com alavancagem"""
        try:
            # Converter preço para formato x18
            price_x18 = to_x18(price)
            
            # Determinar amount (positivo para compra, negativo para venda)
            if side == 'sell':
                amount_x18 = -abs(amount_x18)
            else:
                amount_x18 = abs(amount_x18)
            
            # Criar appendix com leverage (40x)
            # A alavancagem é aplicada através do appendix da ordem
            # build_appendix pode aceitar parâmetros adicionais para leverage
            try:
                # Tentar criar appendix com leverage se suportado
                appendix = build_appendix(OrderType.POST_ONLY)
                # Nota: A alavancagem pode ser configurada no nível da subconta
                # ou através de parâmetros específicos do appendix
                # Se a API suportar leverage no appendix, adicione aqui
            except:
                # Fallback para POST_ONLY padrão
                appendix = build_appendix(OrderType.POST_ONLY)
            
            # Criar parâmetros da ordem
            order = OrderParams(
                sender=SubaccountParams(
                    subaccount_owner=self.owner,
                    subaccount_name=self.subaccount_name,
                ),
                priceX18=price_x18,
                amount=amount_x18,
                expiration=get_expiration_timestamp(self.order_expiration),
                nonce=gen_order_nonce(),
                appendix=appendix  # Post-only para market making
            )
            
            # Calcular digest da ordem (necessário para cancelamento)
            order_for_digest = OrderParams(
                sender=SubaccountParams(
                    subaccount_owner=self.owner,
                    subaccount_name=self.subaccount_name,
                ),
                priceX18=price_x18,
                amount=amount_x18,
                expiration=order.expiration,
                nonce=order.nonce,
                appendix=order.appendix
            )
            order_for_digest.sender = subaccount_to_bytes32(order_for_digest.sender)
            order_digest = self.client.context.engine_client.get_order_digest(
                order_for_digest, product_id
            )
            
            # Colocar ordem
            response = self.client.market.place_order(
                PlaceOrderParams(product_id=product_id, order=order)
            )
            
            product_name = self.products.get(product_id, {}).get('name', f'Product_{product_id}')
            
            order_info = {
                'digest': order_digest,
                'product_id': product_id,
                'product_name': product_name,
                'side': side,
                'price': price,
                'amount': float(from_x18(abs(amount_x18))),
                'price_x18': price_x18,
                'amount_x18': amount_x18,
                'leverage': self.leverage,
                'status': 'open',
                'timestamp': time.time(),
                'stop_loss': stop_loss,
                'take_profit': take_profit,
                'order': order,
                'response': response
            }
            
            self.open_orders.append(order_info)
            self.log_trade(
                f"ORDEM ABERTA ({side.upper()}) [{product_name}] {self.leverage}x", 
                order_digest, price, order_info['amount']
            )
            
            return order_info
            
        except Exception as e:
            error_str = str(e)
            product_name = self.products.get(product_id, {}).get('name', f'Product_{product_id}')
            
            # Registrar erro geral (mas não contar erros de Cloudflare que já são tratados separadamente)
            if not self.is_cloudflare_error(e):
                if product_id not in self.product_general_errors:
                    self.product_general_errors[product_id] = 0
                self.product_general_errors[product_id] += 1
                
                # Se muitos erros, desabilitar permanentemente
                if self.product_general_errors[product_id] >= self.max_general_errors:
                    if product_id not in self.product_permanently_disabled or not self.product_permanently_disabled[product_id]:
                        self.product_permanently_disabled[product_id] = True
                        self.logger.error(
                            f"[{product_name}] DESABILITADO após {self.product_general_errors[product_id]} erros. "
                            f"Reinicie o bot para reativar."
                        )
            
            # Verificar se é erro de "Insufficient account health"
            if "Insufficient account health" in error_str or ("error_code" in error_str and "2006" in error_str):
                # Registrar erro de account health e reduzir quantidade
                if product_id not in self.product_account_health_errors:
                    self.product_account_health_errors[product_id] = 0
                self.product_account_health_errors[product_id] += 1
                
                error_count = self.product_account_health_errors[product_id]
                if error_count >= self.max_account_health_errors:
                    # Reduzir multiplicador de quantidade (começar com 0.7, depois 0.5, 0.3)
                    if product_id not in self.product_quantity_multiplier:
                        self.product_quantity_multiplier[product_id] = 0.7
                    else:
                        current_mult = self.product_quantity_multiplier[product_id]
                        if current_mult > 0.3:
                            self.product_quantity_multiplier[product_id] = max(0.3, current_mult * 0.7)
                    
                    mult = self.product_quantity_multiplier[product_id]
                    self.logger.warning(
                        f"[{product_name}] Erro de account health ({error_count}x). "
                        f"Quantidade será reduzida para {mult*100:.0f}% do valor original na próxima tentativa. "
                        f"Considere aumentar o saldo disponível ou reduzir quantity_per_order_usdc."
                    )
                else:
                    self.logger.warning(
                        f"[{product_name}] Erro de account health ({error_count}/{self.max_account_health_errors}). "
                        f"Ordem muito grande para o saldo disponível."
                    )
            
            # Verificar se é erro do Cloudflare
            elif self.is_cloudflare_error(e):
                self.record_cloudflare_error(product_id)
            
            self.logger.error(f"Erro ao criar ordem {side} em {price}: {error_str[:200]}")
            return None
    
    def update_open_orders(self):
        """Atualizar status das ordens abertas para todos os produtos"""
        try:
            sender = subaccount_to_hex(SubaccountParams(
                subaccount_owner=self.owner,
                subaccount_name=self.subaccount_name
            ))
            
            # Obter ordens abertas para todos os produtos
            all_open_digests = {}
            for product_id in self.products.keys():
                try:
                    open_orders_response = self.client.market.get_subaccount_open_orders(
                        product_id, sender
                    )
                    
                    # Extrair digests das ordens abertas
                    open_digests = set()
                    if hasattr(open_orders_response, 'orders'):
                        for order in open_orders_response.orders:
                            if hasattr(order, 'digest'):
                                open_digests.add(order.digest)
                    elif isinstance(open_orders_response, list):
                        for order in open_orders_response:
                            if 'digest' in order:
                                open_digests.add(order['digest'])
                    
                    all_open_digests[product_id] = open_digests
                except Exception as e:
                    self.logger.warning(f"Erro ao obter ordens abertas para produto {product_id}: {e}")
                    all_open_digests[product_id] = set()
            
            # Verificar quais ordens foram fechadas
            orders_to_remove = []
            for order in list(self.open_orders):
                product_id = order.get('product_id')
                open_digests = all_open_digests.get(product_id, set())
                
                if order['digest'] not in open_digests and order['status'] == 'open':
                    # Ordem foi fechada/executada
                    order['status'] = 'closed'
                    order['filled_price'] = order['price']  # Aproximação
                    order['filled_amount'] = order['amount']
                    
                    # Calcular taxa da ordem (todas as ordens são POST_ONLY = maker)
                    order_value = Decimal(str(order['price'])) * Decimal(str(abs(order['amount'])))
                    order_fee = order_value * self.maker_fee
                    order['fee'] = float(order_fee)
                    
                    # Calcular P/L teórico se for uma ordem de fechamento (venda) com ordem de entrada (compra) correspondente
                    profit = None
                    if order['side'] == 'sell' and len(self.closed_orders) > 0:
                        # Procurar ordem de compra correspondente (FIFO - primeira compra)
                        matched_buy_order = None
                        for i, closed_order in enumerate(self.closed_orders):  # Buscar da primeira para a última (FIFO)
                            if closed_order['side'] == 'buy' and closed_order.get('product_id') == product_id:
                                # Verificar se as quantidades são compatíveis (dentro de 10% de diferença)
                                buy_amount = abs(Decimal(str(closed_order.get('amount', 0))))
                                sell_amount = abs(Decimal(str(order.get('amount', 0))))
                                if buy_amount > 0 and abs(buy_amount - sell_amount) / buy_amount <= 0.1:  # Tolerância de 10%
                                    matched_buy_order = (i, closed_order)
                                    break
                        
                        if matched_buy_order:
                            idx, closed_order = matched_buy_order
                            entry_price = Decimal(str(closed_order['price']))
                            exit_price = Decimal(str(order['price']))
                            # Usar a menor quantidade entre compra e venda para evitar cálculos incorretos
                            buy_amount = abs(Decimal(str(closed_order.get('amount', 0))))
                            sell_amount = abs(Decimal(str(order.get('amount', 0))))
                            amount = min(buy_amount, sell_amount)
                            
                            # Calcular lucro bruto (para posição LONG: venda > compra = lucro)
                            gross_profit = (exit_price - entry_price) * amount
                            
                            # Calcular taxas (maker fee para ambas as ordens, pois são POST_ONLY)
                            entry_value = entry_price * amount
                            exit_value = exit_price * amount
                            entry_fee = entry_value * self.maker_fee
                            exit_fee = exit_value * self.maker_fee
                            total_fees = entry_fee + exit_fee
                            
                            # Lucro líquido (deduzindo taxas)
                            net_profit = gross_profit - total_fees
                            
                            profit = float(net_profit)
                            self.total_profit += net_profit
                            self.total_trades += 1
                            
                            # Salvar trade no histórico
                            self.save_trade_to_history({
                                'timestamp': datetime.now().isoformat(),
                                'product_id': product_id,
                                'product_name': order.get('product_name', f'Product_{product_id}'),
                                'entry_price': float(entry_price),
                                'exit_price': float(exit_price),
                                'amount': float(amount),
                                'gross_profit': float(gross_profit),
                                'total_fees': float(total_fees),
                                'net_profit': profit,
                                'leverage': order.get('leverage', 1)
                            })
                            
                            self.logger.info(
                                f"[P/L TEÓRICO] "
                                f"Lucro bruto: {float(gross_profit):.4f} USDT | "
                                f"Taxas: {float(total_fees):.4f} USDT | "
                                f"Lucro líquido: {profit:.4f} USDT"
                            )
                            
                            # IMPORTANTE: Remover a ordem de compra usada para evitar reutilização
                            self.closed_orders.pop(idx)
                        else:
                            # Se não encontrou ordem de compra correspondente, apenas contar o trade
                            self.total_trades += 1
                    elif order['side'] == 'sell':
                        # Venda sem ordem de compra correspondente, apenas contar
                        self.total_trades += 1
                    
                    self.closed_orders.append(order)
                    
                    # Limpar cache de ordens antigas se exceder o limite (previne consumo infinito de RAM)
                    if len(self.closed_orders) > self.max_closed_orders:
                        # Remover as ordens mais antigas (FIFO) mantendo apenas as mais recentes
                        excess = len(self.closed_orders) - self.max_closed_orders
                        removed_count = 0
                        # Remover apenas ordens que não são de compra (para evitar remover ordens que podem ser pareadas)
                        # Ou remover as mais antigas se já temos muitas
                        for _ in range(excess):
                            if len(self.closed_orders) > 0:
                                self.closed_orders.pop(0)  # Remove a ordem mais antiga
                                removed_count += 1
                        if removed_count > 0:
                            self.logger.debug(f"Cache de ordens fechadas limpo: {removed_count} ordens antigas removidas (limite: {self.max_closed_orders})")
                    
                    product_name = order.get('product_name', f"Product_{product_id}")
                    self.log_trade(
                        f"ORDEM FECHADA ({order['side'].upper()}) [{product_name}] {order.get('leverage', 1)}x", 
                        order['digest'], order['price'], order['amount'], 
                        profit if profit else None
                    )
                    
                    orders_to_remove.append(order)
            
            # Remover ordens fechadas da lista de abertas
            for order in orders_to_remove:
                self.open_orders.remove(order)
            
        except Exception as e:
            self.logger.warning(f"Erro ao verificar ordens abertas: {e}")
    
    def check_risk_limits(self, product_id: int) -> bool:
        """Verificar limites de risco para um produto específico"""
        # Limite de ordens abertas por produto
        active_orders_product = [
            o for o in self.open_orders 
            if o['status'] == 'open' and o.get('product_id') == product_id
        ]
        if len(active_orders_product) >= self.max_open_orders_per_product:
            product_name = self.products.get(product_id, {}).get('name', f'Product_{product_id}')
            self.logger.warning(
                f"Limite de ordens abertas atingido para {product_name}: "
                f"{len(active_orders_product)}/{self.max_open_orders_per_product}"
            )
            return False
        
        # Verificar saldo
        if not self.check_balance():
            return False
        
        return True
    
    def manage_open_positions(self):
        """Gerenciar posições abertas (Stop Loss, Take Profit e limpeza de ordens antigas) para todos os produtos"""
        try:
            current_time = time.time()
            
            for order in list(self.open_orders):
                if order['status'] != 'open':
                    continue
                
                product_id = order.get('product_id')
                if not product_id:
                    continue
                    
                try:
                    market_price = self.get_market_price(product_id)
                except Exception as e:
                    self.logger.warning(f"Erro ao obter preço para produto {product_id}: {e}")
                    continue
                
                # Cancelar ordens muito antigas (mais de 30 minutos = 1800 segundos)
                order_age = current_time - order.get('timestamp', current_time)
                if order_age > 1800:  # 30 minutos
                    product_name = order.get('product_name', f'Product_{product_id}')
                    self.logger.info(
                        f"Cancelando ordem antiga [{product_name}] {order['digest'][:16]}... "
                        f"(idade: {order_age/60:.1f} minutos, preço: {order['price']:.2f})"
                    )
                    self.cancel_order(order)
                    continue
                
                # Cancelar ordens muito longe do preço de mercado (> 2% do preço atual)
                order_price = order['price']
                price_distance_pct = abs((order_price - market_price) / market_price) * 100
                
                if price_distance_pct > 2.0:  # Mais de 2% de distância
                    product_name = order.get('product_name', f'Product_{product_id}')
                    self.logger.info(
                        f"Cancelando ordem longe do preço [{product_name}] {order['digest'][:16]}... "
                        f"(preço ordem: {order_price:.2f}, mercado: {market_price:.2f}, "
                        f"distância: {price_distance_pct:.2f}%)"
                    )
                    self.cancel_order(order)
                    continue
                
                # Verificar Stop Loss e Take Profit
                if order['side'] == 'buy':
                    # Se tiver stop loss configurado e o preço cair abaixo
                    if order.get('stop_loss') and market_price <= order['stop_loss']:
                        self.logger.warning(f"Stop Loss acionado para ordem {order['digest'][:16]}...")
                        self.cancel_order(order)
                    # Se tiver take profit configurado e o preço subir acima
                    elif order.get('take_profit') and market_price >= order['take_profit']:
                        self.logger.info(f"Take Profit acionado para ordem {order['digest'][:16]}...")
                        # Manter a ordem para execução natural (ou cancelar e criar ordem de venda)
                        
                elif order['side'] == 'sell':
                    # Se tiver stop loss configurado e o preço subir acima
                    if order.get('stop_loss') and market_price >= order['stop_loss']:
                        self.logger.warning(f"Stop Loss acionado para ordem {order['digest'][:16]}...")
                        self.cancel_order(order)
                    # Se tiver take profit configurado e o preço cair abaixo
                    elif order.get('take_profit') and market_price <= order['take_profit']:
                        self.logger.info(f"Take Profit acionado para ordem {order['digest'][:16]}...")
            
        except Exception as e:
            self.logger.error(f"Erro ao gerenciar posições: {e}")
    
    def cancel_order(self, order: Dict):
        """Cancelar uma ordem específica"""
        try:
            sender = subaccount_to_hex(SubaccountParams(
                subaccount_owner=self.owner,
                subaccount_name=self.subaccount_name
            ))
            
            product_id = order.get('product_id')
            response = self.client.market.cancel_orders(
                CancelOrdersParams(
                    productIds=[product_id],
                    digests=[order['digest']],
                    sender=sender
                )
            )
            
            order['status'] = 'cancelled'
            product_name = order.get('product_name', f'Product_{product_id}')
            self.logger.info(f"Ordem [{product_name}] {order['digest'][:16]}... cancelada")
            
        except Exception as e:
            self.logger.error(f"Erro ao cancelar ordem {order['digest'][:16]}...: {e}")
    
    def create_market_making_orders(self):
        """Criar ordens de market making próximas ao preço de mercado para todos os produtos"""
        # Se tem range configurado, usar estratégia de Grid Trading
        if self.grid_range_lower is not None and self.grid_range_upper is not None:
            self.create_grid_trading_orders()
            return
        
        # Caso contrário, usar estratégia de Market Making original
        for product_id, product_info in self.products.items():
            # Verificar se produto está desabilitado devido a erros do Cloudflare
            if self.is_product_disabled(product_id):
                    continue
                
            if not self.check_risk_limits(product_id):
                    continue
                
            try:
                product_name = product_info['name']
                
                # Se tem quantidade em USDC, calcular amount_x18 baseado no preço
                amount_x18 = product_info.get('amount_x18')
                base_quantity_usdc = self.quantity_per_order_usdc
                
                # Aplicar multiplicador se houver erro de account health anterior
                if product_id in self.product_quantity_multiplier:
                    mult = self.product_quantity_multiplier[product_id]
                    if base_quantity_usdc:
                        base_quantity_usdc = base_quantity_usdc * mult
                
                if base_quantity_usdc and amount_x18 is None:
                    market_price_temp = self.get_market_price(product_id)
                    quantity_btc = base_quantity_usdc / market_price_temp
                    amount_x18 = to_pow_10(quantity_btc, 18)
                elif amount_x18 is None:
                    self.logger.error(f"Nenhuma quantidade configurada para {product_name}")
                    continue
                elif product_id in self.product_quantity_multiplier:
                    # Aplicar multiplicador também se usar amount_x18
                    mult = self.product_quantity_multiplier[product_id]
                    amount_x18 = int(amount_x18 * mult)
                
                market_price = self.get_market_price(product_id)
                
                # Calcular preços de compra e venda com spread curto
                spread = market_price * (self.grid_spacing / 100)
                buy_price = market_price - spread
                sell_price = market_price + spread
                
                # Arredondar preços para números inteiros (price_increment = 1.0)
                # O exchange requer que os preços sejam múltiplos exatos de 1.0
                buy_price = round(buy_price)
                sell_price = round(sell_price)
                
                # Ajustar quantidade para garantir valor mínimo da ordem (min_size = 100 USDT)
                # e ser múltipla do size_increment específico do produto
                # Trabalhar diretamente com valores inteiros em x18 para evitar erros de precisão
                size_increment_x18 = self.get_size_increment(product_id)
                size_increment_btc = float(from_x18(size_increment_x18))
                
                min_order_value_usdt = 50  # Valor mínimo da ordem em USDT (reduzido para permitir ordens menores)
                min_amount_btc = min_order_value_usdt / max(buy_price, sell_price)
                min_amount_x18 = to_pow_10(min_amount_btc, 18)
                
                # Garantir que a quantidade seja pelo menos o mínimo necessário
                current_amount_x18 = amount_x18
                if current_amount_x18 < min_amount_x18:
                    # Calcular quantos increments precisamos para atingir o mínimo
                    min_increments = (min_amount_x18 // size_increment_x18) + 1
                    adjusted_amount_x18 = min_increments * size_increment_x18
                else:
                    # Arredondar para o múltiplo mais próximo do size_increment (usando apenas operações inteiras)
                    # Método: (value + increment/2) // increment * increment
                    half_increment = size_increment_x18 // 2
                    num_increments = (current_amount_x18 + half_increment) // size_increment_x18
                    adjusted_amount_x18 = num_increments * size_increment_x18
                    # Garantir que ainda atenda ao mínimo
                    if adjusted_amount_x18 < min_amount_x18:
                        min_increments = (min_amount_x18 // size_increment_x18) + 1
                        adjusted_amount_x18 = min_increments * size_increment_x18
                
                amount_x18 = adjusted_amount_x18
                
                # Log apenas se mudou significativamente
                current_amount_btc = float(from_x18(current_amount_x18))
                adjusted_amount_btc = float(from_x18(adjusted_amount_x18))
                if abs(adjusted_amount_btc - current_amount_btc) > 0.000001:
                    self.logger.info(
                        f"[{product_name}] Quantidade ajustada de {current_amount_btc:.6f} para "
                        f"{adjusted_amount_btc:.6f} (múltiplo de {size_increment_btc:.6f})"
                    )
                
                # Calcular Stop Loss e Take Profit (R:R 2:1)
                stop_loss_buy = buy_price * (1 - self.stop_loss_pct)
                take_profit_buy = buy_price * (1 + self.take_profit_pct)
                
                stop_loss_sell = sell_price * (1 + self.stop_loss_pct)
                take_profit_sell = sell_price * (1 - self.take_profit_pct)
                
                # Criar ordem de compra
                buy_order = self.place_order(
                    product_id, 'buy', buy_price, amount_x18, 
                    stop_loss_buy, take_profit_buy
                )
                
                # Criar ordem de venda
                sell_order = self.place_order(
                    product_id, 'sell', sell_price, amount_x18,
                    stop_loss_sell, take_profit_sell
                )
                
                if buy_order and sell_order:
                    self.logger.info(
                        f"[{product_name}] Ordens de Market Making criadas "
                        f"({self.leverage}x): Buy@{buy_price:.6f} | Sell@{sell_price:.6f}"
                    )
            
            except Exception as e:
                product_name = product_info.get('name', f'Product_{product_id}')
                # Verificar se é erro do Cloudflare
                if self.is_cloudflare_error(e):
                    self.record_cloudflare_error(product_id)
                    self.logger.warning(
                        f"[{product_name}] Erro do Cloudflare ao criar ordens. "
                        f"Produto pode ser desabilitado temporariamente."
                    )
                else:
                    self.logger.error(f"Erro ao criar ordens de market making para {product_name}: {e}")
    
    def create_grid_trading_orders(self):
        """Criar ordens de Grid Trading com range configurado"""
        import math
        
        for product_id, product_info in self.products.items():
            # Verificar se produto está desabilitado devido a erros do Cloudflare
            if self.is_product_disabled(product_id):
                continue
            
            if not self.check_risk_limits(product_id):
                continue
            
            try:
                product_name = product_info['name']
                market_price = self.get_market_price(product_id)
                
                # Validar preço de mercado
                if market_price <= 0:
                    self.logger.error(f"[{product_name}] Preço de mercado inválido: {market_price}")
                    continue
                
                # Verificar se grid_range está configurado
                if self.grid_range_lower is None or self.grid_range_upper is None:
                    self.logger.warning(f"[{product_name}] Grid range não configurado. Pulando grid trading.")
                    continue
                
                # Calcular quantidade baseada em USDC ou usar amount_x18
                base_quantity_usdc = self.quantity_per_order_usdc
                
                # Aplicar multiplicador se houver erro de account health anterior
                if product_id in self.product_quantity_multiplier:
                    mult = self.product_quantity_multiplier[product_id]
                    if base_quantity_usdc:
                        base_quantity_usdc = base_quantity_usdc * mult
                
                if base_quantity_usdc:
                    quantity_btc = base_quantity_usdc / market_price
                    amount_x18 = to_pow_10(quantity_btc, 18)
                else:
                    amount_x18 = product_info.get('amount_x18')
                    if not amount_x18:
                        self.logger.error(f"Nenhuma quantidade configurada para {product_name}")
                        continue
                    # Aplicar multiplicador também se usar amount_x18
                    if product_id in self.product_quantity_multiplier:
                        mult = self.product_quantity_multiplier[product_id]
                        amount_x18 = int(amount_x18 * mult)
                
                # Calcular range de preços
                lower_price = market_price * (1 + self.grid_range_lower / 100)
                upper_price = market_price * (1 + self.grid_range_upper / 100)
                
                # Validar e ajustar preços
                if lower_price <= 0:
                    self.logger.warning(f"[{product_name}] Lower price inválido ({lower_price}). Ajustando para 1% acima de zero.")
                    lower_price = market_price * 0.01  # 1% do preço de mercado como mínimo
                
                if upper_price <= lower_price:
                    self.logger.warning(f"[{product_name}] Upper price ({upper_price}) <= Lower price ({lower_price}). Ajustando.")
                    upper_price = market_price * 1.02  # 2% acima do preço de mercado como mínimo
                
                # Arredondar para números inteiros
                lower_price = round(max(1, lower_price))  # Garantir mínimo de 1
                upper_price = round(max(lower_price + 1, upper_price))  # Garantir que upper > lower
                
                # Calcular quantidade de níveis (se grid_levels for usado, senão usar espaçamento)
                if self.grid_levels > 0:
                    num_levels = min(max(1, self.grid_levels), self.max_open_orders_per_product)
                else:
                    # Calcular número de níveis baseado no grid_spacing
                    range_pct = self.grid_range_upper - self.grid_range_lower
                    if self.grid_spacing > 0:
                        num_levels = max(1, int(range_pct / self.grid_spacing))
                        num_levels = min(num_levels, self.max_open_orders_per_product)
                    else:
                        num_levels = 1  # Fallback se grid_spacing for 0
                
                # Garantir que temos pelo menos 1 nível válido
                if num_levels < 1:
                    self.logger.warning(f"[{product_name}] Número de níveis inválido ({num_levels}). Usando 1 nível.")
                    num_levels = 1
                
                # Ajustar quantidade para múltiplo do size_increment específico do produto
                # Trabalhar diretamente com valores inteiros em x18 para evitar erros de precisão
                size_increment_x18 = self.get_size_increment(product_id)
                size_increment_btc = float(from_x18(size_increment_x18))
                
                # Garantir valor mínimo de 100 USDT
                min_order_value_usdt = 100
                if market_price > 0:
                    min_amount_btc = min_order_value_usdt / market_price
                    min_amount_x18 = to_pow_10(min_amount_btc, 18)
                else:
                    self.logger.error(f"[{product_name}] Market price inválido para calcular quantidade mínima. Pulando.")
                    continue
                
                # Trabalhar diretamente em x18 (valores inteiros)
                current_amount_x18 = amount_x18
                if current_amount_x18 < min_amount_x18:
                    # Calcular quantos increments precisamos para atingir o mínimo
                    min_increments = (min_amount_x18 // size_increment_x18) + 1
                    adjusted_amount_x18 = min_increments * size_increment_x18
                else:
                    # Arredondar para o múltiplo mais próximo do size_increment (usando apenas operações inteiras)
                    # Método: (value + increment/2) // increment * increment
                    half_increment = size_increment_x18 // 2
                    num_increments = (current_amount_x18 + half_increment) // size_increment_x18
                    adjusted_amount_x18 = num_increments * size_increment_x18
                    # Garantir que ainda atenda ao mínimo
                    if adjusted_amount_x18 < min_amount_x18:
                        min_increments = (min_amount_x18 // size_increment_x18) + 1
                        adjusted_amount_x18 = min_increments * size_increment_x18
                
                amount_x18 = adjusted_amount_x18
                
                # Validar que lower_price > 0 antes de calcular grids
                if lower_price <= 0:
                    self.logger.error(f"[{product_name}] Lower price inválido ({lower_price}). Pulando grid trading.")
                    continue
                
                # Calcular preços dos grids
                grid_prices = []
                if self.grid_kind == 'geometric':
                    # Grid geométrico: progressão geométrica
                    if num_levels > 1 and lower_price > 0:
                        try:
                            ratio = (upper_price / lower_price) ** (1.0 / (num_levels - 1))
                            for i in range(num_levels):
                                price = lower_price * (ratio ** i)
                                grid_prices.append(round(max(1, price)))  # Garantir preço mínimo de 1
                        except (ZeroDivisionError, ValueError) as e:
                            self.logger.error(f"[{product_name}] Erro ao calcular grid geométrico: {e}. Usando grid linear.")
                            # Fallback para grid linear
                            price_step = (upper_price - lower_price) / max(1, num_levels - 1)
                            for i in range(num_levels):
                                price = lower_price + (price_step * i)
                                grid_prices.append(round(max(1, price)))
                    else:
                        grid_prices.append(round(max(1, lower_price)))
                else:
                    # Grid linear: espaçamento igual
                    if num_levels > 1:
                        price_step = (upper_price - lower_price) / (num_levels - 1)
                        for i in range(num_levels):
                            price = lower_price + (price_step * i)
                            grid_prices.append(round(max(1, price)))  # Garantir preço mínimo de 1
                    else:
                        grid_prices.append(round(max(1, lower_price)))
                
                # Criar ordens de compra (buy) nos preços abaixo do mercado
                # e ordens de venda (sell) nos preços acima do mercado
                orders_created = 0
                mid_price = (lower_price + upper_price) / 2
                
                for grid_price in grid_prices:
                    if orders_created >= self.max_open_orders_per_product:
                        break
                    
                    try:
                        if grid_price < market_price:
                            # Ordem de compra abaixo do preço de mercado
                            stop_loss = grid_price * (1 - self.stop_loss_pct)
                            take_profit = grid_price * (1 + self.take_profit_pct)
                            order = self.place_order(
                                product_id, 'buy', float(grid_price), amount_x18,
                                stop_loss, take_profit
                            )
                            if order:
                                orders_created += 1
                        elif grid_price > market_price:
                            # Ordem de venda acima do preço de mercado
                            stop_loss = grid_price * (1 + self.stop_loss_pct)
                            take_profit = grid_price * (1 - self.take_profit_pct)
                            order = self.place_order(
                                product_id, 'sell', float(grid_price), amount_x18,
                                stop_loss, take_profit
                            )
                            if order:
                                orders_created += 1
                    except Exception as e:
                        # Erros individuais de ordem não são críticos, apenas logar
                        if self.is_cloudflare_error(e):
                            self.record_cloudflare_error(product_id)
                            self.logger.warning(f"Erro do Cloudflare ao criar ordem em {grid_price}. Continuando...")
                        else:
                            self.logger.warning(f"Erro ao criar ordem em {grid_price}: {e}")
                        continue
                
                if orders_created > 0:
                    self.logger.info(
                        f"[{product_name}] Grid Trading criado: {orders_created} ordens "
                        f"no range {lower_price:.0f} - {upper_price:.0f} "
                        f"(grid {self.grid_kind}, leverage {self.leverage}x)"
                    )
            
            except Exception as e:
                product_name = product_info.get('name', f'Product_{product_id}')
                # Verificar se é erro do Cloudflare
                if self.is_cloudflare_error(e):
                    self.record_cloudflare_error(product_id)
                    self.logger.warning(
                        f"[{product_name}] Erro do Cloudflare ao criar grid trading. "
                        f"Produto pode ser desabilitado temporariamente."
                    )
                else:
                    self.logger.error(f"Erro ao criar grid trading para {product_name}: {e}")
    
    def run(self):
        """Loop principal do bot"""
        self.logger.info("=" * 60)
        self.logger.info("INICIANDO BOT DE TRADING NADO FUTURES")
        self.logger.info("=" * 60)
        self.logger.info(f"Alavancagem: {self.leverage}x")
        self.logger.info(f"Subaccount: {self.subaccount_name}")
        self.logger.info(f"Estratégia: Grid Trading / Market Making")
        self.logger.info(f"Produtos: {', '.join([p['name'] for p in self.products.values()])}")
        self.logger.info(f"Grid Spacing: {self.grid_spacing}%")
        self.logger.info(f"Stop Loss: {self.stop_loss_pct*100}% | Take Profit: {self.take_profit_pct*100}% (R:R 2:1)")
        self.logger.info(f"Limite de ordens abertas por produto: {self.max_open_orders_per_product}")
        self.logger.info(f"Taxas: Maker {float(self.maker_fee)*100}% | Taker {float(self.taker_fee)*100}%")
        self.logger.info(f"P/L calculado com taxas deduzidas (maker fee aplicado em todas as ordens POST_ONLY)")
        self.logger.info("=" * 60)
        
        self.running = True
        
        try:
            # Verificar conexão e saldo inicial
            balance = self.get_balance()
            if balance != float('inf'):
                self.logger.info(f"💰 Saldo disponível: {balance:.2f} USDT")
            else:
                self.logger.warning("⚠️  Não foi possível obter saldo da API. Continuando sem verificação de saldo.")
            
            if not self.check_balance():
                self.logger.error("Saldo insuficiente. Encerrando bot.")
                return
            
            # Loop principal
            iteration = 0
            consecutive_errors = 0
            max_consecutive_errors = 5  # Após 5 erros consecutivos, aumentar delay
            last_cache_cleanup = time.time()  # Timestamp da última limpeza de cache
            cache_cleanup_interval = 3600  # Limpar cache a cada 1 hora (3600 segundos)
            
            while self.running:
                try:
                    iteration += 1
                    self.logger.info(f"\n--- Iteração {iteration} ---")
                    
                    # Obter preços de mercado para todos os produtos
                    price_errors = 0
                    for product_id, product_info in self.products.items():
                        try:
                            market_price = self.get_market_price(product_id)
                            self.logger.info(f"[{product_info['name']}] Preço de mercado: {market_price:.6f}")
                        except Exception as e:
                            if self.is_cloudflare_error(e):
                                self.logger.warning(
                                    f"Cloudflare Challenge detectado para {product_info['name']}. "
                                    f"Aguardando antes de tentar novamente..."
                                )
                                price_errors += 1
                            else:
                                self.logger.warning(f"Erro ao obter preço para {product_info['name']}: {e}")
                    
                    # Se todos os preços falharam devido ao Cloudflare, aumentar delay
                    if price_errors == len(self.products):
                        consecutive_errors += 1
                        if consecutive_errors >= max_consecutive_errors:
                            delay = min(60, 10 * consecutive_errors)  # Máximo 60 segundos
                            self.logger.warning(
                                f"Muitos erros consecutivos do Cloudflare ({consecutive_errors}). "
                                f"Aguardando {delay} segundos antes de continuar..."
                            )
                            time.sleep(delay)
                        else:
                            time.sleep(15)  # Aguardar 15 segundos se houver erros do Cloudflare
                        continue
                    else:
                        consecutive_errors = 0  # Reset contador se pelo menos um preço funcionou
                    
                    # Atualizar status das ordens abertas
                    try:
                        self.update_open_orders()
                    except Exception as e:
                        if self.is_cloudflare_error(e):
                            self.logger.warning("Cloudflare Challenge ao atualizar ordens. Pulando esta iteração.")
                            consecutive_errors += 1
                            if consecutive_errors >= max_consecutive_errors:
                                delay = min(60, 10 * consecutive_errors)
                                time.sleep(delay)
                            else:
                                time.sleep(15)
                            continue
                        else:
                            self.logger.warning(f"Erro ao atualizar ordens: {e}")
                    
                    # Gerenciar posições abertas
                    try:
                        self.manage_open_positions()
                    except Exception as e:
                        if self.is_cloudflare_error(e):
                            self.logger.warning("Cloudflare Challenge ao gerenciar posições. Continuando...")
                        else:
                            self.logger.warning(f"Erro ao gerenciar posições: {e}")
                    
                    # Criar novas ordens de market making se necessário
                    try:
                        self.create_market_making_orders()
                    except Exception as e:
                        if self.is_cloudflare_error(e):
                            self.logger.warning("Cloudflare Challenge ao criar ordens. Continuando...")
                        else:
                            self.logger.warning(f"Erro ao criar ordens: {e}")
                    
                    # Reset contador de erros se chegou até aqui sem problemas críticos
                    consecutive_errors = 0
                    
                    # Limpeza periódica de cache de ordens antigas (a cada 1 hora)
                    current_time = time.time()
                    if current_time - last_cache_cleanup >= cache_cleanup_interval:
                        # Remover ordens fechadas muito antigas (mais de 24 horas)
                        # Como não temos timestamp nas ordens, vamos apenas limitar o tamanho
                        if len(self.closed_orders) > self.max_closed_orders:
                            excess = len(self.closed_orders) - self.max_closed_orders
                            removed_count = 0
                            for _ in range(excess):
                                if len(self.closed_orders) > 0:
                                    self.closed_orders.pop(0)
                                    removed_count += 1
                            if removed_count > 0:
                                self.logger.info(f"Limpeza periódica de cache: {removed_count} ordens antigas removidas (total mantido: {len(self.closed_orders)})")
                        last_cache_cleanup = current_time
                    
                    # Resumo do status
                    active_orders = [o for o in self.open_orders if o['status'] == 'open']
                    orders_by_product = {}
                    for order in active_orders:
                        product_name = order.get('product_name', 'Unknown')
                        orders_by_product[product_name] = orders_by_product.get(product_name, 0) + 1
                    
                    for product_name, count in orders_by_product.items():
                        self.logger.info(f"Ordens abertas [{product_name}]: {count}/{self.max_open_orders_per_product}")
                    
                    self.logger.info(f"Total de ordens abertas: {len(active_orders)}")
                    self.logger.info(f"Total de trades: {self.total_trades}")
                    self.logger.info(
                        f"Lucro/Prejuízo acumulado (líquido, após taxas): {float(self.total_profit):.4f} USDT"
                    )
                    
                    # Aguardar antes da próxima iteração
                    time.sleep(5)  # 5 segundos entre iterações
                
                except KeyboardInterrupt:
                    self.logger.info("\nInterrupção do usuário detectada. Encerrando bot...")
                    self.running = False
                    break
                except Exception as e:
                    if self.is_cloudflare_error(e):
                        consecutive_errors += 1
                        delay = min(60, 10 * consecutive_errors)
                        self.logger.warning(
                            f"Cloudflare Challenge detectado no loop principal. "
                            f"Aguardando {delay} segundos... (erros consecutivos: {consecutive_errors})"
                        )
                        time.sleep(delay)
                    else:
                        self.logger.error(f"Erro no loop principal: {e}")
                        import traceback
                        self.logger.error(traceback.format_exc())
                        time.sleep(10)  # Aguardar mais tempo em caso de erro
                        consecutive_errors = 0  # Reset para erros não-Cloudflare
                    
        except Exception as e:
            self.logger.error(f"Erro crítico: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            raise
        
        finally:
            # Fechar todas as ordens abertas antes de encerrar
            self.logger.info("\nFechando ordens abertas...")
            self.close_all_orders()
            
            self.logger.info("=" * 60)
            self.logger.info("BOT ENCERRADO")
            self.logger.info(f"Total de trades: {self.total_trades}")
            
            self.logger.info("=" * 60)
    
    def close_all_orders(self):
        """Fechar todas as ordens abertas de todos os produtos"""
        try:
            sender = subaccount_to_hex(SubaccountParams(
                subaccount_owner=self.owner,
                subaccount_name=self.subaccount_name
            ))
            
            active_orders = [o for o in self.open_orders if o['status'] == 'open']
            if not active_orders:
                return
            
            # Agrupar ordens por product_id
            orders_by_product = {}
            for order in active_orders:
                product_id = order.get('product_id')
                if product_id not in orders_by_product:
                    orders_by_product[product_id] = []
                orders_by_product[product_id].append(order['digest'])
            
            # Cancelar ordens por produto
            total_cancelled = 0
            for product_id, digests in orders_by_product.items():
                try:
                    response = self.client.market.cancel_orders(
                        CancelOrdersParams(
                            productIds=[product_id],
                            digests=digests,
                            sender=sender
                        )
                    )
                    product_name = self.products.get(product_id, {}).get('name', f'Product_{product_id}')
                    self.logger.info(f"{len(digests)} ordens canceladas para {product_name}")
                    total_cancelled += len(digests)
                except Exception as e:
                    product_name = self.products.get(product_id, {}).get('name', f'Product_{product_id}')
                    self.logger.error(f"Erro ao cancelar ordens para {product_name}: {e}")
            
            self.logger.info(f"Total de {total_cancelled} ordens canceladas")
            
        except Exception as e:
            self.logger.error(f"Erro ao cancelar ordens: {e}")


def main():
    """Função principal - mantida para compatibilidade"""
    try:
        # Usar "mainnet" para produção
        # devnet requer configurações adicionais que podem não estar disponíveis
        network = os.getenv('NADO_NETWORK', 'mainnet')
        
        print("AVISO: Use bot1.py ou bot2.py para executar bots com configurações específicas")
        print("Este arquivo (bot.py) contém apenas a classe base.")
        
        # Criar bot padrão (mantido para compatibilidade)
        bot = NadoFuturesBot(network=network, bot_name="BotPadrao")
        bot.run()
    except Exception as e:
        print(f"Erro fatal: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()
