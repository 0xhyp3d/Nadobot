# ⚠️ IMPORTANTE: Sobre Desligar o Computador

## 🛑 O Que Acontece Quando Você Desliga?

**SIM, quando você desliga o computador, TUDO para de rodar!**

Isso significa:
- ❌ Todos os bots param de operar
- ❌ Não há mais trades sendo executados
- ❌ Você perde oportunidades enquanto o computador está desligado
- ⚠️ Ordens abertas podem permanecer na exchange (o bot tenta cancelar ao parar, mas se desligar abruptamente, pode não cancelar)

## ✅ O Que Fazer Antes de Desligar

### 1. Parar os Bots de Forma Segura

```bash
./stop_bots.sh
```

Isso garante que:
- Todos os bots sejam encerrados corretamente
- Ordens abertas sejam canceladas (se possível)
- Logs sejam salvos corretamente

### 2. Salvar o Projeto (Opcional mas Recomendado)

```bash
# Salvar tudo no Git
./salvar_projeto.sh

# Ou manualmente
git add .
git commit -m "Backup antes de desligar"
```

### 3. Fazer Backup do .env (Importante!)

```bash
# Criar backup da configuração (não está no Git por segurança)
cp .env .env.backup
```

## 🔄 Para Rodar Continuamente (24/7)

Se você quer que os bots continuem rodando mesmo quando você não estiver usando o computador:

### Opção Simples: Deixar Computador Ligado

1. Configure para não suspender
2. Use `screen` ou `tmux` para rodar os bots
3. Veja detalhes em: `docs/COMO_RODAR_CONTINUAMENTE.md`

**macOS - Prevenir Suspensão:**
```bash
# Em uma nova janela de terminal
caffeinate -d
```

### Melhor Opção: VPS/Servidor Cloud

Para rodar **realmente 24/7** sem manter seu computador ligado:

- Use um VPS (AWS, DigitalOcean, Linode, etc.)
- Configure os bots lá
- Mantenha rodando continuamente

Veja guia completo em: `docs/COMO_RODAR_CONTINUAMENTE.md`

## 📝 Resumo Rápido

| Situação | O Que Fazer |
|----------|-------------|
| **Vou desligar o computador** | Execute `./stop_bots.sh` antes |
| **Quero rodar 24/7 em casa** | Use `screen`/`tmux` + deixe computador ligado |
| **Quero rodar 24/7 profissionalmente** | Use VPS/Servidor Cloud |

## 🚨 Aviso Importante

**Trading automatizado requer monitoramento constante!**

Mesmo rodando 24/7:
- Monitore regularmente os logs
- Verifique se há erros
- Ajuste configurações conforme necessário
- Mantenha saldo suficiente para as ordens

---

📚 Para mais detalhes, consulte: `docs/COMO_RODAR_CONTINUAMENTE.md`




