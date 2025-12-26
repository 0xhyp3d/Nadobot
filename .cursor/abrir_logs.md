# 📺 Como Abrir Logs dos Bots no Cursor

## Método 1: Dividir Terminal Manualmente (Recomendado)

1. **Abra um terminal integrado no Cursor:**
   - Menu: `Terminal` > `New Terminal`
   - Ou atalho: `` Ctrl+` `` (Ctrl + crase)

2. **Divida o terminal em 4 painéis:**
   - Pressione `` Ctrl+Shift+` `` (ou `Cmd+Shift+"` no Mac) para dividir
   - Repita 3 vezes para ter 4 painéis

3. **Execute em cada painel (nesta ordem):**
   ```bash
   # Painel 1
   tail -f logs/Bot1.log
   
   # Painel 2
   tail -f logs/Bot2.log
   
   # Painel 3
   tail -f logs/Bot3.log
   
   # Painel 4
   tail -f logs/Bot4.log
   ```

## Método 2: Usar Script de Comandos

Execute no terminal integrado do Cursor:

```bash
cd /Users/igorbirni/Bot
tail -f logs/Bot1.log &
tail -f logs/Bot2.log &
tail -f logs/Bot3.log &
tail -f logs/Bot4.log &
```

Depois divida o terminal para ver cada um em um painel separado.

## Método 3: Criar Tarefas do Cursor

Crie um arquivo `.vscode/tasks.json` com tarefas para cada bot.


