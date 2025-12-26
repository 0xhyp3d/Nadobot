# Cálculo de Taxas nos Bots

## ✅ Status: IMPLEMENTADO EM TODOS OS 3 BOTS

Todos os bots (Bot1, Bot2, Bot3) já estão calculando lucros/prejuízos **incluindo as taxas de trading**.

### Como funciona:

1. **Taxas configuradas:**
   - Maker Fee: **0.0035%** (0.000035) - Aplicada em todas as ordens POST_ONLY
   - Taker Fee: **0.001%** (0.00001) - Disponível para ordens market (futuras)

2. **Cálculo para cada trade:**
   - Lucro Bruto = (Preço Venda - Preço Compra) × Quantidade
   - Taxa Compra = Preço Compra × Quantidade × 0.0035%
   - Taxa Venda = Preço Venda × Quantidade × 0.0035%
   - Taxa Total = Taxa Compra + Taxa Venda
   - **Lucro Líquido = Lucro Bruto - Taxa Total**

3. **O que você verá nos logs:**
   ```
   [P/L DETALHADO] Lucro bruto: 10.5000 USDT | Taxas (compra+venda): 0.0735 USDT | Lucro líquido: 10.4265 USDT
   ```

4. **Total acumulado:**
   - O `total_profit` já está **líquido** (após deduzir todas as taxas)
   - Mostrado com 4 casas decimais para precisão

### Bots afetados:
- ✅ **Bot1** - Estratégia Original
- ✅ **Bot2** - Estratégia Customizável  
- ✅ **Bot3** - Grid Trading com Range

### Por que funciona em todos?
Todos os bots importam a classe `NadoFuturesBot` do arquivo `bot.py`, onde o cálculo de taxas foi implementado. Portanto, qualquer bot que use essa classe automaticamente terá o cálculo de taxas incluído.

### Exemplo prático:
Se você faz um trade:
- Compra: 100 BTC a $50,000 = $5,000,000
- Vende: 100 BTC a $50,500 = $5,050,000
- Lucro Bruto: $500
- Taxa Compra: $5,000,000 × 0.0035% = $175
- Taxa Venda: $5,050,000 × 0.0035% = $176.75
- Taxa Total: $351.75
- **Lucro Líquido: $500 - $351.75 = $148.25**

O bot mostrará: **Lucro líquido: 148.25 USDT**




