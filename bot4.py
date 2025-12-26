#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bot 4 - Estratégia Larry Williams %R (9,2) em timeframe de 5 minutos
Williams %R é um oscilador de momentum que varia de -100 a 0
- Valores próximos de 0: sobrecompra
- Valores próximos de -100: sobrevenda

Estratégia:
- Compra quando %R(9) cruza acima de -80 (saindo de sobrevenda)
- Venda quando %R(9) cruza abaixo de -20 (saindo de sobrecompra)
- Filtro de tendência usando %R(2): só compra se %R(2) < -50 (tendência de alta)
"""

import os
import time
import logging
from collections import deque
from decimal import Decimal
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dotenv import load_dotenv

from bot import NadoFuturesBot
from nado_protocol.utils.math import to_pow_10

# Carregar variáveis de ambiente
load_dotenv('.env.bot4')
load_dotenv('.env')

class WilliamsRBot(NadoFuturesBot):
    """Bot baseado na estratégia Larry Williams %R"""
    
    def __init__(self, network: str = "mainnet", private_key: Optional[str] = None, 
                 bot_name: str = "Bot4", config: Optional[Dict] = None):
        
        # Configuração padrão baseada no Bot1 (mais rentável)
        default_config = {
            'subaccount_name': "default",
            'leverage': 40,  # Alavancagem de 40x
            'products': {
                2: {'name': 'BTC/USDT0'},      # BTC-PERP (product_id 2) - ✅ Perpétuo
                3: {'name': 'WETH/USDT0'},     # WETH/USDT0 (product_id 3) - ✅ Spot
                4: {'name': 'ETH/USDT0'},      # ETH-PERP (product_id 4) - ✅ Perpétuo
            },
            'quantity_per_order_usdc': 200,  # 200 USDC por ordem
            # Modo agressivo - DESATIVADO (modo padrão)
            'aggressive_mode': False,  # Modo padrão ativo
            'aggressive_grid_spacing': 0.03,  # Grid mais apertado no modo agressivo
            'aggressive_max_orders': 8,  # Mais ordens no modo agressivo
            'aggressive_grid_levels': 5,  # Mais níveis no modo agressivo
            'aggressive_quantity_usdc': 150,  # Quantidade menor no modo agressivo para evitar account health
            'max_open_orders_per_product': 5,
            'stop_loss_pct': 0.02,  # Stop Loss de 2% (igual Bot1)
            'take_profit_pct': 0.04,  # Take Profit de 4% (igual Bot1, R:R 2:1)
            'min_balance': 100,
            'order_expiration': 3600,
            
            # Parâmetros específicos do Williams %R
            'williams_r_period_1': 9,  # Período principal do %R
            'williams_r_period_2': 2,  # Período para filtro de tendência
            'williams_r_overbought': -20,  # Nível de sobrecompra
            'williams_r_oversold': -80,  # Nível de sobrevenda
            'williams_r_trend_filter': -50,  # Filtro de tendência para compras
            'timeframe_minutes': 5,  # Timeframe de 5 minutos
        }
        
        if config:
            default_config.update(config)
        
        # Inicializar bot base
        super().__init__(network=network, private_key=private_key, bot_name=bot_name, config=default_config)
        
        # Configurações específicas do Williams %R
        self.wr_period_1 = default_config['williams_r_period_1']
        self.wr_period_2 = default_config['williams_r_period_2']
        self.wr_overbought = default_config['williams_r_overbought']
        self.wr_oversold = default_config['williams_r_oversold']
        self.wr_trend_filter = default_config['williams_r_trend_filter']
        self.timeframe_seconds = default_config['timeframe_minutes'] * 60
        
        # Armazenar candles para cálculo do %R por produto
        # Estrutura: {product_id: {'candles': deque, 'current_candle': dict, 'last_wr1': float, 'last_wr2': float}}
        self.product_data = {}
        for product_id in self.products.keys():
            self.product_data[product_id] = {
                'candles': deque(maxlen=self.wr_period_1 + 2),
                'current_candle': {'high': None, 'low': None, 'close': None, 'timestamp': None},
                'last_wr1': None,
                'last_wr2': None,
                'position_side': None
            }
        
        self.logger.info(f"Williams %R Bot inicializado: Período 1={self.wr_period_1}, Período 2={self.wr_period_2}")
        self.logger.info(f"Timeframe: {default_config['timeframe_minutes']} minutos")
        self.logger.info(f"Sobrecompra: {self.wr_overbought}, Sobrevenda: {self.wr_oversold}")
    
    def calculate_williams_r(self, period: int, product_id: int) -> Optional[float]:
        """
        Calcula o Williams %R para um período específico e produto específico
        
        Williams %R = ((Highest High - Close) / (Highest High - Lowest Low)) * -100
        
        Onde:
        - Highest High = maior preço nos últimos N períodos
        - Lowest Low = menor preço nos últimos N períodos
        - Close = preço de fechamento atual (último candle fechado)
        """
        product_info = self.product_data.get(product_id)
        if not product_info:
            return None
        
        candles = product_info['candles']
        current_candle = product_info['current_candle']
        
        # Precisamos do candle atual + candles fechados
        # Se não temos candles fechados suficientes, retornar None
        if len(candles) < period - 1:
            return None
        
        # Incluir candle atual para cálculo se ele existir
        candles_for_calc = list(candles)[-period+1:] if len(candles) >= period - 1 else list(candles)
        
        # Adicionar candle atual se existir e tiver dados
        if current_candle.get('timestamp') is not None:
            candles_for_calc.append(current_candle)
        
        if len(candles_for_calc) < period:
            return None
        
        # Obter os últimos N candles
        recent_candles = candles_for_calc[-period:]
        
        # Encontrar Highest High e Lowest Low
        highest_high = max(candle['high'] for candle in recent_candles)
        lowest_low = min(candle['low'] for candle in recent_candles)
        current_close = recent_candles[-1]['close']
        
        # Calcular %R
        if highest_high == lowest_low:
            return -50.0  # Caso de divisão por zero (mercado sem movimento)
        
        williams_r = ((highest_high - current_close) / (highest_high - lowest_low)) * -100
        
        return round(williams_r, 2)
    
    def update_candle(self, price: float, product_id: int):
        """
        Atualiza o candle atual com o preço de mercado
        Cria um novo candle a cada 5 minutos (por produto)
        """
        product_info = self.product_data.get(product_id)
        if not product_info:
            return
        
        current_candle = product_info['current_candle']
        candles = product_info['candles']
        
        current_time = time.time()
        
        # Determinar o início do candle atual (arredondado para múltiplos de 5 minutos)
        candle_start_time = int(current_time // self.timeframe_seconds) * self.timeframe_seconds
        
        # Se é um novo candle
        if current_candle['timestamp'] is None or current_candle['timestamp'] < candle_start_time:
            # Salvar candle anterior se existir
            if current_candle['timestamp'] is not None:
                candles.append({
                    'timestamp': current_candle['timestamp'],
                    'high': current_candle['high'],
                    'low': current_candle['low'],
                    'close': current_candle['close']
                })
                product_name = self.products[product_id]['name']
                self.logger.debug(
                    f"[{product_name}] Novo candle fechado: H={current_candle['high']:.2f}, "
                    f"L={current_candle['low']:.2f}, C={current_candle['close']:.2f}"
                )
            
            # Inicializar novo candle
            product_info['current_candle'] = {
                'timestamp': candle_start_time,
                'high': price,
                'low': price,
                'close': price
            }
        else:
            # Atualizar candle atual
            if price > current_candle['high']:
                current_candle['high'] = price
            if price < current_candle['low']:
                current_candle['low'] = price
            current_candle['close'] = price
    
    def check_entry_signals(self, wr1: float, wr2: float, product_id: int):
        """
        Verifica sinais de entrada baseados no Williams %R
        
        Estratégia:
        - Compra (Long): %R(9) cruza acima de -80 E %R(2) < -50 (filtro de tendência)
        - Venda (Short): %R(9) cruza abaixo de -20
        """
        product_info = self.product_data.get(product_id)
        if not product_info:
            return
        
        last_wr1 = product_info['last_wr1']
        product_name = self.products[product_id]['name']
        
        # Verificar se é produto SPOT (não suporta SHORT da mesma forma)
        is_spot = product_id == 3  # WETH/USDT0 é spot (product_id 3)
        
        # Verificar se já temos posição aberta
        active_positions = [o for o in self.open_orders if o.get('status') == 'open' and o.get('product_id') == product_id]
        
        # Sinal de compra (Long)
        if last_wr1 is not None and wr1 is not None:
            # %R(9) cruzou acima de -80 (saindo de sobrevenda)
            if last_wr1 <= self.wr_oversold and wr1 > self.wr_oversold:
                # Verificar filtro de tendência: %R(2) deve estar < -50
                if wr2 is not None and wr2 < self.wr_trend_filter:
                    # Verificar se já temos posição long
                    has_long = any(o['side'] == 'buy' for o in active_positions)
                    if not has_long and self.check_risk_limits(product_id):
                        self.logger.info(
                            f"[{product_name}] [SINAL DE COMPRA] %R(9)={wr1:.2f} cruzou acima de {self.wr_oversold}, "
                            f"%R(2)={wr2:.2f} < {self.wr_trend_filter} (filtro OK)"
                        )
                        self.enter_long_position(product_id)
                        product_info['position_side'] = 'long'
                        return
        
        # Sinal de venda (Short) - Desabilitado para produtos SPOT
        if last_wr1 is not None and wr1 is not None:
            # %R(9) cruzou abaixo de -20 (saindo de sobrecompra)
            if last_wr1 >= self.wr_overbought and wr1 < self.wr_overbought:
                # Produtos SPOT não suportam SHORT (precisa ter o ativo para vender)
                if is_spot:
                    self.logger.debug(
                        f"[{product_name}] Sinal de venda ignorado: produtos SPOT não suportam SHORT "
                        f"(%R(9)={wr1:.2f} cruzou abaixo de {self.wr_overbought})"
                    )
                    return
                
                # Verificar se já temos posição short
                has_short = any(o['side'] == 'sell' for o in active_positions)
                if not has_short and self.check_risk_limits(product_id):
                    self.logger.info(
                        f"[{product_name}] [SINAL DE VENDA] %R(9)={wr1:.2f} cruzou abaixo de {self.wr_overbought}"
                    )
                    self.enter_short_position(product_id)
                    product_info['position_side'] = 'short'
                    return
    
    def enter_long_position(self, product_id: int):
        """Abrir posição long (compra)"""
        try:
            market_price = self.get_market_price(product_id)
            product_name = self.products[product_id]['name']
            
            # Calcular quantidade baseada em USDC
            if self.quantity_per_order_usdc:
                quantity_btc = self.quantity_per_order_usdc / market_price
                amount_x18 = to_pow_10(quantity_btc, 18)
            else:
                self.logger.error(f"Nenhuma quantidade configurada para {product_name}")
                return
            
            # Preço de compra (market ou ligeiramente abaixo)
            buy_price = market_price * 0.9995  # 0.05% abaixo para executar
            # Arredondar preço para número inteiro (price_increment = 1.0)
            buy_price = round(buy_price)
            
            # Calcular Stop Loss e Take Profit
            stop_loss = buy_price * (1 - self.stop_loss_pct)
            take_profit = buy_price * (1 + self.take_profit_pct)
            # Arredondar SL e TP também
            stop_loss = round(stop_loss)
            take_profit = round(take_profit)
            
            # Criar ordem de compra
            order = self.place_order(
                product_id=product_id,
                side='buy',
                price=buy_price,
                amount_x18=amount_x18,
                stop_loss=stop_loss,
                take_profit=take_profit
            )
            
            if order:
                self.logger.info(
                    f"[POSIÇÃO LONG ABERTA] {product_name} @ {buy_price:.2f} | "
                    f"SL: {stop_loss:.2f} ({self.stop_loss_pct*100:.1f}%) | "
                    f"TP: {take_profit:.2f} ({self.take_profit_pct*100:.1f}%)"
                )
        
        except Exception as e:
            self.logger.error(f"Erro ao abrir posição long: {e}")
    
    def enter_short_position(self, product_id: int):
        """Abrir posição short (venda) - Apenas para produtos PERPÉTUOS"""
        try:
            # Verificar se é produto SPOT (não suporta SHORT)
            if product_id == 3:  # WETH/USDT0 é spot
                product_name = self.products[product_id]['name']
                self.logger.warning(
                    f"[{product_name}] Tentativa de SHORT ignorada: produtos SPOT não suportam SHORT"
                )
                return
            
            market_price = self.get_market_price(product_id)
            product_name = self.products[product_id]['name']
            
            # Calcular quantidade baseada em USDC
            if self.quantity_per_order_usdc:
                quantity_btc = self.quantity_per_order_usdc / market_price
                amount_x18 = to_pow_10(quantity_btc, 18)
            else:
                self.logger.error(f"Nenhuma quantidade configurada para {product_name}")
                return
            
            # Preço de venda (market ou ligeiramente acima)
            sell_price = market_price * 1.0005  # 0.05% acima para executar
            # Arredondar preço para número inteiro (price_increment = 1.0)
            sell_price = round(sell_price)
            
            # Validar preço antes de criar ordem
            if sell_price <= 0:
                self.logger.error(f"[{product_name}] Preço de venda inválido: {sell_price}")
                return
            
            # Calcular Stop Loss e Take Profit
            stop_loss = sell_price * (1 + self.stop_loss_pct)
            take_profit = sell_price * (1 - self.take_profit_pct)
            # Arredondar SL e TP também
            stop_loss = round(stop_loss)
            take_profit = round(take_profit)
            
            # Log detalhado antes de criar ordem
            self.logger.debug(
                f"[{product_name}] Tentando criar ordem SHORT: "
                f"preço={sell_price:.2f}, quantidade={quantity_btc:.6f}, "
                f"amount_x18={amount_x18}, SL={stop_loss:.2f}, TP={take_profit:.2f}"
            )
            
            # Criar ordem de venda
            order = self.place_order(
                product_id=product_id,
                side='sell',
                price=sell_price,
                amount_x18=amount_x18,
                stop_loss=stop_loss,
                take_profit=take_profit
            )
            
            if order:
                self.logger.info(
                    f"[POSIÇÃO SHORT ABERTA] {product_name} @ {sell_price:.2f} | "
                    f"SL: {stop_loss:.2f} ({self.stop_loss_pct*100:.1f}%) | "
                    f"TP: {take_profit:.2f} ({self.take_profit_pct*100:.1f}%)"
                )
            else:
                self.logger.warning(
                    f"[{product_name}] Falha ao criar ordem SHORT: place_order retornou None"
                )
        
        except Exception as e:
            product_name = self.products.get(product_id, {}).get('name', f'Product_{product_id}')
            self.logger.error(
                f"[{product_name}] Erro ao abrir posição short: {e}",
                exc_info=True
            )
    
    def run_williams_strategy(self):
        """Loop principal da estratégia Williams %R"""
        self.running = True
        
        try:
            self.logger.info("=" * 60)
            self.logger.info("BOT WILLIAMS %R INICIADO")
            self.logger.info(f"Estratégia: Larry Williams %R({self.wr_period_1},{self.wr_period_2})")
            self.logger.info(f"Timeframe: {self.timeframe_seconds // 60} minutos")
            self.logger.info(f"Stop Loss: {self.stop_loss_pct*100:.1f}% | Take Profit: {self.take_profit_pct*100:.1f}%")
            self.logger.info("=" * 60)
            
            # Verificar conexão e saldo
            balance = self.get_balance()
            if balance != float('inf'):
                self.logger.info(f"Saldo inicial: {balance:.2f} USDT")
            
            if not self.check_balance():
                self.logger.error("Saldo insuficiente. Encerrando bot.")
                return
            
            iteration = 0
            consecutive_errors = 0
            
            while self.running:
                try:
                    iteration += 1
                    self.logger.info(f"\n--- Iteração {iteration} ---")
                    
                    # Processar cada produto
                    for product_id, product_info in self.products.items():
                        product_name = product_info['name']
                        
                        # Obter preço de mercado atual
                        try:
                            market_price = self.get_market_price(product_id)
                            if market_price is None:
                                continue
                            consecutive_errors = 0  # Reset contador se preço foi obtido
                        except Exception as e:
                            if self.is_cloudflare_error(e):
                                consecutive_errors += 1
                                delay = min(90, 15 * consecutive_errors)
                                self.logger.warning(
                                    f"Cloudflare Challenge ao obter preço para {product_name}. "
                                    f"Aguardando {delay} segundos... (erros consecutivos: {consecutive_errors})"
                                )
                                time.sleep(delay)
                                continue
                            else:
                                self.logger.warning(f"Erro ao obter preço para {product_name}: {e}")
                                continue
                        
                        # Atualizar candle atual
                        self.update_candle(market_price, product_id)
                        
                        # Calcular Williams %R
                        wr1 = self.calculate_williams_r(self.wr_period_1, product_id)
                        wr2 = self.calculate_williams_r(self.wr_period_2, product_id)
                        
                        product_info = self.product_data[product_id]
                        candles = product_info['candles']
                        
                        if wr1 is not None and wr2 is not None:
                            # Log dos valores do indicador
                            self.logger.info(
                                f"[{product_name}] Preço: {market_price:.2f} | "
                                f"%R({self.wr_period_1})={wr1:.2f} | %R({self.wr_period_2})={wr2:.2f} | "
                                f"Candles: {len(candles)}/{self.wr_period_1}"
                            )
                            
                            # Verificar sinais de entrada
                            self.check_entry_signals(wr1, wr2, product_id)
                            
                            # Atualizar valores anteriores
                            product_info['last_wr1'] = wr1
                            product_info['last_wr2'] = wr2
                        else:
                            # Ainda não temos candles suficientes
                            needed_candles = self.wr_period_1 - len(candles)
                            self.logger.info(
                                f"[{product_name}] Aguardando candles... "
                                f"({len(candles)}/{self.wr_period_1} - faltam {needed_candles} candles de 5min)"
                            )
                        
                        # Verificar ordens abertas e calcular P/L (a cada iteração)
                        # Gerenciar posições (Stop Loss, Take Profit)
                        self.manage_open_positions()
                    
                    # Resumo do status
                    active_orders = [o for o in self.open_orders if o['status'] == 'open']
                    self.logger.info(f"Ordens abertas: {len(active_orders)}")
                    self.logger.info(f"Total de trades: {self.total_trades}")
                    
                    # Mostrar P/L TEÓRICO (apenas teórico, não há cálculo de P/L real)
                    theoretical_pl = float(self.total_profit)
                    if theoretical_pl >= 0:
                        self.logger.info(f"📊 P/L TEÓRICO (estimado): +{theoretical_pl:.4f} USDT | Trades: {self.total_trades}")
                    else:
                        self.logger.warning(f"⚠️  P/L TEÓRICO (estimado): {theoretical_pl:.4f} USDT | Trades: {self.total_trades}")
                    
                    # Aguardar antes da próxima iteração (30 segundos para atualizar candles mais frequentemente)
                    # Atualizar ordens abertas a cada iteração
                    self.update_open_orders()
                    time.sleep(30)
                
                except KeyboardInterrupt:
                    self.logger.info("\nInterrupção do usuário detectada. Encerrando bot...")
                    self.running = False
                    break
                
                except Exception as e:
                    if self.is_cloudflare_error(e):
                        delay = min(90, 15 * (consecutive_errors + 1))
                        self.logger.warning(
                            f"Cloudflare Challenge detectado. Aguardando {delay} segundos... "
                            f"(erros consecutivos: {consecutive_errors + 1})"
                        )
                        consecutive_errors += 1
                        time.sleep(delay)
                    else:
                        self.logger.error(f"Erro no loop principal: {e}")
                        import traceback
                        self.logger.error(traceback.format_exc())
                        time.sleep(60)  # Aguardar mais tempo em caso de erro
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
            self.logger.info("BOT WILLIAMS %R ENCERRADO")
            self.logger.info(f"Total de trades: {self.total_trades}")
            self.logger.info(
                f"Lucro/Prejuízo final (líquido, após taxas): {float(self.total_profit):.4f} USDT"
            )
            self.logger.info("=" * 60)
    
    def run(self):
        """Método principal - redireciona para estratégia Williams %R"""
        self.run_williams_strategy()


def main():
    """Bot 4 - Estratégia Larry Williams %R (9,2)"""
    try:
        network = os.getenv('NADO_NETWORK', 'mainnet')
        
        # Configuração baseada no Bot1 (mais rentável até agora)
        config = {
            'subaccount_name': "default",
            'leverage': 40,  # Alavancagem de 40x
            'products': {
                2: {'name': 'BTC/USDT0'},      # BTC-PERP (product_id 2) - ✅ Perpétuo
                3: {'name': 'WETH/USDT0'},     # WETH/USDT0 (product_id 3) - ✅ Spot
                4: {'name': 'ETH/USDT0'},      # ETH-PERP (product_id 4) - ✅ Perpétuo
            },
            'quantity_per_order_usdc': 200,  # 200 USDC por ordem
            'max_open_orders_per_product': 5,  # Igual Bot1
            'stop_loss_pct': 0.02,  # Stop Loss de 2% (igual Bot1)
            'take_profit_pct': 0.04,  # Take Profit de 4% (igual Bot1, R:R 2:1)
            'min_balance': 100,
            'order_expiration': 3600,
            
            # Parâmetros Williams %R
            'williams_r_period_1': 9,
            'williams_r_period_2': 2,
            'williams_r_overbought': -20,
            'williams_r_oversold': -80,
            'williams_r_trend_filter': -50,
            'timeframe_minutes': 5,  # 5 minutos
        }
        
        # Criar bot com estratégia Williams %R
        bot = WilliamsRBot(
            network=network,
            private_key=os.getenv('PRIVATE_KEY_BOT4') or os.getenv('PRIVATE_KEY'),
            bot_name="Bot4",
            config=config
        )
        
        bot.run()
    
    except Exception as e:
        print(f"Erro fatal no Bot4: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()

