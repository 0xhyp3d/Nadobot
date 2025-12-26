# 🔥 Modo Agressivo ATIVADO

## ✅ Status: Modo Agressivo Ativado em Todos os Bots

O modo agressivo foi ativado adicionando `AGGRESSIVE_MODE=true` no arquivo `.env`.

## 🔄 Próximo Passo: Reiniciar os Bots

**IMPORTANTE**: Você precisa reiniciar todos os bots para aplicar a mudança:

```bash
./restart_bots.sh
```

## 📊 Configurações do Modo Agressivo Ativo

Com o modo agressivo ativado, os bots estarão usando:

- **Grid spacing**: 0.03% (40% mais apertado que o padrão)
- **Max ordens**: 8 por produto (60% mais que o padrão)
- **Grid levels**: 5 níveis (67% mais que o padrão)
- **Quantidade**: 150 USDC por ordem (otimizado para evitar account health)

## 🔍 Verificar se Está Funcionando

Após reiniciar os bots, verifique os logs:

```bash
./watch_bot1.sh
```

Você deve ver:
```
🔥 MODO AGRESSIVO ATIVADO - Parâmetros otimizados para maior rentabilidade e volume
  - Grid spacing: 0.03% (padrão: 0.05%)
  - Max ordens: 8 (padrão: 5)
  - Grid levels: 5 (padrão: 3)
  - Quantidade por ordem: 150 USDC
```

## 🔄 Como Desativar (Voltar ao Modo Padrão)

Se quiser voltar ao modo padrão:

1. Edite o arquivo `.env`:
   ```bash
   AGGRESSIVE_MODE=false
   ```

2. Reinicie os bots:
   ```bash
   ./restart_bots.sh
   ```

## ⚠️ Lembrete

- O modo agressivo cria mais ordens simultaneamente
- Certifique-se de ter saldo suficiente
- Monitore os erros usando: `./verificar_erros.sh`

