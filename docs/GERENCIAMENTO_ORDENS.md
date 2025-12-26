# ⚠️ IMPORTANTE: Gerenciamento de Ordens Antigas

## Situação Atual: Ordens Vão Acumulando

Atualmente, o bot **NÃO cancela automaticamente** ordens que ficaram "pra trás" ou muito longe do preço de mercado.

### Como Funciona Hoje:

1. **Expiração automática**: As ordens expiram automaticamente após **1 hora** (3600 segundos) através do timestamp de expiração enviado para a exchange.

2. **Limite de ordens**: O bot verifica se há espaço para novas ordens baseado em `max_open_orders_per_product`, mas **não cancela** ordens antigas para abrir espaço.

3. **Cancelamento apenas em Stop Loss**: Ordens só são canceladas quando:
   - Stop Loss é acionado
   - Bot é encerrado (fecha todas as ordens)
   - Ordem expira (após 1 hora)

4. **Sem cancelamento por distância do preço**: Ordens que ficam muito longe do preço de mercado continuam ativas até expirarem ou serem executadas.

### Problema Potencial:

Se o preço se move muito, as ordens podem ficar:
- Muito longe do preço atual (pouca chance de execução)
- Acumulando e ocupando espaço de novas ordens
- Bloqueando capital desnecessariamente

### Soluções Possíveis:

#### Opção 1: Cancelar ordens muito antigas (ex: > 30 minutos)
#### Opção 2: Cancelar ordens muito longe do preço (ex: > 1% do preço de mercado)
#### Opção 3: Cancelar e recriar ordens periodicamente para manter próximas ao preço

Quer que eu implemente alguma dessas soluções?




