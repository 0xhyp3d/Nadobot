# Correção: User-Agent de Navegador Real para Evitar Bloqueio do Cloudflare

## 🐛 Problema Identificado

O Cloudflare estava bloqueando as requisições dos bots com o erro "Just a moment..." porque o User-Agent padrão das requisições HTTP identificava o bot como um script automatizado.

## ✅ Solução Implementada

Foi implementado um sistema para adicionar um User-Agent de navegador real (Chrome) em todas as requisições HTTP:

1. **Monkey Patch no requests.Session**: Adiciona automaticamente o User-Agent do Chrome a todas as requisições feitas através da biblioteca `requests`
2. **Tentativa de configuração direta**: Tenta configurar o User-Agent diretamente no cliente HTTP subjacente do SDK da Nado (se disponível)

### User-Agent Utilizado

```
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
```

Este é o User-Agent do Google Chrome 120, um dos navegadores mais comuns, o que reduz significativamente a chance de bloqueio pelo Cloudflare.

## 📊 Como Funciona

### Monkey Patch (Principal)

```python
import requests

# Salvar método original
original_request = requests.Session.request

# Criar novo método que adiciona User-Agent
def request_with_user_agent(self, method, url, **kwargs):
    if 'headers' not in kwargs:
        kwargs['headers'] = {}
    if 'User-Agent' not in kwargs['headers']:
        kwargs['headers']['User-Agent'] = CHROME_USER_AGENT
    return original_request(self, method, url, **kwargs)

# Aplicar o patch
requests.Session.request = request_with_user_agent
```

Isso garante que **todas** as requisições HTTP feitas através do `requests` (que é usado internamente pelo SDK da Nado) terão o User-Agent do Chrome.

### Configuração Direta no Cliente (Complementar)

Após criar o cliente Nado, o código tenta configurar o User-Agent diretamente no cliente HTTP subjacente (se disponível). Se isso não for possível, o monkey patch ainda garante que funcionará.

## 🔄 Próximos Passos

**IMPORTANTE**: Reinicie todos os bots para aplicar a correção:

```bash
./restart_bots.sh
```

## 📝 Observações

- O User-Agent é adicionado **antes** de importar o SDK da Nado, garantindo que todas as requisições sejam afetadas
- Se o SDK da Nado usar uma biblioteca HTTP diferente de `requests` no futuro, será necessário ajustar o código
- O User-Agent usado é do Chrome 120 (última versão estável), que é amplamente aceito
- Esta solução funciona em conjunto com o sistema de desabilitação automática de produtos com erros do Cloudflare

## 🎯 Resultado Esperado

- Menos bloqueios do Cloudflare
- Requisições mais bem-sucedidas para FARTCoin e ZEC
- Bots operando de forma mais estável
- Redução significativa nos erros "Just a moment..."


