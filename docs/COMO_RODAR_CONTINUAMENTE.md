# 🔄 Como Manter os Bots Rodando Continuamente

## ⚠️ Importante: Processos e Desligamento do Computador

**SIM, quando você desliga o computador, todos os processos param!**

Isso significa que:
- ❌ Os bots param de operar
- ❌ As ordens abertas podem não ser canceladas automaticamente
- ❌ Você perde a oportunidade de fazer trades enquanto o computador está desligado

## 🎯 Soluções para Rodar Continuamente

### Opção 1: Usar `screen` ou `tmux` (Mais Simples)

Permite manter os processos rodando mesmo se você fechar o terminal.

#### Instalação

```bash
# macOS (com Homebrew)
brew install screen
# ou
brew install tmux

# Linux (Ubuntu/Debian)
sudo apt-get install screen
# ou
sudo apt-get install tmux
```

#### Usando Screen

```bash
# Criar uma sessão screen chamada "bots"
screen -S bots

# Dentro da sessão, iniciar os bots
./start_all_bots.sh

# Detach (sair sem parar): Ctrl+A depois D

# Reconectar depois
screen -r bots

# Listar sessões
screen -ls

# Matar sessão
screen -X -S bots quit
```

#### Usando Tmux

```bash
# Criar nova sessão
tmux new -s bots

# Dentro da sessão, iniciar os bots
./start_all_bots.sh

# Detach: Ctrl+B depois D

# Reconectar
tmux attach -t bots

# Listar sessões
tmux ls

# Matar sessão
tmux kill-session -t bots
```

**⚠️ LIMITAÇÃO**: Mesmo com screen/tmux, se você **desligar o computador**, os processos param.

### Opção 2: Usar `nohup` (Básico)

Executa processos em background que continuam mesmo se você fechar o terminal.

```bash
# Executar em background com nohup
nohup ./start_all_bots.sh > bots_output.log 2>&1 &

# Ver processos
jobs

# Parar processos
pkill -f "bot[1-4].py"
```

**⚠️ LIMITAÇÃO**: Ainda para quando você desliga o computador.

### Opção 3: Serviços do Sistema (Melhor para Servidores)

#### macOS (com launchd)

Criar arquivo `~/Library/LaunchAgents/com.nadobots.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.nadobots</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/igorbirni/Bot/bot1.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/igorbirni/Bot</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/Users/igorbirni/Bot/logs/bot1_service.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/igorbirni/Bot/logs/bot1_service_error.log</string>
</dict>
</plist>
```

Carregar serviço:
```bash
launchctl load ~/Library/LaunchAgents/com.nadobots.plist
launchctl start com.nadobots
```

#### Linux (systemd)

Criar arquivo `/etc/systemd/system/nado-bots.service`:

```ini
[Unit]
Description=Nado Trading Bots
After=network.target

[Service]
Type=simple
User=seu_usuario
WorkingDirectory=/caminho/para/Bot
ExecStart=/usr/bin/python3 /caminho/para/Bot/bot1.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Ativar serviço:
```bash
sudo systemctl enable nado-bots.service
sudo systemctl start nado-bots.service
sudo systemctl status nado-bots.service
```

**⚠️ LIMITAÇÃO**: Mesmo assim, desligar o computador para os serviços (a menos que seja um servidor que fique sempre ligado).

### Opção 4: Servidor/VPS/Cloud (Melhor Solução)

Para rodar **24/7 sem desligar**, a melhor opção é usar:

1. **VPS (Virtual Private Server)**
   - AWS EC2
   - DigitalOcean
   - Linode
   - Vultr
   - Contabo
   - Outras opções

2. **Servidor Dedicado**
   - Mantenha um computador sempre ligado em casa
   - Ou alugue um servidor dedicado

3. **Raspberry Pi** (Solução Barata)
   - Mantém rodando 24/7
   - Consome pouca energia
   - Custo baixo

#### Configuração Recomendada em VPS

1. Instalar Python e dependências
2. Clonar o repositório
3. Configurar `.env` com suas credenciais
4. Usar `screen` ou `tmux` para manter rodando
5. Ou configurar como serviço do sistema (systemd no Linux)

### Opção 5: Deixar Computador Sempre Ligado

Se você tem um computador que pode ficar sempre ligado:

1. Configure para não entrar em modo suspenso
2. Use `screen` ou `tmux` para rodar os bots
3. Configure para iniciar automaticamente ao ligar (opcional)

**macOS - Prevenir Suspensão:**
```bash
# Prevenir suspensão (até reiniciar)
caffeinate -d

# Prevenir suspensão indefinidamente (em nova janela)
caffeinate -d &
```

**Linux - Prevenir Suspensão:**
- Configurar no gerenciador de energia para nunca suspender

## 📋 Recomendações

### Para Uso Pessoal/Teste
- Use `screen` ou `tmux` se você mantém o computador ligado
- Use `nohup` para testes rápidos

### Para Uso Profissional/24/7
- **Melhor opção**: VPS/Servidor Cloud
- Configure como serviço do sistema
- Monitore regularmente
- Configure alertas para erros

### Checklist ao Desligar o Computador

Se você vai desligar e os bots estão rodando:

1. ✅ **Parar os bots de forma segura**:
   ```bash
   ./stop_bots.sh
   ```

2. ✅ **Verificar que não há ordens abertas** (opcional, o bot cancela ao parar)

3. ✅ **Salvar configurações importantes**:
   ```bash
   git add .
   git commit -m "Backup antes de desligar"
   ```

4. ✅ **Fazer backup do `.env`** (manualmente, pois está no .gitignore):
   ```bash
   cp .env .env.backup
   ```

## 🚨 Avisos Importantes

1. **Ordens Abertas**: Ao desligar, ordens abertas podem permanecer na exchange. O bot tenta cancelar ao encerrar, mas se desligar abruptamente, pode não cancelar.

2. **Saldo**: Deixe saldo suficiente para cobrir as ordens abertas quando voltar.

3. **Preços**: Mercados mudam rapidamente. Ordens abertas podem ser executadas enquanto o bot está parado.

4. **Monitoramento**: Mesmo rodando 24/7, monitore regularmente para garantir que está funcionando.

## 💡 Dica

Para desenvolvimento/teste: Use `screen` ou `tmux` e mantenha o computador ligado.

Para produção: Use VPS/Servidor dedicado com serviço do sistema.




