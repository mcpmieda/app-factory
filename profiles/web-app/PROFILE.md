# General Web App Profile

Status: `validated`

## Quando usar

Experiências interativas voltadas ao usuário final com jornada/estado próprios, sem corresponder claramente a CRUD, dashboard ou ferramenta administrativa.

Antes de aplicar os defaults abaixo, classifique o produto com `core/SYSTEM_ENGINEERING.md`. Este perfil descreve forma de aplicação, não autoriza reduzir um sistema persistente/multiusuário a uma SPA local.

## Defaults comprovados

- modelar primeiro o fluxo completo e seus estados vazio, validação, loading, erro/sucesso;
- estado local e dados estáticos **somente enquanto forem suficientes ao requisito real** e apenas como fonte autoritativa quando o produto for legitimamente `local-app`;
- schema único para validação;
- testes unit/integration e browser do início ao fim.

Vite + React + TypeScript + Zod é uma opção comprovada para SPA pequena, não stack universal.

## Persistência e backend

Persistência, auth, cache cliente, backend e SSR continuam condicionais — porém a condição vem do produto, não da preferência por simplicidade.

- `local-app`: armazenamento local pode ser final quando o requisito é realmente individual/local;
- `persistent-app`: exige fonte de dados durável independente do navegador/dispositivo;
- `multi-user-system` ou superior: exige arquitetura compartilhada/server-side compatível com `core/SYSTEM_ENGINEERING.md`;
- demo/protótipo pode usar mocks ou `localStorage`, mas deve ser identificado como demo e não como sistema de produção completo.

Não herdar dashboard shell, Data Grid, ReUI, banco ou módulos do `web-admin` quando não forem necessários. Da mesma forma, não omitir banco/backend/auth/autorização quando o nível do sistema os exigir.

## Living UI e gates

Default contextual `ambient`, priorizando interaction/state e reduced motion. Exigir acessibilidade, desktop/mobile, build/audit e ausência de erro. Fluxos reais com concorrência ou transação exigem contrato servidor, autorização, idempotência e recovery antes de produção.

Para `persistent-app` ou superior, o E2E crítico deve exercitar a fonte de persistência real ou ambiente equivalente; sobreviver a refresh via `localStorage` não comprova persistência compartilhada.

Evidence: `examples/web-app-pilot/` and `research/V0.9_UNIVERSAL_VALIDATION.md`.
