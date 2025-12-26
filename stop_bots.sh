#!/bin/bash
# Script para parar todos os bots

echo "Parando todos os bots..."

# Encontrar e matar processos Python que estão rodando os bots
pkill -f "python3 bot1.py"
pkill -f "python3 bot2.py"
pkill -f "python3 bot3.py"
pkill -f "python3 bot4.py"

echo "Bots parados!"



