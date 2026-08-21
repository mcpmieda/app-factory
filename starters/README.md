# Starters

A Factory deve iniciar projetos a partir de bases testadas, não de pastas vazias, quando houver starter adequado.

## Primeiros starters planejados

1. `web-admin` — sistema administrativo/dashboard.
2. `web-app` — aplicação web full-stack geral.
3. `website` — site institucional/conteúdo.
4. `chrome-extension` — extensão Chrome moderna.
5. `automation` — automação/script/integração.

## Estratégia

Cada starter deve conter apenas o universalmente útil ao tipo de projeto: estrutura, configuração, testes, lint/typecheck, CI, documentação mínima, design system quando aplicável, `AGENTS.md`/ponte para Factory e `PROJECT_STATE.md` inicial.

Não incluir banco, auth, analytics ou serviços externos em todo starter se o projeto não precisar.

## Primeiro candidato

O primeiro starter será `web-admin`, com forte avaliação de shadcn + ReUI. A stack final será definida após a pesquisa estruturada da V0.2, não congelada prematuramente.