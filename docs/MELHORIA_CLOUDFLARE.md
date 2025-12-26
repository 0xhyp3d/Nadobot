# Melhoria: Tratamento de Erros do Cloudflare Challenge

## 🎯 Objetivo

Melhorar a resiliência dos bots contra bloqueios temporários do Cloudflare Challenge da API da Nado.

## ✅ Melhorias Implementadas

### 1. Detecção Específica de Erros do Cloudflare

Foi adicionada a função `is_cloudflare_error()` na classe `NadoFuturesBot` que detecta especificamente erros do Cloudflare Challenge:

```python
def is_cloudflare_error(self, error: Exception) -> bool:
    """Verifica se o erro é um bloqueio do Cloudflare Challenge"""
    if isinstance(error, BadStatusCodeException):
        error_str = str(error)
        # Cloudflare retorna HTML com "Just a moment..." ou "challenge-platform"
        return "Just a moment" in error_str or "challenge-platform" in error_str or "<!DOCTYPE html>" in error_str
    return False
```

### 2. Retry com Backoff Exponencial

- **Antes**: Os bots tentavam novamente imediatamente após erros
- **Agora**: 
  - Aguardam 15 segundos após primeiro erro do Cloudflare
  - Aumentam o delay progressivamente: 10 segundos × número de erros consecutivos
  - Máximo de 60 segundos (Bot1, Bot2, Bot3) ou 90 segundos (Bot4)
  - Reset do contador quando operação é bem-sucedida

### 3. Tratamento Específico por Operação

#### Bot1, Bot2, Bot3 (`bot.py`)

- **Obter preços**: Se todos os produtos falharem com Cloudflare, aumenta delay
- **Atualizar ordens**: Se falhar com Cloudflare, pula iteração após delay
- **Gerenciar posições**: Continua mesmo com erro do Cloudflare
- **Criar ordens**: Continua mesmo com erro do Cloudflare

#### Bot4 (`bot4.py`)

- **Obter preços**: Aplica delay específico por produto
- **Loop principal**: Aplica backoff exponencial para erros críticos

### 4. Contador de Erros Consecutivos

- Rastreia erros consecutivos do Cloudflare
- Após 5 erros consecutivos, aumenta significativamente o delay
- Reset automático quando operação é bem-sucedida

## 📊 Comportamento Esperado

### Cenário 1: Erro Isolado
1. Bot tenta obter preço → Cloudflare Challenge
2. Bot aguarda 15 segundos
3. Bot tenta novamente → Sucesso
4. Bot continua normalmente

### Cenário 2: Múltiplos Erros Consecutivos
1. Bot tenta obter preço → Cloudflare Challenge (delay: 15s)
2. Bot tenta novamente → Cloudflare Challenge (delay: 30s)
3. Bot tenta novamente → Cloudflare Challenge (delay: 45s)
4. Bot tenta novamente → Cloudflare Challenge (delay: 60s)
5. Bot tenta novamente → Sucesso → Reset contador

### Cenário 3: Todos os Produtos Bloqueados
1. Bot tenta obter preços de todos os produtos → Todos falham com Cloudflare
2. Bot detecta que todos falharam
3. Bot aumenta delay antes de próxima tentativa
4. Bot continua loop após delay

## 🔄 Como Aplicar

As melhorias já estão implementadas no código. **Reinicie os bots** para aplicar:

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

1. **Erros temporários**: O Cloudflare Challenge é temporário e geralmente resolve em alguns minutos
2. **Logs melhorados**: Os logs agora mostram quando erros do Cloudflare são detectados e o delay aplicado
3. **Operação não bloqueada**: Os bots não param completamente, apenas aguardam antes de tentar novamente
4. **Produtos independentes**: Se um produto estiver bloqueado, os outros continuam funcionando

## ⚙️ Parâmetros Ajustáveis

Se necessário, você pode ajustar os seguintes parâmetros em `bot.py`:

- `max_consecutive_errors = 5`: Número de erros antes de aumentar delay significativamente
- `time.sleep(15)`: Delay inicial após erro do Cloudflare
- `min(60, 10 * consecutive_errors)`: Delay máximo e fórmula de backoff

## 🔍 Monitoramento

Para verificar se os bots estão lidando bem com os erros do Cloudflare:

```bash
# Ver logs em tempo real
tail -f logs/bot1.log | grep -i cloudflare
tail -f logs/bot2.log | grep -i cloudflare
tail -f logs/bot3.log | grep -i cloudflare
tail -f logs/bot4.log | grep -i cloudflare
```

Você deve ver mensagens como:
- `"Cloudflare Challenge detectado. Aguardando X segundos..."`
- `"Cloudflare Challenge ao obter preço para..."`


