# 🔧 Correção de Erros "Insufficient Account Health"

## 📋 Problema Identificado

Os bots estavam gerando erros de **"Insufficient account health"** (erro 2006), indicando que as ordens eram muito grandes para o saldo disponível.

## ✅ Solução Implementada

### 1. Redução Automática de Quantidade

O sistema agora detecta automaticamente erros de account health e reduz a quantidade das ordens:

- **Primeira redução**: Quantidade reduzida para **70%** do valor original
- **Segunda redução**: Quantidade reduzida para **49%** do valor original (70% × 70%)
- **Terceira redução**: Quantidade reduzida para **30%** do valor original (mínimo)
- **Mínimo**: A quantidade nunca fica abaixo de **30%** do valor original

### 2. Quantidade Reduzida por Padrão

Para evitar erros desde o início, a quantidade padrão foi reduzida:

- **Antes**: 250 USDC por ordem
- **Agora**: 200 USDC por ordem (modo padrão)
- **Modo Agressivo**: 150 USDC por ordem

### 3. Rastreamento de Erros

O sistema rastreia:
- Erros de account health por produto
- Multiplicadores de quantidade aplicados
- Produtos com muitos erros podem ser desabilitados

## 🎯 Como Funciona

### Detecção Automática

Quando ocorre um erro "Insufficient account health":

1. O sistema registra o erro para aquele produto específico
2. Após 3 erros consecutivos, reduz automaticamente a quantidade
3. Nas próximas tentativas, usa a quantidade reduzida
4. Os logs mostram quando a redução é aplicada

### Exemplo de Log

```
[SOL/USDT0] Erro de account health (3x). Quantidade será reduzida para 70% do valor original na próxima tentativa.
```

## 🔍 Verificar Erros

Execute o script de verificação de erros:

```bash
./verificar_erros.sh
```

Isso mostrará produtos com muitos erros de account health.

## 🔧 Solução Manual

Se os erros persistirem mesmo após a redução automática, você pode:

### Opção 1: Reduzir Quantidade Manualmente

Edite os arquivos dos bots (`bot1.py`, `bot2.py`, etc.):

```python
'quantity_per_order_usdc': 150,  # Reduzir de 200 para 150
```

### Opção 2: Aumentar o Saldo

Deposite mais fundos na conta para suportar ordens maiores.

### Opção 3: Reduzir Max Ordens

Edite os arquivos dos bots:

```python
'max_open_orders_per_product': 3,  # Reduzir de 5 para 3
```

## 📊 Produtos Configurados

Atualmente os bots estão configurados para operar em:

- **SOL/USDT0** (ID 5) - ✅ Funcionando
- **ZEC/USDT0** (ID 18) - ✅ Funcionando
- **FARTCoin/USDT0** (ID 22) - ✅ Funcionando

## 🚨 Produtos Desabilitados Automaticamente

Se um produto acumular **muitos erros** (20+ erros gerais), ele será automaticamente desabilitado. Para reativar, reinicie o bot.

## ✅ Status Atual

- ✅ Sistema de redução automática implementado
- ✅ Quantidade padrão reduzida para 200 USDC
- ✅ Rastreamento de erros ativo
- ✅ Logs informativos adicionados
- ✅ Produtos funcionais configurados (SOL, ZEC, FARTCoin)

## 🔄 Próximos Passos

1. **Monitorar logs**: Use `./watch_bot1.sh` para acompanhar o comportamento
2. **Verificar erros**: Use `./verificar_erros.sh` periodicamente
3. **Ajustar se necessário**: Se muitos erros persistirem, reduza a quantidade manualmente

