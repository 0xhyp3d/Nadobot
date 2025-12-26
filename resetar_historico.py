#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para resetar o histórico de P/L dos bots
Cria backup antes de resetar
"""

import os
import shutil
import time
from datetime import datetime

def reset_history(bot_name: str):
    """Resetar histórico de um bot específico"""
    history_file = f"logs/{bot_name}_history.json"
    
    if not os.path.exists(history_file):
        print(f"⚠️  Arquivo de histórico não encontrado: {history_file}")
        return False
    
    # Criar backup
    timestamp = int(time.time())
    backup_file = f"{history_file}.backup_{timestamp}"
    shutil.copy2(history_file, backup_file)
    print(f"✅ Backup criado: {backup_file}")
    
    # Remover arquivo original
    os.remove(history_file)
    print(f"✅ Histórico resetado: {history_file}")
    
    return True

def main():
    print("═══════════════════════════════════════════════════════════")
    print("  🔄 RESETAR HISTÓRICO DE P/L DOS BOTS")
    print("═══════════════════════════════════════════════════════════")
    print()
    print("⚠️  ATENÇÃO: Isso vai resetar o histórico de P/L calculado.")
    print("   Um backup será criado antes de resetar.")
    print()
    print("   O lucro REAL da sua conta NÃO será afetado.")
    print("   Apenas o cálculo teórico será resetado.")
    print()
    
    bots = ['Bot1', 'Bot2', 'Bot3', 'Bot4']
    
    print("Bots disponíveis:")
    for i, bot in enumerate(bots, 1):
        print(f"  {i}. {bot}")
    print(f"  5. Todos os bots")
    print()
    
    choice = input("Escolha o bot para resetar (1-5): ").strip()
    
    if choice == '5':
        print("\n🔄 Resetando TODOS os bots...")
        for bot in bots:
            print(f"\n--- {bot} ---")
            reset_history(bot)
    elif choice in ['1', '2', '3', '4']:
        bot_idx = int(choice) - 1
        bot_name = bots[bot_idx]
        print(f"\n🔄 Resetando {bot_name}...")
        reset_history(bot_name)
    else:
        print("❌ Opção inválida!")
        return
    
    print()
    print("═══════════════════════════════════════════════════════════")
    print("  ✅ RESET CONCLUÍDO")
    print("═══════════════════════════════════════════════════════════")
    print()
    print("Os bots vão começar a calcular P/L do zero na próxima execução.")
    print("O lucro REAL da sua conta permanece inalterado.")
    print()

if __name__ == "__main__":
    main()


