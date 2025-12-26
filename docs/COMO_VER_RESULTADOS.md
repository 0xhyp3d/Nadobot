# Como Ver os Resultados Totais dos Bots

## ⚠️ Situação Atual

Os bots foram reiniciados recentemente, então os logs atuais não contêm o histórico completo desde ontem. 

**Solução Implementada**: Agora os bots salvam automaticamente cada trade em arquivos JSON de histórico (`logs/bot1_history.json`, `logs/bot2_history.json`, `logs/bot3_history.json`), então **futuros trades não serão perdidos** quando os bots reiniciarem.

## 📊 Como Ver os Resultados

### Opção 1: Usar o Script de Análise (Recomendado)

Execute no terminal:

```bash
cd /Users/igorbirni/Bot
python3 calcular_resultado_total.py
```

Este script:
- ✅ Procura primeiro nos arquivos JSON de histórico (mais confiável)
- ✅ Se não encontrar, analisa os logs como fallback
- ✅ Mostra ranking de rentabilidade
- ✅ Exibe totais históricos desde o início

### Opção 2: Ver os Arquivos JSON Diretamente

Os arquivos de histórico estão em:
- `logs/bot1_history.json`
- `logs/bot2_history.json`
- `logs/bot3_history.json`

Cada arquivo contém:
```json
{
  "trades": [
    {
      "timestamp": "2025-12-24T10:30:00",
      "product_name": "BTC/USDT0",
      "entry_price": 87000.0,
      "exit_price": 87100.0,
      "amount": 0.01,
      "gross_profit": 1.0,
      "total_fees": 0.0306,
      "net_profit": 0.9694,
      "leverage": 40
    }
  ],
  "total_trades": 1,
  "total_profit": 0.9694,
  "created_at": "2025-12-24T08:00:00",
  "last_updated": "2025-12-24T10:30:00"
}
```

## 🔄 Para Recuperar o Histórico Perdido

Se você tiver backups dos logs antigos de ontem, você pode:

1. Copiar os logs antigos para `logs/bot1.log.old`, `logs/bot2.log.old`, etc.
2. O script `calcular_resultado_total.py` pode ser modificado para ler esses arquivos também

Ou, se você souber os valores totais de ontem, pode criar manualmente os arquivos JSON de histórico com os trades antigos.

## 📝 Próximos Passos

Agora que o sistema de persistência está implementado:
- ✅ **Novos trades serão salvos automaticamente** no arquivo JSON
- ✅ **Mesmo se os bots reiniciarem, o histórico será preservado**
- ✅ **O script de análise sempre mostrará o total histórico correto**

## 🚀 Como Funciona Agora

1. **Quando um bot faz um trade**, ele automaticamente:
   - Calcula o lucro/prejuízo (incluindo taxas)
   - Salva no arquivo JSON de histórico
   - Mostra no log

2. **Quando um bot reinicia**, ele automaticamente:
   - Carrega o histórico do arquivo JSON
   - Continua somando a partir do valor anterior
   - Não perde o histórico acumulado

3. **Para ver os resultados**, execute:
   ```bash
   python3 calcular_resultado_total.py
   ```


