# Portability

A App Factory pertence ao repositório, não a um modelo, provedor ou domínio de negócio específico.

## Núcleo neutro

Devem continuar independentes do agente e do tipo de organização:

- princípios/workflow/risco/Definition of Done;
- Skills;
- Context/Autonomy/Execution/Learning contracts;
- System Engineering, API Engineering, Semantic Assurance e Independent Verification;
- Semantic Verification e artefatos;
- templates/scripts/testes;
- Issues/PRs/Git;
- documentação de produto/arquitetura.

O Core é general-purpose. Convenções escolares, comerciais, governamentais ou de qualquer outro domínio pertencem aos projetos/perfis, não ao contrato universal.

## APIs e contratos

Quando uma interface precisar de contrato formal, prefira padrões abertos/versionáveis adequados ao protocolo: OpenAPI, GraphQL SDL, Protobuf, AsyncAPI ou Arazzo.

Redocly CLI, oasdiff, Schemathesis e Pact são defaults condicionais, substituíveis por equivalentes quando a classe de prova permanecer equivalente e a decisão ficar registrada.

Não amarre correção de API a consulta online instável quando contrato/ruleset/tooling puder ser reproduzido localmente.

## Semantic Assurance portátil

`core/SEMANTIC_ASSURANCE.md` não depende de IA, solver ou model checker específico.

A parte determinística usa JSON versionável, IDs, fingerprints, consistência e semantic diff. Em `scenario`, nenhum runtime adicional é obrigatório; em `domain`, o engine stdlib cobre estrutura/referências/cobertura/diff.

Defaults condicionais por propriedade:

- Hypothesis (Python) / fast-check (JS/TS) para property/stateful testing;
- NIST ACTS ou covering-array equivalent para combinatorial/t-way testing;
- Z3/SMT para restrições;
- Alloy para relações/cardinalidades;
- NASA FRET/FRETish para temporal/reactivo;
- P ou Quint/TLA+ para estado/concorrência/distribuído;
- DMN para decisões;
- OPA/Rego ou Cedar para policy/autorização.

Ferramenta gratuita/open source equivalente pode substituir um default quando preservar a propriedade/prova esperada. Formalização/modelo obrigatório precisa de artefato, source refs e gate real.

## Independent Verification portátil

`core/INDEPENDENT_VERIFICATION.md` pertence ao núcleo, não ao GitHub/Codex ou a um scanner.

A matriz é `free-only` e organizada por **classe de falha**, não por marca:

- Trivy — supply chain/secrets/misconfiguration;
- Semgrep CE — SAST; Opengrep é alternativa qualificada, não execução paralela obrigatória;
- StrykerJS/mutmut — mutation;
- Schemathesis — API property/fuzz/stateful;
- RESTler — escalonamento REST stateful profundo;
- OWASP ZAP — DAST;
- axe-core + Playwright — acessibilidade;
- Lighthouse CI — page quality;
- actionlint — correção do GitHub Actions;
- zizmor — segurança do GitHub Actions;
- Squawk — migration safety PostgreSQL;
- dependency-cruiser/equivalente — architecture conformance;
- k6 — load/concurrency;
- Toxiproxy/equivalente — network resilience;
- Playwright multi-engine — browser compatibility quando o produto suportar.

Esses nomes são defaults, não lock-in. Não executar equivalentes redundantes sem ganho demonstrado.

GitHub Actions é executor preferido quando disponível; runner próprio, outro CI ou execução local equivalente podem produzir a mesma evidência. A correção não pode depender de comprar minutos, SaaS ou segunda IA paga.

Workflows/configs devem:

- fixar versões/commits;
- manter permissões mínimas;
- evitar secrets em forks;
- usar alvo efêmero/autorizado para fuzz/DAST/load/fault injection;
- produzir relatórios portáveis quando possível;
- distinguir `required`, `advisory`, `not-applicable` e `exception`.

## Adaptadores

### Codex

`AGENTS.md` funciona como mapa e aponta para fontes comuns.

### Claude Code

Criar `CLAUDE.md` curto quando necessário, sem duplicar Core/Skills.

### Cursor/outros

Adaptadores mínimos somente quando o cliente exigir formato próprio.

## Regra contra divergência

Nunca manter cópias completas independentes das mesmas regras em `AGENTS.md`, `CLAUDE.md`, `.cursor/rules` etc.

API governance, Semantic Assurance e Independent Verification seguem a mesma regra: perfis/templates/projetos registram decisões locais e apontam para o contrato comum.

## Estado do trabalho

Handoff durável usa:

`repo + branch/PR + PROJECT_STATE + Issue + testes`.

Quando API for `contract/governed`, inclua contrato/baseline de compatibilidade.

Quando semantic depth for `domain/formal`, inclua semantic-contract, semantic-assurance, diff/baseline e formalizações/modelos required.

Quando Independent Verification estiver acima de `baseline`, inclua `VERIFICATION.md`/workflow, checks, alvo seguro, thresholds/modelos e exceções.

## Dados operacionais locais

- `.factory/context/` — cache regenerável;
- `.factory/execution.json` — histórico bounded local;
- `.factory/learning.json` — aprendizado técnico allowlisted local;
- `.factory/state.json` — pode ser versionado em handoff importante.

Ausência desses caches não bloqueia continuidade. Learning é otimização, nunca requisito para correção/segurança.

Da mesma forma, ausência de fornecedor específico de scanner/solver/load/fault tool não reduz gate: use equivalente capaz ou registre indisponibilidade/exceção; nunca marque `pass` por conveniência.
