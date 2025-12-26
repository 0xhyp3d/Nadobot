# 🤖 Bot de Trading de Futuros - Nado Protocol

Sistema de trading automatizado para a exchange **Nado Protocol** usando múltiplas estratégias de Grid Trading, Market Making e análise técnica.

## 📋 Índice

- [Características](#-características)
- [Estratégias Disponíveis](#-estratégias-disponíveis)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [Uso](#-uso)
- [Múltiplos Bots](#-múltiplos-bots)
- [Gerenciamento de Risco](#-gerenciamento-de-risco)
- [Logs e Monitoramento](#-logs-e-monitoramento)
- [Solução de Problemas](#-solução-de-problemas)
- [Avisos Importantes](#-avisos-importantes)

## ✨ Características

### Funcionalidades Principais

- ✅ **Múltiplas Estratégias**: Grid Trading, Market Making e Williams %R
- ✅ **Múltiplos Produtos**: Trading simultâneo em BTC, ETH e WETH
- ✅ **Proteção Cloudflare**: Bypass automático de desafios do Cloudflare
- ✅ **Gerenciamento de Erros**: Desabilitação automática de produtos com problemas
- ✅ **Ajuste Dinâmico**: Redução automática de quantidade em caso de "account health" insuficiente
- ✅ **Cálculo de P/L Detalhado**: Lucro líquido considerando todas as taxas
- ✅ **Logs Completos**: Histórico detalhado de todas as operações
- ✅ **Suporte a Múltiplos Bots**: Execute vários bots simultaneamente

### Tecnologias

- **Python 3.8+**
- **Nado Protocol SDK**: SDK oficial da exchange
- **cloudscraper**: Bypass de proteção Cloudflare
- **python-dotenv**: Gerenciamento de variáveis de ambiente

## 🎯 Estratégias Disponíveis

### Bot 1 - Grid Trading / Market Making (Padrão)
- Estratégia conservadora de market making
- Grid spacing: 0.05%
- Máximo de 5 ordens por produto
- 3 níveis de grid

### Bot 2 - Grid Trading Customizável
- Mesma base do Bot 1, com parâmetros totalmente customizáveis
- Ideal para testes de diferentes configurações

### Bot 3 - Grid Trading com Range
- Grid Trading com range superior e inferior configurável
- Suporte a grids lineares e geométricos

### Bot 4 - Williams %R Strategy
- Estratégia baseada em indicador técnico Larry Williams %R
- Períodos: %R(9) e %R(2)
- Timeframe: 5 minutos
- Sinais de entrada baseados em sobrecompra/sobrevenda

## 📦 Instalação

### 1. Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Carteira Ethereum com chave privada

### 2. Clonar/Download do Repositório

```bash
git clone <url-do-repositorio>
cd Bot
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente

Copie o arquivo de exemplo e preencha com suas credenciais:

```bash
cp .env.example .env
```

Edite o arquivo `.env`:

```env
PRIVATE_KEY=0xseus_64_caracteres_hexadecimais_aqui
NADO_NETWORK=mainnet
```

**⚠️ IMPORTANTE**: 
- Nunca compartilhe sua chave privada!
- A chave deve começar com `0x` seguido de 64 caracteres hexadecimais
- Use `mainnet` para produção ou `devnet` para testes

## ⚙️ Configuração

### Configuração Básica

Os bots são configurados através dos arquivos `bot1.py`, `bot2.py`, `bot3.py`, e `bot4.py`. Cada arquivo contém um dicionário `config` com os parâmetros de trading.

### Parâmetros Principais

```python
config = {
    'subaccount_name': "default",           # Nome da subconta
    'leverage': 40,                         # Alavancagem (40x)
    'products': {
        2: {'name': 'BTC/USDT0'},   # BTC-PERP (product_id 2) - Perpétuo
        4: {'name': 'ETH/USDT0'},   # ETH-PERP (product_id 4) - Perpétuo
        3: {'name': 'WETH/USDT0'},  # WETH/USDT0 (product_id 3) - Spot
    },
    'quantity_per_order_usdc': 200,        # Quantidade por ordem em USDC
    'grid_spacing': 0.05,                  # Espaçamento do grid (0.05%)
    'max_open_orders_per_product': 5,      # Máximo de ordens por produto
    'stop_loss_pct': 0.02,                 # Stop Loss (2%)
    'take_profit_pct': 0.04,               # Take Profit (4%)
    'min_balance': 100,                    # Saldo mínimo em USDT
    'grid_levels': 3,                      # Níveis de grid acima/abaixo
    'order_expiration': 3600,              # Expiração das ordens (segundos)
}
```

### Product IDs

Para descobrir os Product IDs corretos:
1. Consulte a documentação da Nado Protocol
2. Use o script de teste: `python testar_produtos.py`
3. Verifique os logs para erros de product_id inválido

### Configuração para Múltiplos Bots

Se você usar múltiplos bots simultaneamente, você pode:

**Opção 1**: Arquivos `.env` separados
```bash
.env.bot1  # Para Bot1
.env.bot2  # Para Bot2
```

**Opção 2**: Variáveis diferentes no mesmo `.env`
```env
PRIVATE_KEY_BOT1=0x...
PRIVATE_KEY_BOT2=0x...
```

## 🚀 Uso

### Executar um Bot Individual

```bash
# Bot 1
python3 bot1.py

# Bot 2
python3 bot2.py

# Bot 3
python3 bot3.py

# Bot 4 (Williams %R)
python3 bot4.py
```

### Executar Todos os Bots

```bash
# Iniciar todos
./start_all_bots.sh

# Parar todos
./stop_bots.sh

# Reiniciar todos
./restart_bots.sh
```

### Executar em Background

Os scripts `start_all_bots.sh` e `run_bots_background.sh` executam os bots em background. Os logs são salvos em `logs/`.

### Encerrar um Bot

Pressione `Ctrl+C` para encerrar de forma segura. O bot cancelará todas as ordens abertas antes de encerrar.

## 🤖 Múltiplos Bots

### Executando Múltiplos Bots Simultaneamente

**⚠️ ATENÇÃO**: Se múltiplos bots usam a mesma conta/subconta:
- Eles compartilharão o mesmo saldo
- Podem competir pelos mesmos fundos
- Risco de conflitos de gerenciamento de risco

**✅ Recomendações**:

1. **Usar Subcontas Diferentes**:
   ```python
   # Bot 1
   'subaccount_name': "bot1"
   
   # Bot 2
   'subaccount_name': "bot2"
   ```

2. **Usar Contas Diferentes**:
   - Cada bot com sua própria `PRIVATE_KEY`

3. **Dividir Produtos** (opcional):
   - Cada bot pode operar em produtos diferentes se necessário



## 🛡️ Gerenciamento de Risco

### Proteções Implementadas

1. **Stop Loss**: 2% (configurável)
2. **Take Profit**: 4% com R:R 2:1 (configurável)
3. **Limite de Ordens**: Máximo de ordens abertas por produto
4. **Saldo Mínimo**: Verificação de saldo antes de operar
5. **Ajuste Dinâmico**: Redução automática de quantidade em caso de "account health" insuficiente
6. **Desabilitação Automática**: Produtos com muitos erros são desabilitados automaticamente

### Taxas

O bot calcula o lucro líquido deduzindo as taxas:
- **Maker Fee**: 0.0035% (0.000035) - Aplicada em ordens POST_ONLY
- **Taker Fee**: 0.001% (0.00001) - Para ordens market (futuras)

O P/L mostrado nos logs já está **líquido** (após todas as taxas).

### Produtos Desabilitados Automaticamente

O bot desabilita automaticamente produtos que:
- Apresentam 5 erros consecutivos do Cloudflare (temporário - 10 minutos)
- Apresentam "Insufficient account health" repetidamente (reduz quantidade)
- Apresentam 10 erros gerais consecutivos (permanente até reiniciar)

## 📊 Logs e Monitoramento

### Ver Logs em Tempo Real

```bash
# Bot 1
./watch_bot1.sh
# ou
tail -f logs/bot1.log

# Bot 2
./watch_bot2.sh

# Bot 3
./watch_bot3.sh

# Bot 4
./watch_bot4.sh
```

### Verificar Erros

```bash
# Resumo de erros
./verificar_erros.sh

# Últimos erros
./ver_ultimos_erros.sh
```

### Histórico de Trades

Os trades são salvos em `logs/Bot*_history.json` com informações detalhadas:
- Timestamp
- Product ID e nome
- Preço de entrada e saída
- Quantidade
- Lucro bruto, taxas e lucro líquido
- Alavancagem

### Calcular Resultado Total

```bash
python calcular_resultado_total.py
```

## 🔧 Solução de Problemas

### Erro: "Chave privada inválida"

- Verifique se a chave começa com `0x`
- Verifique se tem exatamente 64 caracteres hexadecimais após `0x`
- Verifique se não há espaços extras no arquivo `.env`

### Erro: "Cloudflare Challenge"

O bot usa `cloudscraper` para contornar automaticamente. Se persistir:
- O produto será temporariamente desabilitado (10 minutos)
- Verifique os logs para detalhes
- Considere usar outro produto

### Erro: "Insufficient account health"

- O bot reduzirá automaticamente a quantidade em 30%
- Considere aumentar o saldo disponível
- Ou reduza `quantity_per_order_usdc` na configuração

### Produto não está operando

- Verifique se o Product ID está correto
- Verifique os logs para erros
- O produto pode ter sido desabilitado automaticamente
- Reinicie o bot para reativar produtos permanentemente desabilitados

### Bots não iniciando

- Verifique se o arquivo `.env` existe e está configurado
- Verifique se as dependências estão instaladas: `pip install -r requirements.txt`
- Verifique os logs: `tail -f logs/bot*.log`

## ⚠️ Avisos Importantes

### ⚠️ Riscos do Trading

- **Trading envolve riscos significativos**. Você pode perder todo o seu capital.
- **Este bot é para fins educacionais**. Use por sua conta e risco.
- **Sempre teste em devnet primeiro** antes de usar em produção.
- **Comece com valores pequenos** até entender o comportamento do bot.
- **Monitore regularmente** o desempenho e ajuste conforme necessário.

### 🔒 Segurança

- **NUNCA compartilhe sua chave privada**
- **NUNCA commite arquivos `.env` no Git**
- **Mantenha backups seguros** das configurações
- **Use subcontas diferentes** para diferentes estratégias
- **Revise o código** antes de executar em produção

### 📝 Limitações

- O bot não ajusta automaticamente o tamanho das posições quando você deposita mais dinheiro
- Você precisa editar manualmente a configuração e reiniciar
- Produtos com muitos erros são desabilitados automaticamente
- O bot precisa de pelo menos 45 minutos para o Bot4 (Williams %R) começar a gerar sinais

## 📚 Documentação Adicional

Consulte a pasta `docs/` para documentação detalhada sobre:
- Configuração de produtos específicos
- Correções e melhorias implementadas
- Estratégias detalhadas
- Guias de troubleshooting

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:
1. Faça um fork do repositório
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Abra um Pull Request

## 📄 Licença

[Adicione a licença do seu projeto aqui]

## 🙏 Agradecimentos

- [Nado Protocol](https://nadohq.github.io/nado-python-sdk/) pelo SDK oficial
- Comunidade de desenvolvedores de trading bots

## 📞 Suporte

Para problemas ou dúvidas:
1. Consulte a documentação em `docs/`
2. Verifique os logs em `logs/`
3. Abra uma issue no repositório

---

**⚠️ Lembre-se**: Trading envolve riscos. Use por sua conta e risco.
