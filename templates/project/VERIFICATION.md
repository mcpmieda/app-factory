# VERIFICATION

> Plano durável de verificação do projeto. Preencher proporcionalmente; não transformar em checklist universal.

## Classificação

- risco: `<low|medium|high|critical>`
- nível do sistema: `<website|local-app|persistent-app|multi-user-system|production-system|critical-system>`
- API mode: `<none|lightweight|contract|governed>`
- semantic depth: `<none|scenario|domain|formal>`
- Independent Verification: `<baseline|independent|adversarial|release>`
- integrações externas materiais: `<sim|não>`
- executor preferido: `github_ci`
- política de custo: `free-only`

## Evidência primária

- lint/typecheck/build:
- testes unitários/integrados:
- E2E/browser:
- persistência/autorização:
- critérios Semantic Verification:

## Verificadores independentes selecionados

> Remova linhas não aplicáveis. Não preencha tudo por reflexo.

| Classe | Ferramenta default | Status | Trigger | Motivo local |
| --- | --- | --- | --- | --- |
| Supply chain/secrets | Trivy ou equivalente | `<required/advisory/n-a>` | PR | |
| SAST | Semgrep CE ou Opengrep substituto validado | `<required/advisory/n-a>` | PR | |
| CI correctness | actionlint | `<required/advisory/n-a>` | PR | |
| CI security | zizmor | `<required/advisory/n-a>` | PR | |
| Mutation testing | StrykerJS/mutmut/equivalente | `<required/advisory/n-a>` | PR seletivo/release | |
| Domain property testing | Hypothesis/fast-check | `<required/advisory/n-a>` | PR seletivo/release | |
| Combinatorial/t-way | NIST ACTS/equivalente | `<required/advisory/n-a>` | PR seletivo/release | |
| API fuzz/property | Schemathesis/equivalente | `<required/advisory/n-a>` | PR/release | |
| API stateful deep | Microsoft RESTler | `<required/advisory/n-a>` | release/nightly | |
| DAST baseline | OWASP ZAP | `<required/advisory/n-a>` | PR | |
| DAST ativo | OWASP ZAP | `<required/advisory/n-a>` | release | |
| PostgreSQL migration safety | Squawk/equivalente | `<required/advisory/n-a>` | PR | |
| Architecture conformance | dependency-cruiser/equivalente | `<required/advisory/n-a>` | PR | |
| Cross-browser E2E | Playwright Chromium/Firefox/WebKit | `<required/advisory/n-a>` | PR seletivo/release | |
| Acessibilidade | axe-core + Playwright | `<required/advisory/n-a>` | PR | |
| Page quality | Lighthouse CI | `<required/advisory/n-a>` | release | |
| Load/concurrency | k6 | `<required/advisory/n-a>` | PR seletivo/release | |
| Network resilience | Toxiproxy/equivalente | `<required/advisory/n-a>` | PR seletivo/release | |

Ferramenta alternativa gratuita pode substituir um default quando tecnicamente melhor. Não rode equivalentes redundantes sem ganho documentado.

## Modelos/artefatos geradores, quando aplicável

- propriedades derivadas de invariantes/ranges/estados:
- modelo combinatorial (`specs/combinatorial-model.json` ou equivalente):
- workload/SLO/thresholds de k6:
- configuração RESTler:
- regras arquiteturais:
- migrations PostgreSQL verificadas:

Um modelo inexistente não deve ser fingido como gate executado. ACTS/RESTler/architecture checks só bloqueiam quando o artefato necessário estiver materializado.

## Ambiente de teste

- alvo efêmero/local:
- banco/seed fictício:
- credenciais de teste:
- stubs/proxies de integrações:
- teardown:
- produção explicitamente fora de alvo para fuzz/DAST ativo/load/fault injection: `sim`
- terceiros explicitamente fora de alvo para carga/fault injection: `sim`

## Thresholds e budgets

Registre somente thresholds derivados de requisito, SLO ou baseline real. Não inventar:

- `100%` mutation score universal;
- Lighthouse 100 universal;
- número arbitrário de usuários simultâneos;
- latência sem requisito/baseline;
- t-way arbitrário só porque ACTS está disponível.

## Exceções/suppressions

Toda exceção deve conter:

- finding/check;
- justificativa;
- escopo mínimo;
- owner/revisão;
- prazo de revisão quando temporária.

## Última evidência relevante

- commit/PR:
- data:
- checks required: `<pass/fail>`
- checks advisory:
- limitações conhecidas:
