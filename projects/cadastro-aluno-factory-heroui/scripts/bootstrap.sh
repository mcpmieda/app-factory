#!/usr/bin/env bash
set -euo pipefail

echo "→ Preparando o projeto..."

if [ -f package-lock.json ]; then
  npm ci
else
  npm install
fi

echo "→ Instalando Chromium para os testes E2E..."
npx playwright install --with-deps chromium

echo "✓ Ambiente pronto."
echo "O app será iniciado automaticamente na porta 3000."
