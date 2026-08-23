# VERIFICATION

> Plano durável de verificação do projeto. Preencher proporcionalmente; não transformar em checklist universal.

## Classificação

- risco: `<low|medium|high|critical>`
- nível do sistema: `<website|local-app|persistent-app|multi-user-system|production-system|critical-system>`
- API mode: `<none|lightweight|contract|governed>`
- Independent Verification: `<baseline|independent|adversarial|release>`
- executor preferido: `github_ci`
- política de custo: `free-only`

## Evidência primária

- lint/typecheck/build:
- testes unitários/integrados:
- E2E/browser:
- persistência/autorização:
- critérios Semantic Verification:

## Verificadores independentes

| Check | Ferramenta | Status | Trigger | Motivo |
| --- | --- | --- | --- | --- |
| Supply chain/secrets | Trivy ou equivalente | `<required/advisory/n-a>` | PR | |
| SAST | Semgrep CE ou equivalente | `<required/advisory/n-a>` | PR | |
| Mutation testing | StrykerJS/mutmut/equivalente | `<required/advisory/n-a>` | PR seletivo/release | |
| API fuzz/property | Schemathesis/equivalente | `<required/advisory/n-a>` | PR/release | |
| DAST baseline | OWASP ZAP | `<required/advisory/n-a>` | PR | |
| DAST ativo | OWASP ZAP | `<required/advisory/n-a>` | release | |
| Acessibilidade | axe-core + Playwright | `<required/advisory/n-a>` | PR | |
| Performance/qualidade | Lighthouse CI | `<required/advisory/n-a>` | release | |

Remova linhas não aplicáveis. Ferramenta alternativa gratuita pode ser usada quando tecnicamente melhor.

## Ambiente de teste

- alvo efêmero/local:
- banco/seed fictício:
- credenciais de teste:
- teardown:
- produção explicitamente fora de alvo para fuzz/DAST ativo: `sim`

## Thresholds e budgets

Registre somente thresholds derivados de baseline real. Não inventar 100% mutation score ou Lighthouse 100 universal.

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
