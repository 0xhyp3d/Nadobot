# ⚠️ IMPORTANTE: Múltiplos Bots Rodando Simultaneamente

## 1. Os 3 Bots Podem Rodar ao Mesmo Tempo?

**SIM**, tecnicamente os 3 bots podem rodar simultaneamente, mas há considerações importantes:

### ⚠️ Atenção - Mesma Conta/Subconta:
- Se os 3 bots usam a **mesma conta/subconta**, eles estarão **compartilhando o mesmo saldo**
- Eles competirão pelos mesmos fundos disponíveis
- Isso pode causar problemas de gerenciamento de risco

### ✅ Como Usar Múltiplos Bots Corretamente:
1. **Opção 1**: Usar subcontas diferentes para cada bot
   - Bot1 → subaccount: "bot1"
   - Bot2 → subaccount: "bot2"  
   - Bot3 → subaccount: "bot3"

2. **Opção 2**: Usar contas diferentes para cada bot
   - Cada bot com seu próprio `PRIVATE_KEY_BOT1`, `PRIVATE_KEY_BOT2`, `PRIVATE_KEY_BOT3`

3. **Opção 3**: Dividir o saldo manualmente entre os bots (não recomendado)

## 2. Ajuste Automático de Tamanho das Posições?

**NÃO**, atualmente os bots **NÃO ajustam automaticamente** o tamanho das posições quando você deposita mais dinheiro.

### Como Funciona Atualmente:
- O tamanho das ordens é **fixo** na configuração de cada bot:
  - Bot1: `amount_x18: to_pow_10(0.001, 18)` = 0.001 BTC por ordem
  - Bot2: `amount_x18: to_pow_10(0.001, 18)` = 0.001 BTC por ordem
  - Bot3: `quantity_per_order_usdc: 250` = 250 USDC por ordem

- O saldo é verificado apenas para garantir que há fundos suficientes (mínimo de 100 USDT)

### Para Ajustar o Tamanho das Posições:
Você precisa **editar manualmente** os arquivos de configuração:
- `bot1.py` - linha 27: `'amount_x18': to_pow_10(0.001, 18)` → ajustar quantidade
- `bot2.py` - linha 29: `'amount_x18': to_pow_10(0.001, 18)` → ajustar quantidade
- `bot3.py` - linha 33: `'quantity_per_order_usdc': 250` → ajustar quantidade

E depois **reiniciar os bots**:
```bash
./restart_bots.sh
```

### ⚠️ Recomendação:
Se você quer que os bots ajustem automaticamente baseado no saldo disponível, seria necessário modificar o código para:
1. Verificar o saldo disponível periodicamente
2. Calcular um tamanho de posição proporcional ao saldo
3. Ajustar as quantidades das ordens dinamicamente

Isso requer mudanças no código do `bot.py`.




