# Correção: Bug no Cálculo de P/L

## 🐛 Problema Identificado

O código estava **reutilizando a mesma ordem de compra** para múltiplas ordens de venda, causando cálculo incorreto de lucro/prejuízo.

### Como acontecia:

1. Ordem de compra (BTC @ $87,000) é fechada → adicionada a `closed_orders`
2. Ordem de venda 1 (BTC @ $87,100) é fechada → emparelha com a ordem de compra, calcula P/L, mas **não remove a ordem de compra** da lista
3. Ordem de venda 2 (BTC @ $87,200) é fechada → **reutiliza a mesma ordem de compra**, calcula P/L novamente incorretamente
4. Resultado: O mesmo lucro/prejuízo é contabilizado múltiplas vezes!

### Impacto:

- **P/L inflado**: O lucro/prejuízo estava sendo contabilizado múltiplas vezes
- **Histórico incorreto**: Os arquivos JSON de histórico contêm dados incorretos
- **Total acumulado errado**: A soma dos lucros não corresponde ao lucro real da conta

## ✅ Correção Implementada

Agora o código **remove a ordem de compra** da lista `closed_orders` após usá-la para calcular o P/L, garantindo que cada ordem seja usada apenas uma vez.

### Mudança no código:

```python
# ANTES: Ordem de compra não era removida
for closed_order in reversed(self.closed_orders):
    if closed_order['side'] == 'buy' and ...:
        # Calcular P/L
        break  # ❌ Ordem não removida, pode ser reutilizada

# DEPOIS: Ordem de compra é removida após uso
matched_buy_order = None
for i, closed_order in enumerate(reversed(self.closed_orders)):
    idx = len(self.closed_orders) - 1 - i
    if closed_order['side'] == 'buy' and ...:
        matched_buy_order = (idx, closed_order)
        break

if matched_buy_order:
    idx, closed_order = matched_buy_order
    # Calcular P/L
    self.closed_orders.pop(idx)  # ✅ Remove após usar
```

## 🔄 Próximos Passos

**IMPORTANTE**: Como os históricos anteriores estão incorretos, você tem duas opções:

### Opção 1: Limpar Histórico e Começar do Zero (Recomendado)

```bash
# Fazer backup dos históricos atuais (caso queira analisar depois)
mkdir -p logs/backup_incorreto
cp logs/*_history.json logs/backup_incorreto/ 2>/dev/null || true

# Limpar históricos para recomeçar com cálculos corretos
rm logs/*_history.json
```

Depois disso, reinicie os bots:
```bash
./restart_bots.sh
```

### Opção 2: Manter Histórico e Aceitar que os Totais Acumulados Estão Incorretos

Se você quiser manter o histórico (para análise), os bots continuarão funcionando, mas:
- Os totais acumulados mostrarão valores incorretos (inflados)
- Novos trades serão calculados corretamente
- Você precisará recalcular manualmente os totais se necessário

## 📊 Valores Corretos Esperados

Após a correção, os valores de P/L devem estar muito mais próximos do lucro real da conta (~30 USD).

A diferença pode ser explicada por:
- Trades que não foram contabilizados
- Custos adicionais (funding rates, etc.)
- Timing de cálculo vs. execução real

## ✅ Taxas Aplicadas Corretamente

As taxas **estão sendo aplicadas corretamente**:
- Maker Fee: 0.0035% (0.000035) em ordens POST_ONLY
- Taker Fee: 0.001% (0.00001) - não usado atualmente (todas as ordens são POST_ONLY)
- Taxas deduzidas de: `(entry_value * maker_fee) + (exit_value * maker_fee)`

O problema era a **reutilização de ordens**, não o cálculo de taxas.


