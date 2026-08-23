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

## APIs e integrações

Ter backend não torna OpenAPI obrigatório.

Quando houver consumidor independente, API compartilhada, integração externa, webhook, eventos ou evolução separada entre cliente/provedor, aplicar `core/API_ENGINEERING.md` e classificar a interface como `none`, `lightweight`, `contract` ou `governed`.

- `lightweight`: tipos/validação/teste de integração podem ser suficientes para uma interface interna pequena;
- `contract`/`governed`: manter fonte de verdade machine-readable adequada ao protocolo e gates proporcionais de contrato, compatibilidade, runtime e segurança;
- HTTP/OpenAPI é default forte para API HTTP compartilhada, mas GraphQL, gRPC, AsyncAPI e Arazzo entram somente quando o requisito justificar;
- Redocly/oasdiff/Schemathesis/Pact são opções de gate, não dependências automáticas deste perfil.

## Independent Verification

Aplique `core/INDEPENDENT_VERIFICATION.md` sem transformar toda SPA em pipeline pesado.

- web app local/baixo risco pode permanecer `baseline`;
- persistência compartilhada, autenticação, múltiplos usuários ou risco médio podem elevar para `independent`;
- sistemas multiusuário/API/alto risco podem elevar para `adversarial`;
- releases de produção relevantes podem usar `release`.

Quando selecionados, Trivy/Semgrep/axe, mutation testing, Schemathesis, OWASP ZAP e Lighthouse CI rodam preferencialmente em GitHub CI/runner equivalente. Checks não aplicáveis não são instalados. Scanners não substituem os testes de fluxo nem a revisão semântica.

## Living UI e gates

Default contextual `ambient`, priorizando interaction/state e reduced motion. Exigir acessibilidade, desktop/mobile, build/audit e ausência de erro. Fluxos reais com concorrência ou transação exigem contrato servidor, autorização, idempotência e recovery antes de produção.

Para `persistent-app` ou superior, o E2E crítico deve exercitar a fonte de persistência real ou ambiente equivalente; sobreviver a refresh via `localStorage` não comprova persistência compartilhada.

Quando API `contract`/`governed` fizer parte do fluxo, o E2E/integration evidence deve provar correspondência entre contrato e implementação e os gates de `core/API_ENGINEERING.md` aplicáveis.

Quando Independent Verification ficar acima de `baseline`, `VERIFICATION.md`/workflow registra checks `required/advisory`, alvo seguro e exceções. DAST/fuzz destrutivo nunca aponta para produção por inferência.

Evidence: `examples/web-app-pilot/` and `research/V0.9_UNIVERSAL_VALIDATION.md`.
