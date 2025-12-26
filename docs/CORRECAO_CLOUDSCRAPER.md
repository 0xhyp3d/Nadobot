# Correção: Integração do cloudscraper para Contornar Cloudflare

## 🐛 Problema Identificado

O Cloudflare estava bloqueando as requisições dos bots com desafios JavaScript ("Just a moment..."), mesmo com User-Agent de navegador real. Isso acontece porque o Cloudflare detecta que as requisições não estão resolvendo os desafios JavaScript adequadamente.

## ✅ Solução Implementada: cloudscraper

Foi implementada uma solução robusta usando a biblioteca `cloudscraper`, que é especializada em resolver automaticamente os desafios JavaScript do Cloudflare.

### Como Funciona

1. **Substituição de `requests.Session`**: A classe `requests.Session` é substituída por `CloudflareSession`, que usa `cloudscraper.create_scraper()` internamente
2. **Compatibilidade Total**: A nova classe mantém total compatibilidade com `requests.Session`, então o SDK da Nado funciona sem modificações
3. **Resolução Automática**: O cloudscraper resolve automaticamente os desafios JavaScript do Cloudflare, incluindo:
   - Resolução de desafios "Just a moment..."
   - Simulação de navegador real (Chrome)
   - Gerenciamento de cookies e tokens do Cloudflare

### Implementação

```python
class CloudflareSession(requests.Session):
    """Session que usa cloudscraper para contornar Cloudflare"""
    def __init__(self, *args, **kwargs):
        # Criar sessão cloudscraper
        self._cloudscraper = cloudscraper.create_scraper(
            browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
        )
        # Copiar atributos para compatibilidade
    
    def request(self, method, url, **kwargs):
        # Usar cloudscraper que resolve desafios automaticamente
        return self._cloudscraper.request(method, url, **kwargs)
```

### Fallback

Se o `cloudscraper` não estiver instalado, o código faz fallback para `requests` normal com User-Agent do Chrome.

## 📦 Instalação

O `cloudscraper` foi adicionado ao `requirements.txt`. Para instalar:

```bash
pip install -r requirements.txt
```

Ou diretamente:

```bash
pip install cloudscraper>=1.2.71
```

## 🔄 Próximos Passos

**IMPORTANTE**: Instale o cloudscraper e reinicie todos os bots:

```bash
pip install cloudscraper>=1.2.71
./restart_bots.sh
```

## 📝 Observações

- **Compatibilidade**: A solução é totalmente compatível com o SDK da Nado, não requer modificações no código do SDK
- **Performance**: O cloudscraper pode adicionar um pequeno delay inicial (alguns segundos) ao resolver o primeiro desafio do Cloudflare, mas depois funciona normalmente
- **Manutenção**: O cloudscraper é atualizado regularmente para lidar com mudanças no Cloudflare
- **Fallback Automático**: Se o cloudscraper não estiver instalado, o código usa requests normal com User-Agent

## 🎯 Resultado Esperado

- ✅ Requisições passam pelos desafios do Cloudflare automaticamente
- ✅ Menos ou nenhum erro "Just a moment..."
- ✅ FARTCoin e ZEC funcionando normalmente
- ✅ Bots operando de forma estável

## 🔍 Detecção

Ao iniciar o bot, você verá uma das seguintes mensagens:

- `[CLOUDFLARE] cloudscraper ativado - proteção contra desafios do Cloudflare habilitada` (se cloudscraper está instalado)
- `[CLOUDFLARE] cloudscraper não disponível - usando requests com User-Agent padrão` (se cloudscraper não está instalado)

Certifique-se de instalar o cloudscraper para obter a proteção completa contra Cloudflare!


