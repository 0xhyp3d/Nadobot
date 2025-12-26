# Atualização: Produtos Funcionais Configurados

## 📊 Produtos Atualizados

Todos os bots foram atualizados para usar **apenas os produtos que funcionam corretamente**, identificados através de testes:

### ✅ Produtos Funcionais Configurados:

| Product ID | Nome | Status |
|------------|------|--------|
| 5 | SOL/USDT0 | ✅ Funcionando |
| 18 | ZEC/USDT0 | ✅ Funcionando |
| 22 | FARTCoin/USDT0 | ✅ Funcionando |

### ❌ Produtos Removidos (com erros):

- **BTC/USDT0 (ID 2)**: Removido devido a erros intermitentes do Cloudflare Challenge

## 🔄 Mudanças Aplicadas

1. **bot1.py**: Atualizado para usar SOL, ZEC e FARTCoin
2. **bot2.py**: Atualizado para usar SOL, ZEC e FARTCoin
3. **bot3.py**: Atualizado para usar SOL, ZEC e FARTCoin
4. **bot4.py**: Atualizado para usar SOL, ZEC e FARTCoin (antes só tinha BTC)
5. **bot.py**: Adicionado `size_increment` para SOL (ID 5)

## ⚙️ Configuração Técnica

### size_increment por Produto:

- **SOL (ID 5)**: `0.01 SOL` = 10000000000000000 (x18) - valor estimado
- **ZEC (ID 18)**: `0.001 ZEC` = 1000000000000000 (x18)
- **FARTCoin (ID 22)**: `0.001 FARTCoin` = 1000000000000000 (x18)

⚠️ **Nota**: O `size_increment` do SOL foi estimado. Se houver erros de ordem relacionados a `size_increment`, verifique o erro na API e ajuste o valor no código.

## 🚀 Próximos Passos

**IMPORTANTE**: Reinicie todos os bots para aplicar as mudanças:

```bash
./restart_bots.sh
```

Ou manualmente:
```bash
./stop_bots.sh
sleep 3
./start_all_bots.sh
```

## 📝 Observações

- Os bots agora operam em **3 produtos simultaneamente**: SOL, ZEC e FARTCoin
- O sistema de desabilitação automática por Cloudflare continua ativo para gerenciar erros intermitentes
- Se um produto começar a dar muitos erros, ele será temporariamente desabilitado por 10 minutos
- Os logs mostrarão qual produto está sendo negociado: `[SOL/USDT0]`, `[ZEC/USDT0]`, ou `[FARTCoin/USDT0]`

## 🔍 Monitoramento

Monitore os logs para verificar se todos os produtos estão funcionando:

```bash
# Ver logs do Bot1
./watch_bot1.sh

# Ver logs do Bot2
./watch_bot2.sh

# Ver logs do Bot3
./watch_bot3.sh

# Ver logs do Bot4
./watch_bot4.sh
```

Se algum produto começar a dar erro, ele será automaticamente desabilitado temporariamente pelo sistema de proteção contra Cloudflare.

