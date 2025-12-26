# Bot4 - Estratégia Larry Williams %R (9,2)

## 📊 Estratégia

O Bot4 implementa a estratégia **Larry Williams %R** com os seguintes parâmetros:
- **Williams %R Período 1**: 9 períodos (indicador principal)
- **Williams %R Período 2**: 2 períodos (filtro de tendência)
- **Timeframe**: 5 minutos

## 🎯 Sinais de Entrada

### Compra (Long)
- %R(9) cruza **acima de -80** (saindo de sobrevenda)
- **E** %R(2) < -50 (filtro de tendência - confirma tendência de alta)

### Venda (Short)
- %R(9) cruza **abaixo de -20** (saindo de sobrecompra)

## 📈 Gerenciamento de Risco

Baseado no **Bot1** (mais rentável):
- ✅ **Leverage**: 40x
- ✅ **Stop Loss**: 2%
- ✅ **Take Profit**: 4% (R:R 2:1)
- ✅ **Quantidade por ordem**: 250 USDC
- ✅ **Máximo de ordens abertas**: 5 por produto
- ✅ **Saldo mínimo**: 100 USDT

## 🔧 Como Funciona

1. **Cálculo de Candles**: O bot armazena candles de 5 minutos baseado no preço de mercado atual
2. **Williams %R**: Calcula o indicador usando os últimos N candles
3. **Sinais**: Monitora cruzamentos do %R para identificar oportunidades
4. **Execução**: Abre posições long/short quando os sinais são confirmados
5. **Proteção**: Aplica Stop Loss e Take Profit automaticamente

## 🚀 Como Executar

```bash
# Executar apenas o Bot4
python3 bot4.py

# Ou iniciar todos os bots (incluindo Bot4)
./start_all_bots.sh

# Ver logs em tempo real
./watch_bot4.sh
# ou
tail -f logs/bot4.log
```

## 📝 Logs

O bot registra:
- Valores atuais do Williams %R(9) e %R(2)
- Sinais de entrada identificados
- Posições abertas com Stop Loss e Take Profit
- Lucro/Prejuízo acumulado

## ⚠️ Observações

- O bot precisa de **pelo menos 9 candles de 5 minutos** (45 minutos) para começar a gerar sinais
- Durante os primeiros 45 minutos, o bot apenas coleta dados e não executa trades
- Os candles são atualizados a cada 5 minutos (arredondado para múltiplos de 5 minutos)
- O bot verifica o mercado a cada 30 segundos para atualizar os candles e verificar sinais

## 📊 Exemplo de Log

```
[2025-12-24 10:30:00] [Bot4] INFO - [BTC/USDT0] Preço: 87329.50 | %R(9)=-75.32 | %R(2)=-45.12 | Candles: 9/9
[2025-12-24 10:30:15] [Bot4] INFO - [SINAL DE COMPRA] %R(9)=-79.50 cruzou acima de -80, %R(2)=-48.20 < -50 (filtro OK)
[2025-12-24 10:30:20] [Bot4] INFO - [POSIÇÃO LONG ABERTA] BTC/USDT0 @ 87329.50 | SL: 85583.21 (2.0%) | TP: 90822.68 (4.0%)
```


