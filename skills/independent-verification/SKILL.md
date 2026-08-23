---
name: independent-verification
description: Use when software risk, system level, API exposure, authentication, production release or shared data justify evidence independent from the implementing AI. Selects free/open-source deterministic verification engines such as mutation testing, API fuzzing, DAST, SAST, supply-chain scanning, accessibility and Lighthouse without duplicating Semantic Verification, API Engineering or Security Review.
---

# Independent Verification

## Objetivo

Produzir evidência independente do raciocínio da IA implementadora usando ferramentas determinísticas gratuitas/open source, preferencialmente em GitHub Actions.

Leia `core/INDEPENDENT_VERIFICATION.md` antes de selecionar ferramentas.

## Responsabilidade

Esta Skill **não** decide sozinha a intenção do produto, o contrato de API ou o threat model.

- `semantic-verification` define comportamentos que precisam de prova;
- `api-engineering` define gates de contrato/API;
- `security-review` prioriza ameaças;
- esta Skill monta a matriz de verificadores externos e sua cadência;
- `execution-router` escolhe o backend capaz.

## Procedimento

1. Recupere risco, nível de sistema e API mode já classificados.
2. Rode/derive o plano determinístico com `python scripts/independent_verification.py --root <projeto> ...` quando o runtime estiver disponível.
3. Confirme sinais técnicos: UI web, OpenAPI/GraphQL, testes existentes e linguagem.
4. Escolha o menor modo suficiente: `baseline`, `independent`, `adversarial` ou `release`.
5. Materialize somente os checks aplicáveis no workflow/config do projeto.
6. Prefira GitHub Actions com permissões mínimas, versões fixadas e ambiente efêmero.
7. Classifique cada check como `required`, `advisory`, `not-applicable` ou `exception`.
8. Não transforme ferramenta indisponível em `pass`.
9. Para DAST/fuzz, nunca inferir produção como alvo; usar ambiente descartável/autorizado.
10. Registre decisões duráveis em `VERIFICATION.md` quando o modo for acima de `baseline`.

## Defaults por classe

- **SAST**: Semgrep Community Edition.
- **Supply chain/secrets/misconfiguration**: Trivy.
- **Mutation JS/TS**: StrykerJS.
- **Mutation Python**: mutmut.
- **API fuzz/property/stateful**: Schemathesis quando API Engineering indicar.
- **DAST**: OWASP ZAP; baseline em PR e active somente em release/alto risco contra alvo autorizado.
- **Acessibilidade web**: axe-core + Playwright.
- **Performance/qualidade web**: Lighthouse CI quando houver baseline estável.

Ferramenta equivalente pode substituir um default quando gratuita, madura e melhor para a stack; documente a razão.

## Custo

A camada é `free-only` por padrão. Não introduza serviço pago, token de SaaS comercial ou segunda IA paga. GitHub-hosted runner pode usar a franquia disponível; se isso não for suficiente, prefira self-hosted/local já disponível em vez de criar gasto sem autorização.

## Gate de conclusão

Quando um check for `required`, a entrega não passa enquanto:

- o check não tiver executado com sucesso; ou
- existir exceção explícita, pequena, tecnicamente justificada e versionada conforme o risco permitir.

Uma revisão semântica de risco médio/alto continua separada: scanners não contam como segundo agente/contexto.
