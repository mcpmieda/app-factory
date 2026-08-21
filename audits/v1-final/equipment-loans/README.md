# Empréstimos de Equipamentos

Sistema administrativo local e fictício para uma escola saber quais equipamentos estão disponíveis, com quem está cada item e quais devoluções estão atrasadas.

## O que funciona

- inventário com estados disponível, emprestado e atrasado;
- empréstimo com responsável e data prevista;
- devolução preservando o histórico;
- busca por item, patrimônio ou responsável;
- filtros de situação, incluindo apenas atrasados;
- bloqueio transacional de dois empréstimos ativos para o mesmo item;
- persistência SQLite entre recargas durante a auditoria local.

## Requisitos

- Node.js 22–24;
- npm 10.9.9.

## Iniciar

```bash
npm ci
npm run setup
npm run dev
```

Abra `http://localhost:3000`. O seed usa somente pessoas e equipamentos fictícios.

## Validar

```bash
npm run format:check
npm run lint
npm run typecheck
npm run test:coverage
npm run build
npm audit --audit-level=high
npx playwright install chromium
npm run e2e
```

O E2E recria somente `data/e2e.db`, exercita empréstimo → reload → devolução em desktop e mobile, testa atrasados, teclado, overflow, console e `prefers-reduced-motion`.

## Limite operacional

SQLite foi escolhido porque esta é uma auditoria local de um único processo. Ele não é uma decisão automática de produção. Antes de publicar para uso real, escolha o provider conforme concorrência/deploy e adicione identidade/autorização no servidor; este projeto deliberadamente não inventa login ou credenciais.
