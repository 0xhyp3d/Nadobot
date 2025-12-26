#!/bin/bash
# Script para abrir 3 terminais automaticamente (macOS Terminal)
# Execute: ./open_logs.sh

# Verificar se está no macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "Este script funciona apenas no macOS"
    exit 1
fi

# Abrir Terminal 1 - Bot1
osascript <<EOF
tell application "Terminal"
    activate
    do script "cd /Users/igorbirni/Bot && echo '=== BOT1 - LOGS EM TEMPO REAL ===' && tail -f logs/bot1.log"
end tell
EOF

sleep 1

# Abrir Terminal 2 - Bot2
osascript <<EOF
tell application "Terminal"
    activate
    do script "cd /Users/igorbirni/Bot && echo '=== BOT2 - LOGS EM TEMPO REAL ===' && tail -f logs/bot2.log"
end tell
EOF

sleep 1

# Abrir Terminal 3 - Bot3
osascript <<EOF
tell application "Terminal"
    activate
    do script "cd /Users/igorbirni/Bot && echo '=== BOT3 - LOGS EM TEMPO REAL ===' && tail -f logs/bot3.log"
end tell
EOF

echo "3 terminais foram abertos, cada um mostrando os logs de um bot!"





