---
name: independent-verification
description: Use when software risk, system level, API exposure, CI, persistence, migrations, integrations or production release justify evidence independent from the implementing AI. Selects a minimal free/open-source matrix across security, mutation, property/combinatorial testing, database safety, architecture, browser compatibility, load, resilience and CI self-protection without duplicating Semantic Assurance, Semantic Verification, API Engineering or Security Review.
---

# Independent Verification

## Objetivo

Produzir evidência independente do raciocínio da IA implementadora usando ferramentas determinísticas gratuitas/open source, preferencialmente em GitHub Actions ou executor equivalente.

Leia `core/INDEPENDENT_VERIFICATION.md` antes de selecionar ferramentas.

## Responsabilidade

Esta Skill não decide sozinha a intenção, arquitetura, API ou threat model.

- `semantic-assurance` deriva domínio, invariantes, estados e candidatos a property/combinatorial testing;
- `semantic-verification` define comportamentos que precisam de prova;
- `api-engineering` define gates de contrato/API;
- `security-review` prioriza ameaças;
- esta Skill monta a menor matriz de verificadores independentes capaz de cobrir os riscos materiais;
- `execution-router` escolhe o backend capaz.

## Procedimento

1. Recupere risco, nível de sistema, API mode e semantic depth já classificados.
2. Rode/derive `python scripts/independent_verification.py --root <projeto> ...` quando o runtime estiver disponível.
3. Confirme sinais técnicos: workflows GitHub, UI/browser, API contract, linguagem/testes, migrations PostgreSQL, limites arquiteturais, invariantes/estados, load tests e integrações externas.
4. Escolha o menor modo suficiente: `baseline`, `independent`, `adversarial` ou `release`.
5. Materialize somente checks aplicáveis no workflow/config do projeto.
6. Prefira GitHub Actions com permissões mínimas, versões fixadas, dados fictícios e ambiente efêmero.
7. Classifique cada check como `required`, `advisory`, `not-applicable` ou `exception`.
8. Não transforme ferramenta ausente em `pass`.
9. DAST/fuzz/load/fault injection nunca inferem produção/terceiro como alvo.
10. Registre decisões duráveis em `VERIFICATION.md` acima de `baseline`.

## Defaults por classe

### Segurança e qualidade técnica

- **Supply chain/secrets/misconfiguration**: Trivy.
- **SAST**: Semgrep Community Edition; Opengrep é substituto qualificado após piloto, não scanner paralelo padrão.
- **DAST**: OWASP ZAP; baseline em PR, active somente em alvo autorizado/release.
- **Acessibilidade**: axe-core + Playwright.
- **Performance de página**: Lighthouse CI com baseline real.

### Força/exploração dos testes

- **Mutation JS/TS**: StrykerJS.
- **Mutation Python**: mutmut.
- **API fuzz/property/stateful**: Schemathesis quando API Engineering indicar.
- **REST stateful profundo**: Microsoft RESTler somente para API REST/OpenAPI `governed` complexa, normalmente release/nightly.
- **Property domínio Python**: Hypothesis.
- **Property domínio JS/TS**: fast-check.
- **Combinatorial/t-way**: NIST ACTS ou covering-array generator equivalente quando Semantic Assurance demonstrar espaço combinatório real.

### Infraestrutura e operação

- **GitHub Actions correctness**: actionlint.
- **GitHub Actions security**: zizmor.
- **PostgreSQL migration safety**: Squawk quando migrations PostgreSQL existirem.
- **Architecture conformance JS/TS**: dependency-cruiser ou equivalente quando limites forem declarados.
- **Load/concurrency**: k6 quando workload/SLO/baseline justificar.
- **Network resilience**: Toxiproxy ou equivalente quando integrações externas forem materiais.
- **Cross-browser web release**: Playwright Chromium + Firefox + WebKit quando o produto suportar esses engines; não aplicar a extensão específica de Chrome por reflexo.

## Regras de não redundância

- não rodar Semgrep CE + Opengrep só para aumentar número de scanners;
- Schemathesis continua API fuzz principal; RESTler é escalonamento stateful profundo;
- Lighthouse não substitui k6 e k6 não substitui Lighthouse;
- Hypothesis/fast-check testam propriedades do domínio, não duplicam mutation testing;
- ACTS só entra quando há múltiplas dimensões finitas relevantes;
- Squawk só entra em PostgreSQL compatível;
- dependency-cruiser só bloqueia se houver arquitetura declarada/config executável.

## Custo

A camada é `free-only` por padrão. Não introduza serviço pago, token de SaaS comercial ou segunda IA paga. Se GitHub-hosted runner não couber na franquia disponível, prefira self-hosted/local já disponível em vez de criar gasto sem autorização.

## Gate de conclusão

Quando um check for `required`, a entrega não passa enquanto:

- o check não tiver executado com sucesso; ou
- existir exceção explícita, pequena, tecnicamente justificada e versionada conforme o risco permitir.

Revisão semântica de risco médio/alto continua separada: scanners, fuzzers, model generators e linters não contam como segundo agente/contexto.
