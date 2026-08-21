# General Web App Profile

Status: `validated`

## Quando usar

Experiências interativas voltadas ao usuário final com jornada/estado próprios, sem corresponder claramente a CRUD, dashboard ou ferramenta administrativa.

## Defaults comprovados

- modelar primeiro o fluxo completo e seus estados vazio, validação, loading, erro/sucesso;
- estado local e dados estáticos enquanto suficientes;
- schema único para validação;
- testes unit/integration e browser do início ao fim.

Vite + React + TypeScript + Zod é uma opção comprovada para SPA pequena, não stack universal.

## Condicionais e anti-defaults

Persistência, auth, cache cliente, backend e SSR entram apenas por necessidade real. Não herdar dashboard shell, Data Grid, ReUI, banco ou módulos do `web-admin`.

## Living UI e gates

Default contextual `ambient`, priorizando interaction/state e reduced motion. Exigir acessibilidade, desktop/mobile, build/audit e ausência de erro. Fluxos reais com concorrência ou transação exigem contrato servidor, autorização, idempotência e recovery antes de produção.

Evidence: `examples/web-app-pilot/` and `research/V0.9_UNIVERSAL_VALIDATION.md`.
